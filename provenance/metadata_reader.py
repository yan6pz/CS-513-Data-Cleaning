import json
import operator
import dlv_util as du
import os


class MetadataReader(object):
    def problem_names(self):
        raise NotImplementedError("This method must be implemented.")

    def script_path(self, problem_name):
        raise NotImplementedError("This method must be implemented.")

    def facts_file_path(self, problem_name, predicate_name):
        raise NotImplementedError("This method must be implemented.")

    def predicate_names(self, problem_name):
        raise NotImplementedError("This method must be implemented.")

    def dlv_filter(self, problem_name, predicate_name):
        # What should we filter on using -filter with dlv.
        raise NotImplementedError("This method must be implemented.")

    def predicates(self, problem_name, predicate_name):
        raise NotImplementedError("This method must be implemented.")

    def predicate_score_fraction(self, problem_name, predicate_name):
        raise NotImplementedError("This method must be implemented.")

    def total_marks(self):
        raise NotImplementedError("This method must be implemented.")


class JSONMetadataReader(MetadataReader):
    __total_marks_key = "total_marks"
    __solutions_output_dir_key = "solutions_output_dir"
    __facts_dir_key = "facts_dir"
    __problems_key = "problems"
    __facts_file_key = "facts_file"
    __predicates_key = "predicates"
    __score_key = "score"
    __solution_file_key = "solution_file"
    __order_key = "order"
    __dlv_filter_key = "dlv_filter"
    __dlv_file_suffix = ".dlv"

    def __init__(self, json_file_path, sols_dir):
        json_file_path = JSONMetadataReader.__resolve_path(json_file_path)
        with open(json_file_path) as jc_file:
            self.grading_config = json.load(jc_file)
        self.sols_dir = sols_dir

    def problem_names(self):
        return self.__order_dict(self.grading_config[self.__problems_key])

    def script_path(self, problem_name):
        script_file_name = problem_name + self.__dlv_file_suffix
        script_file_path = os.path.join(self.sols_dir, script_file_name)
        return self.__resolve_path(script_file_path)

    def facts_file_path(self, problem_name, predicate_name):
        facts_dir = self.grading_config[self.__facts_dir_key]
        facts_file_problem_level = self.grading_config[self.__problems_key][problem_name].get(self.__facts_file_key)
        facts_file_predicate_level = self.grading_config[self.__problems_key][problem_name][self.__predicates_key][predicate_name].get(self.__facts_file_key)
        # predicate level fact file takes priority over problem level.
        if facts_file_predicate_level is not None:
            return os.path.join(facts_dir, facts_file_predicate_level)
        else:
            return os.path.join(facts_dir, facts_file_problem_level)


    def predicate_names(self, problem_name):
        return self.__order_dict(self.grading_config[self.__problems_key][problem_name][self.__predicates_key])

    def dlv_filter(self, problem_name, predicate_name):
        # What should we filter on using -filter with dlv.
        dlv_filter_name = self.grading_config[self.__problems_key][problem_name][self.__predicates_key][predicate_name].get(self.__dlv_filter_key)
        if dlv_filter_name is None:
            # Default to predicate name.
            return predicate_name
        else:
            return dlv_filter_name

    def predicates(self, problem_name, predicate_name):
        # Read file name containing output.
        predicate_output_file = self.grading_config[self.__problems_key][problem_name][self.__predicates_key][predicate_name][self.__solution_file_key]
        # Resolve directory containing output files.
        predicate_output_dir = self.grading_config[self.__solutions_output_dir_key]
        predicate_output_dir = JSONMetadataReader.__resolve_path(predicate_output_dir)
        # Get abs path.
        predicate_out_file_abs = os.path.join(predicate_output_dir, predicate_output_file)
        # Return predicates list.
        with open(predicate_out_file_abs) as f:
            lines = f.read().strip()
            return du.sorted_predicates_list(lines)

    def predicate_score_fraction(self, problem_name, predicate_name):
        return self.grading_config[self.__problems_key][problem_name][self.__predicates_key][predicate_name][
            self.__score_key]

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
