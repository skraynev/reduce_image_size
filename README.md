# Installation

* install uv via [oficial doc](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
* install dependencies
```sh
uv sync
```

# Run linter check
```sh
uv run ruff check --fix
```

# Usage

Compress all files in ~/test_images/ directory on 0.8 of original file size 
```sh
uv run resize.py ~/test_images/ 0.8
```

Compress all "jpg" files in ~/test_images/ directory on 0.5 of original file size
```sh
uv run resize.py ~/test_images/ 0.5 --regex *.jpg
```

Compress all "png" files in ~/test_images/ directory on 0.75 of original file size
and pack to "result.pdf"
```sh
uv run resize.py ~/test_images/ 0.75 --regex *.jpg --pdf result
```