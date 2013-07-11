bootstrap:
	pip install -r requirements.txt

test:
	nosetests test/TestPlugin_runner.py

.PHONY: bootstrap test