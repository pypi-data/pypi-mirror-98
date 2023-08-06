# yamltopy

![PyPI](https://img.shields.io/pypi/v/yamltopy?style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dw/yamltopy?style=flat-square)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/szikszail/yamltopy?style=flat-square)

## Install

```shell
pip install yamltopy
```

## Usage

```
usage: yamltopy [-h] [-i INPUT] [-o OUTPUT] [-n NAME] [-v]

Convert YAML configuration file to a Python modulefor better performance

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The input Yaml file (YML or YAML)
  -o OUTPUT, --output OUTPUT
                        The output Py file
  -n NAME, --name NAME  The name of the exported variable containg the Yaml data
  -v, --verbose
```

Convert YAML file to PY:

```shell
yamltopy -i path/to/file.yaml -o path/to/output.py -n NAME_OF_VARIABLE
```

You can import the output file (if modules set up properly):

```python
from path.to.output import NAME_OF_VARIABLE

print(NAME_OF_VARIABLE)
```
