style:
	flake8 ./webapp

type:
	mypy ./webapp

test:
	python -m unittest -v tests.user_model_test

check:
	make -j3 style type test
