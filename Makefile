.PHONY: docs docker-build docker-run clean

docs:
	cd docs && sphinx-apidoc -f -o source ../src
	cd docs && sphinx-build -M html source build

docker-build:
	docker build -t repro-project .

docker-run:
	docker run --rm \
		-v "$(PWD)/output:/app/output" \
		repro-project

clean:
	rm -rf docs/build
