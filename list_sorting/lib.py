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


# @profile  # Uncomment before running mprof
def split_iterator_read_all_parse_regex(
    get_text: Callable[[], str]
) -> Iterable[Union[str, int]]:
    """Iterator-based algorithm that loads entire file before using regex iterator to
    split words. Words are sanitized and parsed by additional regex(es).
    """

    class IterSplit:
        def __init__(self, read_all: Callable[[], str]):
            self.re_iter = re.finditer(r"\S+", read_all())

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

            if word == 0 or word:
                return word

            return self.__next__()

    return (s for s in IterSplit(get_text))


# @profile  # Uncomment before running mprof
def split_generator_read_1_parse_regex(
    get_next_character: Callable[[], str]
) -> Generator[Union[str, int], None, None]:
    """Generator-based algorithm that loads one character at a time to find
    words. Once a word is found, regex are used to sanitize and parse the word.
    """
    current_match: List[str] = []

    while character := get_next_character():
        if character in string.whitespace:
            if current_match:
                word = clean_and_parse_word("".join(current_match))
                if word == 0 or word:
                    yield word
                current_match = []
        else:
            current_match.append(character)

    if current_match:
        word = clean_and_parse_word("".join(current_match))
        if word == 0 or word:
            yield word


# @profile  # Uncomment before running mprof
def split_generator_read_1_parse_manual(
    get_next_character: Callable[[], str],
) -> Generator[Union[str, int], None, None]:
    """Generator-based algorithm that scans one character at a time to find
    and sanitize words. The type of the word is inferred during scanning.

    Hypothesis: this is the best algorithm for time/space.
    """
    current_match: List[str] = []
    parser: Callable[[str], Union[str, int]] = str

    while character := get_next_character():
        if character in string.whitespace:
            if current_match and current_match != ["-"]:
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

    if current_match and current_match != ["-"]:
        yield parser("".join(current_match))


# @profile  # Uncomment before running mprof
def split_generator_read_all_parse_manual(get_text: Callable[[], str]):
    """Read all of text file, then pass each character to split_generator_read_1_parse_manual"""
    text = get_text()
    text_len = len(text)
    i = 0

    def next_char():
        nonlocal i
        if i < text_len:
            c = text[i]
            i += 1
            return c
        return None

    return split_generator_read_1_parse_manual(next_char)
