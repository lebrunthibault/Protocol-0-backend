import functools
import re
from typing import List


def _compare_strings(s1: str, s2: str) -> int:
    words_1 = re.findall("\s+|\S+", s1)
    words_2 = re.findall("\s+|\S+", s2)

    for w1, w2 in zip(words_1, words_2):
        if w1 != w2:
            return 1 if w1 > w2 else -1

    for wo1, wo2, result in ((words_1, words_2, -1), (words_2, words_1, 1)):
        if len(wo1) > len(wo2):
            if wo1[len(wo2)] == " ":
                return result
            else:
                return -result

    return 0


def sort_by_name(input: List[str]) -> List[str]:
    """Sort by name like in windows explorer"""
    return sorted(input, key=functools.cmp_to_key(_compare_strings))
