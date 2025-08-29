# Viscope
This is the  base package for virtual/real microscope controlling system

## Add-on packages
[spectralCamera](https://github.com/ondrejstranik/spectralCamera) - package to control various spectral cameras

[plim](https://github.com/ondrejstranik/plim) -  package to control plasmon imaging sensors

[hmflux](https://github.com/ondrejstranik/hmflux) - package to control holographic min-Flux localisation microscopy

[aposim](https://github.com/ondrejstranik/aposim) -  package to control microsocpe with apoptome functionality

[scanImaging](https://github.com/ondrejstranik/scanImaging) - package to control fluorescence lifetime image scanning microscope (FLIM/ISM) 




## Package installation
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

