import data_reader as dr
import sys
import regex_validate as rv
import json
import os

# Read configuration.
json_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grading_config.json")
with open(json_config_file) as jc_file: grading_config = json.load(jc_file)
total_marks_key = "total_marks"
marks_division_key = "marks_division"


def calculate_marks(prblm, total_tests, total_mistakes, print_feedback_to):
    try:
        total_marks_of_prblm = (grading_config[total_marks_key]*grading_config[marks_division_key][prblm])*1.0
    except KeyError:
        print_output("Scoring criteria for {0} is not provided in the config".format(prblm), print_feedback_to)
        return 0
    marks_per_test_case = total_marks_of_prblm/total_tests
    deductions = total_mistakes*marks_per_test_case
    marks_scored = total_marks_of_prblm - deductions
    return marks_scored


def evaluate_problem(test_cases, prblm, sol, print_feedback_to):
    marks_scored = 0
    try:  # Valid problem.
        marks_scored = grade_problem(test_cases, prblm, sol, print_feedback_to)
    except KeyError:
        print_output("Invalid problem {0}".format(prblm), print_feedback_to)
    print_output("---------------------------------------------------------------------------", print_feedback_to)
    return marks_scored


def grade_problem(test_cases, prblm, sol, print_feedback_to):
    test_case = test_cases[prblm]
    print_output("Evaluating {0}".format(prblm), print_feedback_to)
    false_neg, false_pos = rv.validate(sol, test_case[0], test_case[1], test_case[2])
    if len(false_neg) == 0 and len(false_pos) == 0:
        print_output("{0} passed".format(prblm), print_feedback_to)
    else:
        report_false_negatives(false_neg, print_feedback_to)
        report_false_positives(false_pos, print_feedback_to)
    marks_scored = calculate_marks(prblm, len(test_case[0]) + len(test_case[1]),
                                   len(false_neg) + len(false_pos), print_feedback_to)
    marks_scored = round(marks_scored, 2)
    print_output("Score: {0:.2f}".format(marks_scored), print_feedback_to)
    return marks_scored


def report_false_negatives(false_neg, print_feedback_to):
    if len(false_neg) > 0:
        print_output("Following expressions should have been matched by your regex but didn't match.", print_feedback_to)
        for expr in false_neg:
            print_output("\t {0}".format(expr), print_feedback_to)


def report_false_positives(false_pos, print_feedback_to):
    if len(false_pos) > 0:
        print_output("Following expressions should not have been matched by your regex but did match.", print_feedback_to)
        for expr in false_pos:
            print_output("\t {0}".format(expr), print_feedback_to)


def evaluate(sol_file, print_feedback_to=None):
    prblm_wise_score = {}
    total_score = 0
    max_score = grading_config[total_marks_key]
    try:
        # Read solutions
        solutions = dr.read_solution(sol_file)
        # Read test cases.
        test_cases = dr.read_test_cases()
        print_output("Starting evaluation of regex. For each regex, we will show false positive matches and false negative matches, if any."
                      , print_feedback_to)
        # Evaluate for each problem
        for prblm, sol in sorted(solutions.iteritems()):
            prblm_score = evaluate_problem(test_cases, prblm, sol, print_feedback_to)
            total_score += prblm_score
            prblm_wise_score[prblm] = prblm_score
        print_output("Total Score: {0:.2f}/{1}".format(round(total_score, 2), grading_config[total_marks_key]), print_feedback_to)
        return prblm_wise_score, total_score, max_score
    except Exception as e:
        print_output(e.message, print_feedback_to)
        return prblm_wise_score, total_score, max_score


def problem_names():
    return sorted(dr.read_test_cases().keys())


def print_output(message, print_feedback_to):
    print >> print_feedback_to, message


if __name__ == '__main__':
    evaluate('Solutions.txt', sys.stdout)


def test(cells):
    if "physical_description 2" not in cells or cells["physical_description 2"]["value"] == '':
        return ''
    elif cells.get("physical_description 3", None) is None or cells["physical_description 3"]["value"] == '':
        if cells.get("physical_description 4", None) is None or cells["physical_description 4"]["value"] == '':
            return cells["physical_description 2"]["value"] + " - - "
        else:
            return cells["physical_description 2"]["value"] + " - - " + cells["physical_description 4"]["value"]
    else:
        return cells["physical_description 2"]["value"] + " - " + cells["physical_description 3"]["value"] + " - " + cells["physical_description 4"]["value"]
