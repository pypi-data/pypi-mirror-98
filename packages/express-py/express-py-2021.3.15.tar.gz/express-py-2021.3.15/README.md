[![PyPI version](https://badge.fury.io/py/express-py.svg)](https://badge.fury.io/py/express-py)
[![License: Apache](https://img.shields.io/badge/License-Apache-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# ExPreSS

Exabyte Property Extractor, Sourcer, Serializer (ExPreSS) is a Python package to extract material- and simulation-related properties and serialize them according to the Exabyte Data Convention (EDC) outlined in [Exabyte Source of Schemas and Examples (ESSE)](https://github.com/Exabyte-io/exabyte-esse). 

## Functionality

As below:

- Extract structural information, material properties and from simulation data
- Serialize extracted information according to ESSE/EDC
- Support for multiple simulation engines, including:
  - [VASP](#links)
  - [Quantum ESPRESSO](#links)
  - others, to be added

The package is written in a modular way easy to extend for additional applications and properties of interest. Contributions can be in the form of additional [functionality](#todo-list) and [bug/issue reports](https://help.github.com/articles/creating-an-issue/).

## Architecture

The following diagram presents the package architecture. The package provides an [interface](express/__init__.py) to extract properties in EDC format. Inside the interface `Property` classes are initialized with a `Parser` (Vasp, Espresso, or Structure) depending on the given parameters through the parser factory. Each `Property` class implements required calls to `Parser` functions listed in these [Mixins Classes](express/parsers/mixins) to extract raw data either from the textual files, XML files or input files in string format and implements a serializer to form the final property according to the EDC format.

![ExPreSS](https://user-images.githubusercontent.com/10528238/53124591-9958e700-3510-11e9-9222-3aedacfd7943.png)

### Parsers

As explained above, ExPreSS parsers are responsible for extracting raw data from different sources such as data on the disk and provide the raw data to properties classes. In order to make sure all parsers implement the same interfaces and abstract properties classes from the parsers implementations, a set a [Mixin Classes](express/parsers/mixins) are provided which should be mixed with the parsers. The parsers must implement Mixins' abstract methods at the time of inheritance.

### Properties

ExPreSS properties classes are responsible to form the properties based on the raw data provided by the parsers and serialize the property according to EDC. A list of supported properties are available in [here](express/settings.py).

### Extractors

Extractors are classes that are composed with the parsers to extract raw data from the corresponding sources such as text or XML.

## Installation

ExPreSS can be installed as a Python package either via PyPi or the repository as below.

#### PyPi

```bash
pip install express
```

#### Repository

0. Install [git-lfs](https://help.github.com/articles/installing-git-large-file-storage/) in order to pull the files stored on Git LFS.

1. Clone repository:
    
    ```bash
    git clone git@github.com:Exabyte-io/exabyte-express.git
    ```

2. Install [virtualenv](https://virtualenv.pypa.io/en/stable/) using [pip](https://pip.pypa.io/en/stable/) if not already present:

    ```bash
    pip install virtualenv
    ```

3. Create virtual environment and install required packages:

    ```bash
    cd exabyte-express
    virtualenv venv
    source venv/bin/activate
    export GIT_LFS_SKIP_SMUDGE=1
    pip install -e PATH_TO_EXPRESS_REPOSITORY
    ```

## Usage

### Extract Total Energy

The following example demonstrates how to initialize an ExPreSS class instance, to extract and serialize total energy produced in a Quantum ESPRESSO calculation. The full path to the calculation directory (`work_dir`) and the file containing standard output (`stdout_file`) are required to be passed as arguments to the underlying Espresso parser.

```python

import json
from express import ExPrESS

kwargs = {
    "work_dir": "./tests/fixtures/espresso/test-001",
    "stdout_file": "./tests/fixtures/espresso/test-001/pw-scf.out"

}

express_ = ExPrESS("espresso", **kwargs)
print json.dumps(express_.property("total_energy"), indent=4)

```

### Extract Relaxed Structure

In this example the final structure of a VASP calculation is extracted and is serialized to a material. The final structure is extracted from the `CONTCAR` file located in the calculation directory (`work_dir`). `is_final_structure=True` argument should be passed to the [Material Property](express/properties/material.py) class to let it know to extract final structure.

```python

import json
from express import ExPrESS

kwargs = {
    "work_dir": "./tests/fixtures/vasp/test-001",
    "stdout_file": "./tests/fixtures/vasp/test-001/vasp.out"

}

express_ = ExPrESS("vasp", **kwargs)
print json.dumps(express_.property("material", is_final_structure=True), indent=4)

```

### Extract Structure from Input

One can use [StructureParser](express/parsers/structure.py) to extract materials from POSCAR or PW input files. Please note that `StructureParser` class only works with strings and not files and therefore the input files should be read first and then passed to the parser.

```python

import json
from express import ExPrESS

with open("./tests/fixtures/vasp/test-001/POSCAR") as f:
    poscar = f.read()

kwargs = {
    "structure_string": poscar,
    "structure_format": "poscar"
}

express_ = ExPrESS("structure", **kwargs)
print json.dumps(express_.property("material"), indent=4)

with open("./tests/fixtures/espresso/test-001/pw-scf.in") as f:
    pwscf_input = f.read()

kwargs = {
    "structure_string": pwscf_input,
    "structure_format": "espresso-in"
}

express_ = ExPrESS("structure", **kwargs)
print json.dumps(express_.property("material"), indent=4)

```

## Tests

There are two types of tests in ExPreSS, unit and integration, implemented in [Python Unit Testing Framework](https://docs.python.org/2/library/unittest.html).

### Unit Tests

Unit tests are used to assert properties are serialized according to EDC. Properties classes are initialized with mocked parser data and then are serialized to assert functionality.

### Integration Tests

Parsers functionality is tested through integration tests. The parsers are initialized with the configuration specified in the [Tests Manifest](./tests/manifest.yaml) and then the functionality is asserted.

### Run Tests

Run the following commands to run the tests.

```bash
sh run-tests.sh -t=unit
sh run-tests.sh -t=integration
```

## Contribution

This repository is an [open-source](LICENSE.md) work-in-progress and we welcome contributions. We suggest forking this repository and introducing the adjustments there, the changes in the fork can further be considered for merging into this repository as explained in [GitHub Standard Fork and Pull Request Workflow](https://gist.github.com/Chaser324/ce0505fbed06b947d962).

## TODO list

Desirable features for implementation:

- Add support for other properties
- Add support for other types of applications, parsers and extractors
- other (TBA)

## Links

1. [Exabyte Source of Schemas and Examples (ESSE), Github Repository](https://github.com/exabyte-io/exabyte-esse)
1. [Vienna Ab-initio Simulation Package (VASP), official website](https://cms.mpi.univie.ac.at/vasp/)
1. [Quantum ESPRESSO, Official Website](https://www.quantum-espresso.org/)
