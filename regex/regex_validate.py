import re


def validate(regexp, positive_examples, negative_examples, ignore_case):
    if ignore_case:
        false_neg = filter(None, [x for x in positive_examples
                                if not re.match(regexp + "$", x, re.I)])  
        false_pos = filter(None, [x for x in negative_examples
                                  if re.match(regexp + "$", x, re.I)])
    else:
        false_neg = filter(None, [x for x in positive_examples
                                if not re.match(regexp + "$", x)])
        false_pos = filter(None, [x for x in negative_examples
                                  if re.match(regexp + "$", x)])
    return false_neg, false_pos

