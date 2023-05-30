# hps-align
Tools needed to run HPS alignment workflow

This is a `pip`-installable python package; however, it will never be published to PyPI
because all of its users are expected to be its developers as well.

## Dependencies
Using `pip` to install this package whereever you wish will handle the python packages;
however, we also require to have an installation of ROOT with the PyROOT bindings.
You can check if this requirement is satisified in your environment by trying to
`import ROOT` in your python terminal.

## Install
Install an "editable" version of this package so
it is both (a) accessible by Python form wherever
and (b) will refer back to your source code so 
you can make changes without having to re-install.
```
python3 -m pip install -e .
```
On SDF, there isn't a good "local install" location,
so you should manually specify a target. Below,
I am directing python to install `hps_align` to the
python library installed with `hps-mc`.
```
python3 -m pip install --target ${HPSMC_DIR}/lib/python -e .
```

## Usage
Now that this package is "installed", you can run it from anywhere!
Run the module to see an up-to-date help printout.
```
python3 -m hps_align --help
```
