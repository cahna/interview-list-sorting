import heapq
import io
import re
import string
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Generator, Iterable, List, Optional, Type, Union

RE_SPLIT_WHITESPACE = re.compile("(?:^|\w+)((?:(?![^\w]*).)*)")
RE_NON_ALPHANUMERIC = re.compile("[^a-z0-9]", re.IGNORECASE)
RE_IS_NUMBER = re.compile("^(\d+)$")


def clean_parse_word(word: str) -> Union[str, int]:
    """Remove ignored characters from word and parse word to int if word represents an int"""
    clean_word = re.sub(RE_NON_ALPHANUMERIC, "", word)
    if RE_IS_NUMBER.match(clean_word):
        return int(clean_word) * (word.startswith("-") and -1 or 1)
    return clean_word


def iter_split(handle: io.IOBase) -> Iterable[Union[str, int]]:
    """Iterator-based algorithm.
    - Load entire text file as a string.
    - Split words by whitespace.
    - Remove ignorable characters using regex replace.
    - Parse input into strings and ints using regex matching.
    """
    return (
        clean_parse_word(m.group(0))
        for m in re.finditer(RE_SPLIT_WHITESPACE, handle.read())
        if m.group(0)
    )


def gen_split(handle: io.IOBase) -> Generator[Union[str, int], None, None]:
    """Generator-based algorithm.
    - 1 byte is read from file at a time (requirements specify ASCII only).
    - Split words by whitespace.
    - Remove ignorable characters using regex replace.
    - Parse input into strings and ints using regex matching.
    """
    current_match: List[str] = []
    character = handle.read(1)

    while character:
        if character in string.whitespace:
            if current_match:
                yield clean_parse_word("".join(current_match))
                current_match = []
        else:
            current_match.append(character)

        character = handle.read(1)

    if current_match:
        yield clean_parse_word("".join(current_match))

    handle.close()


def gen_split_2(handle: io.IOBase) -> Generator[Union[str, int], None, None]:
    """Generator-based algorithm.
    - 1 byte is read from file at a time (requirements specify ASCII only).
    - Split words by whitespace.
    - Remove ignorable characters and determine appropriate parsing on-the-fly.
    """
    current_match: List[str] = []
    character = handle.read(1)
    parser: Union[Type[str], Type[int]] = str

    while character:
        if character in string.whitespace:
            if current_match:
                yield parser("".join(current_match))
                current_match = []
        else:
            if current_match:
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
            else:
                if character in "-" + string.digits:
                    # Possible (negative) number
                    parser = int

            current_match.append(character)

        character = handle.read(1)

    if current_match:
        yield parser("".join(current_match))

    handle.close()
