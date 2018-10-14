from metadata_reader import JSONMetadataReader as JSONMdr
import dlv_util as du
import sys


def evaluate(mr, print_feedback_to=None):
    total_score = 0
    results = {}
    try:
        problem_names = mr.problem_names()
        for problem_name in problem_names:
            score = evaluate_problem(problem_name, mr, print_feedback_to)
            results[problem_name] = score
            total_score += score
            print_output("___________________________________________________________________________", print_feedback_to)
        print_output("Total Score: {0:.2f}/{1}".format(round(total_score, 2), mr.total_marks()), print_feedback_to)
        return results, total_score
    except Exception as e:
        print_output(e.message, print_feedback_to)
        return results, total_score


def evaluate_problem(problem_name, mr, print_feedback_to):
    dlv_script_path = mr.script_path(problem_name)
    print_output("Evaluating problem: {0}".format(problem_name), print_feedback_to)
    facts_add = facts_added(problem_name, mr)
    # If facts are added by student, then award 0 marks else evaluate script.
    if facts_add:
        score = 0.0
        print_output("\tYou are not allowed to add any facts. Score={0}".format(score), print_feedback_to)
    else:
        score = round(evaluate_predicates(problem_name, mr, print_feedback_to), 2)
        print_output("\tTotal Score for problem: {0:.2f}".format(score), print_feedback_to)
    return score


def facts_added(problem_name, mr):
    script_file_path = mr.script_path(problem_name)
    facts = du.extract_facts([script_file_path])
    return len(facts) != 0


def evaluate_predicates(problem_name, mr, print_feedback_to):
    score = 0.0
    for predicate_name in mr.predicate_names(problem_name):
        score += evaluate_predicate(problem_name, predicate_name, mr, print_feedback_to)
    return score


def evaluate_predicate(problem_name, predicate_name, mr, print_feedback_to):
    run_output = dlv_run(problem_name, predicate_name, mr)
    expected_output = mr.predicates(problem_name, predicate_name)
    c = cmp(run_output, expected_output)
    score = 0.0
    if c != 0:
        print_output("\tYour output for {0} doesn't match with expected output. Score={1}"
                     .format(predicate_name, score), print_feedback_to)
    else:
        score = mr.predicate_score_fraction(problem_name, predicate_name)*mr.total_marks()
        print_output("\tYour output for {0} matches with expected output. Score={1}"
                     .format(predicate_name, score), print_feedback_to)
    return score


def dlv_run(problem_name, predicate_name, mr):
    script_file_path = mr.script_path(problem_name)
    facts_file_path = mr.facts_file_path(problem_name, predicate_name)
    dlv_run_output = du.run_with_filter([facts_file_path, script_file_path], mr.dlv_filter(problem_name, predicate_name))
    return du.sorted_predicates_list(dlv_run_output)


def print_output(message, print_feedback_to):
    print >> print_feedback_to, message


if __name__ == '__main__':
    if len(sys.argv) < 3:
        if len(sys.argv) < 2:
            sols_dir = ""
            config_file = "grading_config.json"
        else:
            sols_dir = sys.argv[1]
            config_file = "grading_config.json"
    else:
        sols_dir = sys.argv[1]
        config_file = sys.argv[2]
    mr_o = JSONMdr(config_file, sols_dir)
    evaluate(mr_o, sys.stdout)
