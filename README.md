# Programming Test Python

## Usage

1. Install [`poetry`](https://python-poetry.org/)
2. Create venv: `python3 -m venv venv`
3. Activate venv: `source venv/bin/activate`
4. Install dependencies: `poetry install`
5. Run script: `listSorting --help`

## Examples

### Sort input1.txt and output to `stdout`

```sh
listSorting input1.txt
```

### Sort input3.txt and write output to output3.txt

```sh
listSorting input3.txt output3.txt
```

### Pipe input via `stdin` and output to `stdout`

```sh
listSorting < input4.txt
```
