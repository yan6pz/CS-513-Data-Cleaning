import os
import evaluate as e
import sys
import csv
import StringIO

total_score_column_name = "_Total_Score"
sol_file_column_name = "_File_Name"


def evaluate(sols_dir, sols_file):
    print "Evaluating file: {0}".format(sols_file)
    prblm_wise_score, total_score = e.evaluate(os.path.join(sols_dir, sols_file), StringIO.StringIO())
    evaluation = prblm_wise_score
    evaluation[total_score_column_name] = total_score
    evaluation[sol_file_column_name] = sols_file
    return evaluation


def bulk_evaluate(sols_dir, output_csv):
    sols_dir = resolve_sols_dir(sols_dir)
    output_header = create_output_header()
    evaluations = [evaluate(sols_dir, f) for f in os.listdir(sols_dir) if os.path.isfile(os.path.join(sols_dir, f))]
    # Write to csv
    with open(output_csv, 'wb') as f:
        w = csv.DictWriter(f, output_header)
        w.writeheader()
        w.writerows(evaluations)


def create_output_header():
    prblms = e.problem_names()
    output_header = [sol_file_column_name]
    output_header.extend(prblms)
    output_header.append(total_score_column_name)
    return output_header


def resolve_sols_dir(sols_dir):
    if not os.path.isabs(sols_dir):
        # Regex home dir
        regex_home_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(regex_home_dir, sols_dir)
    else:
        return sols_dir


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Directory containing solution files should be provided as first command line argument" \
              " and output csv file name should be second command line argument."
        sys.exit(0)
    sols_dir = sys.argv[1]
    output_csv = sys.argv[2]
    bulk_evaluate(sols_dir, output_csv)
