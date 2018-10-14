import os
import re
from sys import platform

import shell_util as shell_utils

__dlv_program__ = {'windows': 'dlw-win.exe', 'linux': 'dlv-linux.bin', 'mac': 'dlv-apple.bin'}
__dlv_program_dir__ = 'dlv_binary'


def sorted_predicates_list(dlv_output):
    """
    Takes a dlv output and extracts all the predicates in it.

    Whole of line should be enclosed in a opening and closing brace.
    e.g. {predicate1(a1,b1,c1,...), predicate2(a2,b2,c2,...), ...}
    :param dlv_output: dlv output from which predicates have to be extracted.
    :return: a sorted list of the predicates.
    :raises: ValueError if there dlv output has more than line.
    """
    # Check number of lines.
    dlv_output_lines = _extract_lines(dlv_output)
    if len(dlv_output_lines) != 1:
        raise ValueError("Dlv output should only have one line.")
    # Strip leading and trailing braces.
    dlv_output = _strip_leading_trailing_brace_pair(dlv_output_lines[0])
    # by now, DLV output should be like: predicate1(a1,b1,c1), predicate2(a2,b2,c2,...), ...
    # We separate predicates on as each member of a list.
    predicates_list = _separate_predicates(dlv_output)
    # Sort.
    return sorted(predicates_list)


def extract_facts(dlv_scripts_abs_paths):
    """
    Extract just the facts from the given dlv scripts

    :param dlv_scripts_abs_paths list of absolute paths of the dlv scripts.
    """
    # Run with a -facts flag.
    facts_args = ['-silent', '-facts']
    dlv_facts_output = run_dlv(dlv_scripts_abs_paths, facts_args)

    # Run with a -nofacts flag.
    no_facts_args = ['-silent', '-nofacts']
    dlv_no_facts_output = run_dlv(dlv_scripts_abs_paths, no_facts_args)
    return _extract_facts_from_dlv_output(dlv_facts_output, dlv_no_facts_output)


def run_dlv(dlv_scripts_abs_paths, args=()):
    """
    Run dlv file. Pass command line args as an array.

    Unfortunately callers have to pass absolute path but as of now there is no better way: dlv program doesn't
    take commands from stdin. We could take a file-like object and write that to temp file but that seems an overkill.
    :param dlv_scripts_abs_paths: list of absolute paths of the dlv scripts.
    :param args: arguments array to be passed to the dlv file.
    :return: stdout if dlv runs successfully(retcode = 0) stderr otherwise.
    :raises: OSError if there was a problem running dlv.
    """
    dlv_program = _get_platform_dependent_dlv_program_path()
    dlv_command = [dlv_program] + list(args) + dlv_scripts_abs_paths  # add dlv_program to an array, concatenate args to it.
    ret_code, stdout, stderr = shell_utils.execute(dlv_command)
    print 'Result: ' + ''.join(stdout)
    if ret_code == 0:
        return stdout
    else:
        raise OSError(stderr)


def run_with_filter(dlv_scripts_abs_paths, dlv_filter):
    """
    Run the dlv file with a filter.
    :param dlv_scripts_abs_paths list of absolute paths of the dlv scripts.
    :param dlv_filter filter to be applied on the dlv file.
    :return: output of the dlv run.
    :raises: OSError if there was a problem running dlv.
    """
    dlv_output = run_dlv(dlv_scripts_abs_paths, ['-silent', '-filter=' + dlv_filter])
    return dlv_output


def _extract_facts_from_dlv_output(dlv_output, dlv_no_facts_output):
    """
    Extract just the facts from two dlv outputs -- one with -facts flag and one with -nofacts.

    dlv has two flags. -facts and -nofacts.
    The problem is that -facts flag doesn't just add facts to output but also derived predicates(non-facts).
    So to workaround this, dlv should be run twice with these two flags one at a time before calling this function.
    This function just extracts predicates from two runs and returns the diff.
    :param dlv_output: dlv output of a run with -facts flag.
    :param dlv_no_facts_output: dlv output of a run with -nofacts flag.
    :return: tuple of facts.
    """
    dlv_output = sorted_predicates_list(
        dlv_output)  # Facts output contains both facts and derived predicates.
    dlv_no_facts_output = sorted_predicates_list(dlv_no_facts_output)  # no facts contain just derived predicates
    facts = (x for x in dlv_output if x not in dlv_no_facts_output)
    return tuple(facts)


def _get_platform_dependent_dlv_program_path():
    """
    Get absolute path of platform(OS) dependent DLV program.

    Assumes that dlv programs for all the operating systems is in the same directory as this py file.
    Supports windows, linux and macOS right now.
    :return: absolute path of platform(OS) dependent DLV program.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dlv_program = _get_platform_dependent_dlv_program_name()
    return os.path.join(current_dir, __dlv_program_dir__, dlv_program)


def _get_platform_dependent_dlv_program_name():
    """
    Get platform dependent dlv program name. Uses __dlvProgram__ dictionary defined in this module.
    :return: platform dependent dlv program name.
    :raises: EnivronmentError if the environment is other than linux, mac or windows.
    """
    # read operating system dependent dlv program name
    if platform == "linux" or platform == "linux2":
        # linux
        return __dlv_program__['linux']
    elif platform == "darwin":
        # OS X
        return __dlv_program__['mac']
    elif platform == "win32":
        # Windows...
        return __dlv_program__['windows']
    else:
        raise EnvironmentError("Platform {0} not supported.".format(platform))


def _extract_lines(s):
    """
    Splits on line delimiter and removes empty lines.
    :param s: input string.
    :return: lines in the string.
    """
    s_arr = s.split(os.linesep)
    return [s for s in s_arr if s]


def _strip_leading_trailing_brace_pair(dlv_output):
    """
    dlv output in enclosed in braces. This function removes the braces.
    :param dlv_output: string of the format # {predicate1(a1,b1,c1,...), predicate2(a2,b2,c2,...), ...}
    :return: all of string but leading and trailing brace.
    """
    regex = re.compile(r'\{(.*)\}')  # greedy search
    predicates = re.search(regex, dlv_output)
    if predicates is None:
        raise ValueError('DLV output should have had leading and trailing brace pair.')
    else:
        return predicates.group(1)


def _separate_predicates(dlv_output):
    """
    Extracts individual predicates out of the provided dlv_output.
    :param dlv_output: dlvoutput of the form predicate1(a1,b1,c1,...), predicate2(a2,b2,c2,...)
    :return: individual predicates as members of a list.
    """
    regex = r'\)\s*,'
    repl = ')\n'
    # replace ), with )\n
    predicates_one_on_each_line = re.sub(regex, repl, dlv_output)
    # next, split on \n to get list of predicates.
    predicates = predicates_one_on_each_line.split('\n')
    return [x.strip() for x in predicates]
