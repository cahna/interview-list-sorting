import random
import string
from typing import List, Tuple

"""
Static test data as tuples of (input_text, expected_text)
"""
TEST_DATA: List[Tuple[str, str]] = [
    *[(s, "\n") for s in string.whitespace + string.punctuation],
    ("999999 -999999", "-999999 999999\n"),
    ("apple orange banana\n", "apple banana orange\n"),
    ("1 10 3 8 5\n", "1 3 5 8 10\n"),
    ("-1 -10 -3 -8 -5\n", "-10 -8 -5 -3 -1\n"),
    ("car 10 truck 4 2 bus\n", "bus 2 car 4 10 truck\n"),
    ("20 cat bi?rd 12 do@g\n", "12 bird cat 20 dog\n"),
    ("-20 -cat bi?rd 12 do@g\n", "-20 bird cat 12 dog\n"),
    ("a b c 1 2 3", "a b c 1 2 3\n"),
    ("-a -b -c -1 -2 -3", "a b c -3 -2 -1\n"),
    ("-a- -b- -c- -1- -2- -3-", "a b c -3 -2 -1\n"),
    ("--a1-- ---b2--- -c-3- --1- -2-- --3--", "a1 b2 c3 -3 -2 -1\n"),
    ("a man, a plan, a canal: panama", "a a a canal man panama plan\n"),
    ("%", "\n"),
    ("  $ $ $ $ ", "\n"),
    ("-", "\n"),
]

INT_2000 = range(-9999, 9999 + 1)

"""
Fuzzing test data
"""
TEST_DATA_RANDOM: List[Tuple[str, str]] = [
    ("".join((random.choices(string.whitespace + string.punctuation, k=100))), "\n"),
    (
        "a".join((random.choices(string.punctuation, k=100))),
        "a" * 99 + "\n",
    ),
    (
        (" " * random.randint(1, 10)).join(
            map(str, random.sample(INT_2000, k=len(INT_2000)))
        ),
        " ".join(map(str, INT_2000)) + "\n",
    ),
]
