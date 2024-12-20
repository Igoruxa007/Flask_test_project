style:
	flake8 ./webapp

types:
	mypy ./webapp

test:
	python -m unittest -v tests.test_user_model

check:
	make -j3 style types tests
