#!/bin/bash

pushd qsimulator
pip uninstall -y qsim
pip install .
rm -r build
rm -r qsim.egg-info
rm -r __pycache__
popd
echo '-----------------------------------------------------'

pushd qcircuit
pip uninstall -y qckt
pip install .
rm -r build
rm -r qckt.egg-info
rm -r __pycache__
popd
echo '-----------------------------------------------------'
