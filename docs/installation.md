# Installation

## For users

Use this if you just want to use Viscope in your own project (no need to
edit Viscope's own source).

0. (optional) create and activate a dedicated conda environment
```bash
conda create --name viscope python=3.10
conda activate viscope
```
1. install directly from the GitHub repository
```bash
python -m pip install git+https://github.com/ondrejstranik/viscope.git
```

This installs the latest version from the `main` branch.

2. to upgrade later, force a fresh install. A plain `--upgrade` is not
   enough for git dependencies -- pip only checks that the URL still
   matches, not whether the remote has new commits -- so
   `--force-reinstall` is required too (`--no-deps` keeps it from also
   reinstalling every other dependency):
```bash
python -m pip install --upgrade --force-reinstall --no-deps git+https://github.com/ondrejstranik/viscope.git
```

## For developers

Use this if you want to modify Viscope itself -- the package is installed
in editable mode, so changes to the source take effect immediately without
reinstalling.

0. clone the repository and move into it
```bash
git clone https://github.com/ondrejstranik/viscope.git
cd viscope
```
1. create and activate a conda environment
```bash
conda create --name viscope python=3.10
conda activate viscope
```
2. install the package in editable mode
```bash
python -m pip install -e .
```

If you use Pylance in VS Code, add the following to `.vscode\settings.json`
so it can resolve the package while it's installed in editable mode:
```json
    "python.languageServer": "Pylance",
    "python.analysis.extraPaths": [
        "path\to\the\package\folder"
    ],
```
