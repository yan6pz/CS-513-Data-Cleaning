import json
import operator
import os


class MetadataReader(object):
    def problem_names(self):
        raise NotImplementedError("This method must be implemented.")

    def database_path(self, problem_name):
        raise NotImplementedError("This method must be implemented.")

    def query_file_path(self, problem_name):
        raise NotImplementedError("This method must be implemented.")

    def expected_output_file_path(self, problem_name):
        raise NotImplementedError("This method must be implemented.")

    def sort_before_comparison(self, problem_name):
        raise NotImplementedError("This method must be implemented.")

    def score_fraction(self, problem_name):
        raise NotImplementedError("This method must be implemented.")

    def total_marks(self):
        raise NotImplementedError("This method must be implemented.")


class JSONMetadataReader(MetadataReader):
    __total_marks_key = "total_marks"
    __databases_dir_key = "databases_dir"
    __solutions_output_dir_key = "solutions_output_dir"
    __problems_key = "problems"
    __score_key = "score"
    __order_key = "order"
    __database_file_key = "database_file"
    __sort_before_comparison_key = "sort"
    __query_file_suffix = ".sql"
    __expected_output_file_suffix = ".csv"

    # Read not_for_learner/README.txt

    def __init__(self, json_file_path, solutions_dir):
        # File path should either be absolute or relative to the path of current python file.
        json_file_path = JSONMetadataReader.__resolve_path(json_file_path)
        with open(json_file_path) as jc_file:
            self.grading_config = json.load(jc_file)
        self.solutions_dir = solutions_dir

    def problem_names(self):
        return self.__order_dict(self.grading_config[self.__problems_key])

    def database_path(self, problem_name):
        database_dir = self.grading_config[self.__databases_dir_key]
        database_file = self.grading_config[self.__problems_key][problem_name][self.__database_file_key]
        database_path = os.path.join(database_dir, database_file)
        return self.__resolve_path(database_path)

    def query_file_path(self, problem_name):
        query_file = problem_name + self.__query_file_suffix
        query_file_path = os.path.join(self.solutions_dir, query_file)
        return self.__resolve_path(query_file_path)

    def expected_output_file_path(self, problem_name):
        expected_output_dir = self.grading_config[self.__solutions_output_dir_key]
        expected_output_file = problem_name + self.__expected_output_file_suffix
        expected_output_file_path = os.path.join(expected_output_dir, expected_output_file)
        return self.__resolve_path(expected_output_file_path)

    def sort_before_comparison(self, problem_name):
        return self.grading_config[self.__problems_key][problem_name][self.__sort_before_comparison_key]

    def score_fraction(self, problem_name):
        return self.grading_config[self.__problems_key][problem_name][self.__score_key]

    def total_marks(self):
        return float(self.grading_config[self.__total_marks_key])

    def __order_dict(self, d):
        # Sort by order attribute.
        new_dict = {key: value[self.__order_key] for key, value in d.iteritems()}
        sorted_dict_items = sorted(new_dict.items(), key=operator.itemgetter(1))
        return [x[0] for x in sorted_dict_items]

    @staticmethod
    def __resolve_path(path):
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
        return path
