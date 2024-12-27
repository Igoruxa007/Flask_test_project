style:
	flake8 ./webapp

types:
	mypy ./webapp

test:
	python -m unittest -v tests.user_model_test

check:
	make -j3 style test
