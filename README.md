# A quantun computing development environment in Python
Comprises of two parts - `qusimulator` (package `qsim`) the quantum simulator, and `qucircuit` (packages `qckt`, `qckt.gatesutils`, and `qckt.backend`) the library to implement quantum computing programs using quantum circuits paradigm. `qucircuit` uses `qusimulator` as a backed engine to run quantum circuits.

## INSTALLATION
`qusimulator` and `qucircuit` are on PyPi now. So, you can simply install them using `pip`.

    pip install qusimulator
    pip install qucircuit

Since `qucircuit` has `qusimulator` as a dependency, so installing qucircuit will also install `qusimulator`.

## FEATURES
All common gates available as pre-defined. Allows user-defined gates. Allows adding control qubits to any gates. A number of utility functions to manipulate gates - combine sequentially applied or parallelly applied gates, check for unitarity, inverse.

Full featured support for quantum noise simulation. Leverages a new density-matrix based simulation engine.

Easy to follow documentation with tutorial introduction - see `qusimumator/README.md` and `qucircuit/README.md`. A bunch of examples under `examples/qsim` and `examples/qckt`. Code for regression tests also serves as examples to quickly learn `qsim` and `qckt` packages (see folder `tests/`).

Getting started tutorials - `examples/qckt/Getting-started-tutorial.ipynb`, `examples/qckt/Getting-started-tutorial-noise-sim.ipynb`

Growing list of known quantum algorithm implementations included as examples.

## CLI tool
An interactive commandline interface (`qsimcli`) to quickly check out sequence of quantum operations.
