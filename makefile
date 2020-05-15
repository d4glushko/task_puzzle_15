init:
	pip install -r requirements.txt

test:
	pytest

coverage:
	coverage run -m pytest
	coverage report

run:
	chmod +x run.sh
	./run.sh
