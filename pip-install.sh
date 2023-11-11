#!/bin/bash

select=${1:-all}

if [ $select == "all" ] || [ $select == "qsim" ]; then
	pushd qsimulator
	pip uninstall -y qsim
	pip install .
	rm -r build
	rm -r qsim.egg-info
	rm -r __pycache__
	popd
	echo '-----------------------------------------------------'
fi

if [ $select == "all" ] || [ $select == "qckt" ]; then
	pushd qcircuit
	pip uninstall -y qckt
	pip install .
	rm -r build
	rm -r qckt.egg-info
	rm -r __pycache__
	popd
	echo '-----------------------------------------------------'
fi
