# Installation

## For users

Use this if you just want to use Viscope in your own project (no need to
edit Viscope's own source).

0. (optional) create and activate a dedicated conda environment
   `conda create --name viscope python=3.9` then `conda activate viscope`
1. install directly from the GitHub repository
   `python -m pip install git+https://github.com/ondrejstranik/viscope.git`

This installs the latest version from the `main` branch. To upgrade later,
re-run the same command with `--upgrade`.

## For developers

Use this if you want to modify Viscope itself -- the package is installed
in editable mode, so changes to the source take effect immediately without
reinstalling.

0. clone the repository and move into it
   `git clone https://github.com/ondrejstranik/viscope.git` then
   `cd viscope`
1. create and activate a conda environment
   `conda create --name viscope python=3.9` then `conda activate viscope`
2. install the package in editable mode
   `python -m pip install -e .`

If you use Pylance in VS Code, add the following to `.vscode\settings.json`
so it can resolve the package while it's installed in editable mode:
```
    "python.languageServer": "Pylance",
    "python.analysis.extraPaths": [
        "path\to\the\package\folder"
    ],
```
