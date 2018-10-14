import os
import evaluate as e
import sys
import csv
from metadata_reader import JSONMetadataReader as JSONMdr
import cStringIO


total_score_column_name = "_Total_Score"
sol_dir_column_name = "_Dir_Name"


def bulk_evaluate(sols_dir, output_csv, config_file):
    sols_dir = resolve_sols_dir(sols_dir)
    output_header = create_output_header(config_file)
    evaluations = [evaluate(config_file, sols_dir, d) for d in os.listdir(sols_dir) if os.path.isdir(os.path.join(sols_dir, d))]
    # Write to csv
    with open(output_csv, 'wb') as f:
        w = csv.DictWriter(f, output_header)
        w.writeheader()
        w.writerows(evaluations)


def evaluate(config_file, sols_dir, d):
    print "Evaluating {0}".format(d)
    mr = JSONMdr(config_file, os.path.join(sols_dir, d))
    prblm_wise_score, total_score = e.evaluate(mr, cStringIO.StringIO())
    evaluation = prblm_wise_score
    evaluation[total_score_column_name] = total_score
    evaluation[sol_dir_column_name] = d
    print "----------------------------------------------------------------------"
    return evaluation


def resolve_sols_dir(sols_dir):
    if not os.path.isabs(sols_dir):
        # Dlv home dir
        dlv_home_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(dlv_home_dir, sols_dir)
    else:
        return sols_dir


def create_output_header(config_file):
    prblms = JSONMdr(config_file, '').problem_names()
    output_header = [sol_dir_column_name]
    output_header.extend(prblms)
    output_header.append(total_score_column_name)
    return output_header

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Directory containing solution directories should be provided as first command line argument" \
              " and output csv file name should be second command line argument."
        sys.exit(0)
    sols_dir_o = sys.argv[1]
    output_csv_o = sys.argv[2]
    if len(sys.argv) == 4:
        config_file_o = sys.argv[3]
    else:
        config_file_o = "grading_config.json"
    bulk_evaluate(sols_dir_o, output_csv_o, config_file_o)
