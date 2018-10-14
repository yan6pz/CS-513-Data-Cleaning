import sql_util as su
#import traceback as tb
import math
import sys
import metadata_reader


def evaluate(mr, print_feedback_to=None):
    total_score = 0
    results = {}
    problem_names = mr.problem_names()
    for problem_name in problem_names:
        score = evaluate_problem(problem_name, mr, print_feedback_to)
        results[problem_name] = score
        total_score += score
        print_output("___________________________________________________________________________", print_feedback_to)
    total_score = int(math.ceil(total_score))
    print_output("Total Score: {0}/{1}".format(total_score, mr.total_marks()), print_feedback_to)
    return results, total_score


def evaluate_problem(problem_name, mr, print_feedback_to):
    print_output("Evaluating problem: {0}".format(problem_name), print_feedback_to)
    score = 0.0
    expected_output_file = mr.expected_output_file_path(problem_name)
    database_file = mr.database_path(problem_name)
    query_file = mr.query_file_path(problem_name)
    sort_before_comparison = mr.sort_before_comparison(problem_name)
    try:
        passed = su.cmp_select_output_with_csv(expected_output_file, database_file, query_file, sort_before_comparison)
        if passed:
            score = mr.score_fraction(problem_name)*mr.total_marks()
            print_output("\tYour output matches with expected output. Score={0}".format(score), print_feedback_to)
        else:
            print_output("\tYour output doesn't match with expected output. Score={0}".format(score), print_feedback_to)
    except Exception as e:
        print_output("\t" + e.message + "Score={0}".format(score), print_feedback_to)
        #tb.print_exc(file=print_feedback_to)
    return score


def print_output(message, print_feedback_to):
    print >> print_feedback_to, message


if __name__ == "__main__":
    solutions_dir = "solutions"
    config_file = "grading_config.json"
    meta_reader = metadata_reader.JSONMetadataReader(config_file, solutions_dir)
    results_g, total_score_g = evaluate(meta_reader, sys.stdout)
