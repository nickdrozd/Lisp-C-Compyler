.PHONY : all header lint

all :

header :
	python3 compyler/header.py

lint :
	pylint compyler
