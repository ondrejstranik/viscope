# Viscope
This is the  base package for virtual/real microscope controlling system

## Add-on packages
[spectralCamera](https://github.com/ondrejstranik/spectralCamera) - package to control various spectral cameras

[plim](https://github.com/ondrejstranik/plim) -  package to control plasmon imaging sensors

[hmflux](https://github.com/ondrejstranik/hmflux) - package to control holographic min-Flux localisation microscopy

[aposim](https://github.com/ondrejstranik/aposim) -  package to control microsocpe with apoptome functionality




## Package installation
0. start conda,create new environment (name = viscope) `conda create --name viscope python=3.9`
1. start conda, activate your environment `conda activate xxx` (xxx .. name of your environment)
2. move to the package folder `cd yyy` (yyy ... name of the folder)
3. type `python -m pip install -e. --config-settings editable_mode=strict`
