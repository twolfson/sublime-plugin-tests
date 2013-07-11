bootstrap:
	pip install -r requirements.txt

test:
	nosetests test/*.py

.PHONY: bootstrap test