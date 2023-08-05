# PyToJCAMP

[![Documentation Status](https://readthedocs.org/projects/pytojcamp/badge/?version=latest)](https://pytojcamp.readthedocs.io/en/latest/?badge=latest)
![Python package](https://github.com/cheminfo-py/pytojcamp/workflows/Python%20package/badge.svg)
![pre-commit](https://github.com/cheminfo-py/pytojcamp/workflows/pre-commit/badge.svg)
[![codecov](https://codecov.io/gh/cheminfo-py/pytojcamp/branch/master/graph/badge.svg)](https://codecov.io/gh/cheminfo-py/pytojcamp)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytojcamp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub last commit](https://img.shields.io/github/last-commit/cheminfo-py/pytojcamp)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/cheminfo-py/pytojcamp/master?filepath=examples%2Fexample.ipynb)

Python to JCAMP converter. Inspired by [PyToJCAMP](https://github.com/cheminfo/convert-to-jcamp).

Some tools work well with the [JCAMP](http://jcamp-dx.org/) format.
This package allows converting Python data structures to JCAMP, this can make it easier for Python based web services to interact with the [ELN](eln.epfl.ch).

## Installation

To get the latest development version from the head use

```
pip install git+https://github.com/cheminfo-py/pytojcamp.git
```

to install the latest stable release use

```
pip install pytojcamp
```

## Usage

See the example notebooks, which you can [try out on Binder](https://mybinder.org/v2/gh/kjappelbaum/pytojcamp/master?filepath=examples%2Fexample.ipynb).

### x/y data

For simple x/y data you can use

```python
from pytojcamp import from_xy
jcamp_string = from_xy((x,y))
```

## multicolumn data

For multicolumn data you can use

```python
from pytojcamp import from_dict

data_dictionaries = {
    'x' : {
        'data': [1,2,3],
        'type': 'INDEPENDENT',
        'unit': 'cm'
    },
    'y' : {
        'data': [3,2,3],
        'type': 'DEPENDENT',
        'unit': 'h'
    },
    'z' : {
        'data': [3,2,3],
        'type': 'DEPENDENT',
        'unit': 'kg'
    }
}

jcamp_string = from_dict(data_dictionaries)
```
