#!/bin/bash

select=${1:-all}

if [ $select == "all" ] || [ $select == "qusimulator" ]; then
	pushd qusimulator
	pip install .
	rm -r build
	rm -r qusimulator.egg-info
	rm -r __pycache__
	popd
	echo '-----------------------------------------------------'
fi

if [ $select == "all" ] || [ $select == "qucircuit" ]; then
	pushd qucircuit
	pip install .
	rm -r build
	rm -r qucircuit.egg-info
	rm -r __pycache__
	popd
	echo '-----------------------------------------------------'
fi
