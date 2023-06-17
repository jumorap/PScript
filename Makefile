SHELL := /bin/bash

start:
	python pscript.py

test:
	python pscript.py scripts/array_plot.psc
	python pscript.py scripts/print_exporands.psc
	python pscript.py scripts/arrays_in_arrays.psc
	python pscript.py scripts/while_bucle.psc
	python pscript.py scripts/function_while_bucle.psc
	python pscript.py scripts/exporand_array_history.psc
	python pscript.py scripts/exporand_bucle.psc
	python pscript.py scripts/gen_list_rands_plot.psc
	python pscript.py scripts/print_rands.psc
	python pscript.py scripts/default_error_manage.psc
	python pscript.py scripts/update_values.psc
	echo "All tests passed"

token:
	python pscript.py -t

full:
	python pscript.py scripts/s006.psc -t
