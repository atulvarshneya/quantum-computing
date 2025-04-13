# Quantum Computing Development Environment in Python

This project provides a comprehensive environment for quantum computing development in Python. It consists of two main components:

1. **`qusimulator`**: A quantum simulator. It is comprised of the following package:
    - `qsim`
2. **`qucircuit`**: A library for implementing quantum computing programs using the quantum circuit paradigm. It includes the following packages:
   - `qckt`
   - `qckt.gatesutils`
   - `qckt.backend`

The `qucircuit` library uses `qusimulator` as its backend engine to execute quantum circuits.

---

## Installation

Both `qusimulator` and `qucircuit` are available on PyPI. You can install them using `pip`:

```bash
pip install qusimulator
pip install qucircuit
```

> **Note**: Installing `qucircuit` will automatically install `qusimulator` as it is a dependency.

---

## Features

### General

- **Predefined Quantum Gates**: Includes all common quantum gates.
- **Custom Gates**: Supports user-defined gates.
- **Controlled Gates**: Allows adding control qubits to any gate.
- **Gate Utilities**: Provides functions to:
  - Combine gates applied sequentially or in parallel.
  - Check for unitarity.
  - Compute the inverse of gates.

### Quantum Noise Simulation

Features a density-matrix-based simulation engine for realistic noise modeling.

### Extensive Documentation

Includes tutorials and examples to help you get started:
  - Documentation: `qusimulator/README.md` and `qucircuit/README.md`
  - Examples: `examples/qsim` and `examples/qckt`
  - Regression tests: Located in the `tests/` folder, which also serve as learning resources.
- **Tutorials**:
  - `examples/qckt/Getting-started-tutorial.ipynb`
  - `examples/qckt/Getting-started-tutorial-noise-sim.ipynb`
- **Quantum Algorithm Implementations**: A growing collection of known quantum algorithms is included as examples.

---

## Command-Line Interface (CLI)

The project includes an interactive CLI tool, `qsimcli`, to quickly experiment with sequences of quantum operations.

---

Explore the examples, tutorials, and documentation to dive into quantum computing with this powerful Python-based environment!
