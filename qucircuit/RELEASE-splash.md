# Qucircuit – A quantum computing circuits simulator
## Release 2.2

`$ pip install qucircuit`

New feature added for multi-shot readout of the result of the quantum circuit run. The readout occurs automatically at the end of running the circuit. the Job object should be created with shots argument for the number of shots. After running the job on any backend, the Job object allows you to access the counts. Please read Section `class Job` in developer documentation README.md for details.

'Getting started' tutorial Jupyter notebooks, and documentation resources - 
* [Getting started tutorial Jupyter notebook](https://github.com/atulvarshneya/quantum-computing/tree/master/examples/qckt/Getting-started-tutorial.ipynb)
* [Getting started with noise simulation tutorial Jupyter notebook](https://github.com/atulvarshneya/quantum-computing/tree/master/examples/qckt/Getting-started-tutorial-noise-sim.ipynb)
* [Example implementations of various quantum algorithms](https://github.com/atulvarshneya/quantum-computing/tree/master/examples/qckt)
* [Developer documentation](https://github.com/atulvarshneya/quantum-computing/blob/master/qucircuit/README.md)
