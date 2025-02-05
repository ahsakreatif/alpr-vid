docker-build:
	docker build -t openalpr-python .

docker-run:
	docker run -it --rm openalpr-python bash
