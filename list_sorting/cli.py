import heapq
import sys
from enum import Enum, unique
from typing import List, Mapping, Union

import typer

from .lib import (
    split_generator_read_1_parse_manual,
    split_generator_read_1_parse_regex,
    split_iterator_read_all_parse_regex,
)


@unique
class Algorithm(str, Enum):
    ITERATOR = "iterator"
    GENERATOR = "generator"
    GENERATOR2 = "generator2"


IMPLEMENTATIONS = {
    Algorithm.ITERATOR: split_iterator_read_all_parse_regex,
    Algorithm.GENERATOR: split_generator_read_1_parse_regex,
    Algorithm.GENERATOR2: split_generator_read_1_parse_manual,
}


def list_sorting(
    algorithm: Algorithm = typer.Option(Algorithm.GENERATOR2),
    input_file: typer.FileText = typer.Argument(sys.stdin, help="Input file"),
    output_file: typer.FileTextWrite = typer.Argument(sys.stdout, help="Output file"),
):
    """Sort a list of strings and numbers, ignoring non-alphanumeric characters"""
    implementation = IMPLEMENTATIONS[algorithm]

    # Keep track of the order in which strings and ints appear in the input
    type_order = []

    # O(1) insert into heap, leveraging the invariant and heapsort for performance
    type_heaps: Mapping[type, List[Union[int, str]]] = {str: [], int: []}

    for match in implementation(input_file):
        type_order.append(type(match))
        heapq.heappush(type_heaps[type(match)], match)

    for i in range(len(type_order)):
        type_ = type_order[i]
        typer.echo(str(heapq.heappop(type_heaps[type_])), nl=False, file=output_file)
        if i < len(type_order) - 1:
            typer.echo(" ", nl=False, file=output_file)

    # All examples end with newline
    typer.echo("\n", nl=False, file=output_file)


def cli():
    typer.run(list_sorting)


if __name__ == "__main__":
    cli()
