SHELL := /bin/bash

start:
	py pscript.py

test:
	py pscript.py scripts/t02.txt

token:
	py pscript.py -t

full:
	py pscript.py scripts/t02.txt -t
