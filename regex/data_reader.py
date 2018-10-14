import os

__test_cases_dir = 'test_cases'
__positive_examples_indicator = "Positive examples:"
__negative_examples_indicator="Negative examples:"
__ignore_case_indicator="Ignore case:"
__comment_char = '#'


def read_test_cases():
    # Read regex home.
    regex_home_dir = os.path.dirname(os.path.abspath(__file__))
    # Under regex home, find test cases dir
    test_cases_dir = os.path.join(regex_home_dir, __test_cases_dir)
    test_cases_files = __get_test_cases_files(test_cases_dir)
    return __get_positive_and_negative_examples(test_cases_dir, test_cases_files)


def read_solution(solutions_file):
    if os.path.isabs(solutions_file):
        regex_sols_file = solutions_file
    else:
        # Regex home dir
        regex_home_dir = os.path.dirname(os.path.abspath(__file__))
        regex_sols_file = os.path.join(regex_home_dir, solutions_file)
    regex_solutions = __read_file(regex_sols_file)
    solutions = {}
    for regex_sol in regex_solutions:
        prblm, sol = __extract_sol(regex_sol)
        if prblm is not None:
            solutions[prblm] = sol
    return solutions

def __extract_sol(sol):
    solarr = sol.split('=', 1)
    if len(solarr) <= 1: return None
    prblm = solarr[0].strip()
    sol = solarr[1].strip()[1:-1] # Strip off first and last single quote.
    return prblm, sol


def __get_test_cases_files(test_cases_dir):
    return [f for f in os.listdir(test_cases_dir) if os.path.isfile(os.path.join(test_cases_dir, f))]


def __get_positive_and_negative_examples(test_cases_dir, test_cases_files):
    test_cases = {}
    for test_file in test_cases_files:
        test_cases[__strip_extension(test_file)] = __extract_pos_neg_examples(test_cases_dir, test_file)
    return test_cases


def __extract_pos_neg_examples(test_cases_dir, test_file):
    data = __read_file(os.path.join(test_cases_dir, test_file))
    ignore_case = __ignore_case_value(data)
    pos_example_start_index = __get_index_of(data, __positive_examples_indicator)
    neg_example_start_index = __get_index_of(data, __negative_examples_indicator)
    if pos_example_start_index < neg_example_start_index:
        pos_examples = data[pos_example_start_index+1:neg_example_start_index]
        neg_examples = data[neg_example_start_index+1:]
    else:
        neg_examples = data[neg_example_start_index+1:pos_example_start_index]
        pos_examples = data[pos_example_start_index+1:]
    return pos_examples, neg_examples, ignore_case


def __ignore_case_value(data):
    new_list = [item.lower() for item in data]
    index = -1
    for x in new_list:
        if x.startswith(__ignore_case_indicator.lower()):
            index = new_list.index(x)
    if index == -1:
        return True
    else:
        return data[index].split(':')[1].strip() == "true"


def __get_index_of(l, str):
    new_list = [item.lower() for item in l]
    try:
        return new_list.index(str.lower())
    except ValueError:
        return -1


def __strip_extension(file):
    return file.split('.')[0]


def __read_file(test_file):
    with open(test_file) as f_in:
        lines = list(line.strip() for line in f_in) # All lines including the blank ones
        lines = [line for line in lines if line] # Non-blank lines
        lines = [line for line in lines if not line.startswith(__comment_char)] # remove comment lines.
    return tuple(lines)
