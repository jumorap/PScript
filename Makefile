SHELL := /bin/bash

start:
	python pscript.py

test:
	python pscript.py scripts/t02.txt
	python pscript.py scripts/s001.txt
	python pscript.py scripts/s002.txt
	python pscript.py scripts/s003.txt
	python pscript.py scripts/s004.txt
	python pscript.py scripts/s005.txt
	python pscript.py scripts/s006.txt
	python pscript.py scripts/gen_list_rands_plot.txt
	python pscript.py scripts/print_rands.txt
	echo "All tests passed"

token:
	python pscript.py -t

full:
	python pscript.py scripts/t02.txt -t
