SHELL := /bin/bash

start:
	python pscript.py

test:
	python pscript.py scripts/t02.txt

token:
	python pscript.py -t

full:
	python pscript.py scripts/t02.txt -t
