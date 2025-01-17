VERSION = `cat VERSION`
.PHONY: build run daemon test run-local black black-check update-requirements
PORT=6000

build:
	docker build --tag opentopodata:$(VERSION) --file docker/Dockerfile .

build-m1:
	docker build --tag opentopodata:$(VERSION) --file docker/apple-silicon.Dockerfile .

run:
	docker run --rm -it --volume $(shell pwd)/data:/app/data:ro -p $(PORT):5000 opentopodata:$(VERSION) 

CON_NAME=opentopodata 
daemon:
	docker run --name $(CON_NAME) --rm -itd --volume $(shell pwd)/data:/app/data:ro -p $(PORT):5000 opentopodata:$(VERSION) 

stop:
	docker stop $(CON_NAME)

test: build black-check 
	docker run --rm -e DISABLE_MEMCACHE=1 --volume $(shell pwd)/htmlcov:/app/htmlcov opentopodata:$(VERSION) pytest --ignore=data --ignore=scripts --cov=opentopodata --cov-report html

test-m1: build-m1 black-check 
	docker run --rm -e DISABLE_MEMCACHE=1 --volume $(shell pwd)/htmlcov:/app/htmlcov opentopodata:$(VERSION) pytest --ignore=data --ignore=scripts --cov=opentopodata --cov-report html

run-local:
	FLASK_APP=opentopodata/api.py FLASK_DEBUG=1 flask run --port $(PORT)

black:
	black --target-version py37 tests opentopodata

black-check:
	docker run --rm opentopodata:$(VERSION) black --check --target-version py37 tests opentopodata

update-requirements: build
	# pip-compile gets confused if there's already a requirements.txt file, and
	# it can't be deleted without breaking the docker mount. So instead do the
	# compiling in /tmp. Should run test suite afterwards.
	docker run --rm -v $(shell pwd)/requirements.txt:/app/requirements.txt -w /tmp opentopodata:$(VERSION)  /bin/bash -c "cp /app/requirements.in .; pip-compile requirements.in; cp requirements.txt /app/requirements.txt"

