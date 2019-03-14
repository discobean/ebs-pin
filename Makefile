python3:
	python setup.py sdist

upload: python3
	twine upload dist/*
