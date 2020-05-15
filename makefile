init:
	pip install -r requirements.txt

test:
	pytest

run:
	chmod +x run.sh
	./run.sh
