import io
import re
import string
from typing import Callable, Generator, Iterable, List, Union

RE_NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]", re.IGNORECASE)
RE_NOT_A_DIGIT = re.compile(r"[^0-9]")
RE_IS_POSITIVE_NUMBER = re.compile(r"^[^a-z\-\d]*((?:\d|[^a-z])+)$", re.IGNORECASE)
RE_IS_NEGATIVE_NUMBER = re.compile(r"^[^a-z\d]*(-(?:[^a-z]*\d[^a-z]*)+)", re.IGNORECASE)


def clean_and_parse_word(word: str) -> Union[str, int]:
    """
    Remove bad characters from word & parse into int if appropriate.
    """
    if m := RE_IS_NEGATIVE_NUMBER.match(word):
        capture = m.group(0)
        number_string = re.sub(RE_NOT_A_DIGIT, "", capture)

        if number_string:
            return int(number_string) * -1
    elif m := RE_IS_POSITIVE_NUMBER.match(word):
        capture = m.group(0)
        number_string = re.sub(RE_NOT_A_DIGIT, "", capture)

        if number_string:
            return int(number_string)

    return re.sub(RE_NON_ALPHANUMERIC, "", word)


def iter_split(handle: io.IOBase) -> Iterable[Union[str, int]]:
    """Iterator-based algorithm.
    - Load entire text file as a string.
    - Iterate over words using re.finditer to split on whitespace.
    - Remove ignorable characters using regex replace.
    - Parse input into strings and ints using regex matching.
    """

    class IterSplit:
        def __init__(self, fh: io.IOBase):
            self.re_iter = re.finditer(r"\S+", fh.read())

        def _get_next_match(self):
            if match := next(self.re_iter):
                return match

            raise StopIteration

        def __iter__(self):
            return self

        def __next__(self):
            match = self._get_next_match()
            group = match.group(0).strip()

            while not group:
                match = self._get_next_match()
                group = match.group(0).strip()

            word = clean_and_parse_word(group)

            if word:
                return word

            return self.__next__()

    return (s for s in IterSplit(handle))

    # return (
    #     clean_and_parse_word(m.group(0))
    #     for m in re.finditer(r"\S+", handle.read())
    #     if m.group(0)
    # )


def gen_split(handle: io.IOBase) -> Generator[Union[str, int], None, None]:
    """Generator-based algorithm.
    - 1 byte is read from file at a time (requirements specify ASCII only).
    - Split words by whitespace.
    - Remove ignorable characters using regex replace.
    - Parse input into strings and ints using regex matching.
    """
    current_match: List[str] = []

    while character := handle.read(1):
        if character in string.whitespace:
            if current_match:
                yield clean_and_parse_word("".join(current_match))
                current_match = []
        else:
            current_match.append(character)

    if current_match:
        yield clean_and_parse_word("".join(current_match))

    handle.close()


def gen_split_2(handle: io.IOBase) -> Generator[Union[str, int], None, None]:
    """Generator-based algorithm.
    - 1 byte is read from file at a time (requirements specify ASCII only).
    - Split words by whitespace.
    - Remove bad characters and determine appropriate parsing on-the-fly.
    """
    current_match: List[str] = []
    parser: Callable[[str], Union[str, int]] = str

    while character := handle.read(1):
        if character in string.whitespace:
            if current_match:
                yield parser("".join(current_match))
                current_match = []
        else:
            if current_match:  # Building current word
                if character in string.ascii_letters:
                    if parser == int:
                        # No longer possible to be an int
                        parser = str
                        if current_match[0] == "-":
                            # Because word is string, '-' should be ignored
                            current_match.pop(0)
                elif character not in string.digits:
                    # Not alphanumeric, so ignore
                    continue
            else:  # Beginning of a word
                if character in "-" + string.digits:
                    # Possible (negative) number
                    parser = int
                elif character not in string.ascii_letters:
                    # Not alphanumeric, so ignore
                    continue

            current_match.append(character)

    handle.close()

    if current_match:
        yield parser("".join(current_match))
