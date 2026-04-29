# pdf-text-extractor
A python cli tool used to extract the text contents of a `.pdf` file.

## Prerequisites

-   **python3** (Version >= 3.10)
-   **poetry** Python project package management tool (optional)

## Installation


### Download the script

``` bash
wget https://raw.githubusercontent.com/Vaenyx/pdf-text-extractor/main/pdf-text-extractor.py
```

### Download dependency info

#### Poetry
```bash
wget https://raw.githubusercontent.com/Vaenyx/pdf-text-extractor/main/pyproject.toml
wget https://raw.githubusercontent.com/Vaenyx/pdf-text-extractor/main/poetry.lock
```

#### Pip
```bash
wget https://raw.githubusercontent.com/Vaenyx/pdf-text-extractor/main/requirements.txt
```

## Usage

### Execution

#### Poetry
``` bash
poetry run python3 pdf-text-extractor.py [OPTIONS] filepath
```

#### Pip
``` bash
python3 -m pip install -r requirements.txt
python3 pdf-text-extractor [OPTIONS] filepath
```

### Options

| Option | Description |
|--------|-------------|
| `filepath` | PDF file path |
| `-o, --out <path>` | Output file path |
| `-s, --start <page>` | Start page |
| `-e, --end <page>` | End page |
| `-r, --replace <json>` | Replace phrases as JSON (e.g. `'{\"dog\":\"cat\"}'`) |
| `-h, --help` | Show help and exit |

---

### Examples

```bash
python3 pdf-text-extractor.py file.pdf
```

```bash
python3 pdf-text-extractor.py file.pdf -o output.txt
```

```bash
python3 pdf-text-extractor.py file.pdf -s 1 -e 5
```

```bash
python3 pdf-text-extractor.py file.pdf -r "{\"NORTH\":\"N\", \"SOUTH\": \"S\"}"
```

```bash
python3 pdf-text-extractor.py file.pdf -s 2 -e 10 -o output.txt
```
