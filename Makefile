SHELL := /bin/bash

start:
	python pscript.py

test:
	python pscript.py scripts/s001.psc
	python pscript.py scripts/s002.psc
	python pscript.py scripts/s003.psc
	python pscript.py scripts/s004.psc
	python pscript.py scripts/s005.psc
	python pscript.py scripts/s006.psc
	python pscript.py scripts/gen_list_rands_plot.psc
	python pscript.py scripts/print_rands.psc
	python pscript.py scripts/default_error_manage.psc
	python pscript.py scripts/update_values.psc
	echo "All tests passed"

token:
	python pscript.py -t

full:
	python pscript.py scripts/s006.psc -t
