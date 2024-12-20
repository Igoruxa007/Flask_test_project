style:
	flake8 ./webapp

types:
	mypy ./webapp

test:
	python -m unittest -v tests.tests

check:
	make -j3 style types tests
