# Installation

0. start conda,create new environment (e.g. environment'name  = viscope) `conda create --name viscope python=3.9`
1. start conda, activate your environment `conda activate viscope`
2. move to the package folder `cd path\to\the\package\folder`
3. type `python -m pip install -e.`

4. if you use pylance in vscode you have to add into the file .vscode\settings.json following
```
    "python.languageServer": "Pylance",
    "python.analysis.extraPaths": [
        "path\to\the\package\folder"
    ],
```
