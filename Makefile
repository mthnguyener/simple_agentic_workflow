PROJECT=saw

ifeq ($(wildcard docker/.env),)
    $(shell scripts/create_usr_vars.sh)
endif

ifeq (, $(wildcard docker/.env))
        $(shell ln -s ../usr_vars docker/.env)
endif
include usr_vars
export

ifeq ("$(shell uname -s)", "Linux*")
	BROWSER=/usr/bin/firefox
else ifeq ("$(shell uname -s)", "Linux")
	BROWSER=/usr/bin/firefox
else
	BROWSER=open
endif

CONTAINER_PREFIX:=$(USER_NAME)_$(PROJECT)
DOCKER_CMD=docker
DOCKER_COMPOSE_CMD=docker compose
DOCKER_IMAGE=$(shell head -n 1 docker/python.Dockerfile | cut -d ' ' -f 2)
PKG_MANAGER=pip
PROFILE_PY:=""
PROFILE_PROF:=$(notdir $(PROFILE_PY:.py=.prof))
PROFILE_PATH:=profiles/$(PROFILE_PROF)
SRC_DIR=/usr/src/$(PROJECT)
TEX_WORKING_DIR=${SRC_DIR}/${TEX_DIR}
USER:=$(shell echo $${USER%%@*})
USER_ID:=$(shell id -u $(USER))
VERSION=$(shell grep "^__version__" saw/version.py | cut -d '"' -f 2)

.PHONY: docs format-style upgrade-packages

cpp-build:
	@rm -rf build \
		&& mkdir -p build lib \
		&& cd build \
		&& cmake .. \
		&& cmake --build . \
		&& cp lib/*.so* ../lib

deploy: docker-up
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c "pip install build && python3 -m build --wheel && pip uninstall -y build"
	@echo "Tagging version $(VERSION)"
	@git tag -a v$(VERSION) -m "Version $(VERSION)"
	@echo "Wheel file created in the dist/ directory"
	@echo "Enter the following to push this tag to the repository:"
	@echo "git push origin v$(VERSION)"

docker-down:
	@$(DOCKER_COMPOSE_CMD) -f docker/docker-compose.yaml down

docker-images-update:
	@$(DOCKER_CMD) image ls | grep -v REPOSITORY | cut -d ' ' -f 1 | xargs -L1 $(DOCKER_CMD) pull

docker-rebuild: setup.py
	@$(DOCKER_COMPOSE_CMD) -f docker/docker-compose.yaml up -d --build 2>&1 | tee docker/image_build.log

docker-remove-images:
	@read -p "Enter the pattern to match Docker images: " pattern; \
	images=$$(docker images --format "{{.Repository}}:{{.Tag}}" | grep $$pattern); \
	if [ -n "$$images" ]; then \
		echo "Removing images: $$images"; \
		docker rmi $$images; \
	else \
		echo "No images found matching pattern: $$pattern"; \
	fi

docker-up:
	@$(DOCKER_COMPOSE_CMD) -f docker/docker-compose.yaml up -d

docs: docker-up
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c "cd docs && make html"
	@${BROWSER} http://localhost:$(PORT_NGINX) 2>&1 &

docs-first-run-delete: docker-up
	find docs -maxdepth 1 -type f -delete
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"cd docs \
			 && sphinx-quickstart -q \
				-p $(PROJECT) \
				-a "Minh Nguyen" \
				-v $(VERSION) \
				--ext-autodoc \
				--ext-viewcode \
				--makefile \
				--no-batchfile"
	$(DOCKER_COMPOSE_CMD) -f docker/docker-compose.yaml restart nginx
ifeq ("$(shell git remote)", "origin")
	git fetch
	git checkout origin/main -- docs/
else
	$(DOCKER_CMD) container run --rm \
		-v `pwd`:/usr/src/$(PROJECT) \
		-w /usr/src/$(PROJECT)/docs \
		ubuntu \
		/bin/bash -c \
			"sed -i -e 's/# import os/import os/g' conf.py \
			 && sed -i -e 's/# import sys/import sys/g' conf.py \
			 && sed -i \"/# sys.path.insert(0, os.path.abspath('.'))/d\" \
				conf.py \
			 && sed -i -e \"/import sys/a \
				from saw import __version__ \
				\n\nsys.path.insert(0, os.path.abspath('../saw'))\" \
				conf.py \
			 && sed -i -e \"s/version = '0.1.0'/version = __version__/g\" \
				conf.py \
			 && sed -i -e \"s/release = '0.1.0'/release = __version__/g\" \
				conf.py \
			 && sed -i -e \"s/alabaster/sphinx_rtd_theme/g\" \
				conf.py \
			 && sed -i -e 's/[ \t]*$$//g' conf.py \
			 && echo >> conf.py \
			 && sed -i \"/   :caption: Contents:/a \
				\\\\\n   package\" \
				index.rst"
endif

docs-init:
	@rm -rf docs/*
	@$(DOCKER_COMPOSE_CMD) -f docker/docker-compose.yaml  up -d
	@$(DOCKER_CMD) container run --rm -v `pwd`:/usr/src/$(PROJECT) $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"cd /usr/src/$(PROJECT)/docs \
			 && sphinx-quickstart -q \
				-p $(PROJECT) \
				-a "Minh Nguyen" \
				-v $(VERSION) \
				--ext-autodoc \
				--ext-viewcode \
				--makefile \
				--no-batchfile \
			 && cd .. \
			 adduser --system --no-create-home --uid $(USER_ID) --group $(USER) &> /dev/null \
			 chown -R $(USER):$(USER) docs"
	@git fetch
	@git checkout origin/main -- docs/

docs-view: docker-up
	@${BROWSER} http://localhost:$(PORT_NGINX) &

format-style: docker-up
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python yapf -i -p -r --style "pep8" ${SRC_DIR}

getting-started: docs-init
	@mkdir -p cache \
		&& mkdir -p htmlcov \
		&& mkdir -p logs/tests \
		&& mkdir -p profiles \
		&& mkdir -p wheels \
		&& printf "%s\n" \

ipython: docker-up
	$(DOCKER_CMD) container exec -it $(CONTAINER_PREFIX)_python ipython

latexmk: docker-up
	$(DOCKER_CMD) container exec -w $(TEX_WORKING_DIR) $(CONTAINER_PREFIX)_latex \
		/bin/bash -c "latexmk -f -pdf $(TEX_FILE) && latexmk -c"

notebook: docker-up notebook-server
	@printf "%s\n" \
		"" \
		"" \
		"" \
		"####################################################################" \
		"Use this link on the host to access the Jupyter server." \
		""
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"jupyter lab list 2>&1 \
			 | grep -o 'http.*$(PORT_JUPYTER)\S*' \
			 | sed -e 's/\(http:\/\/\).*\(:\)/\1localhost:/' && \
			echo "" && \
	        jupyter lab list 2>&1 \
			 | grep -o 'http.*$(PORT_JUPYTER)\S*' \
			 | sed -e 's/\(http:\/\/\).*\(:\)[0-9]*\/?//'"
	@printf "%s\n" \
		"" \
		"####################################################################"

notebook-delete-checkpoints: docker-up
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		rm -rf `find -L -type d -name .ipynb_checkpoints`

notebook-server: notebook-stop-server
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"jupyter lab \
				--allow-root \
				--no-browser \
				--ServerApp.ip=0.0.0.0 \
				--ServerApp.port=$(PORT_JUPYTER) \
				&"

notebook-stop-server:
	@-$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c "jupyter lab stop $(PORT_JUPYTER)"

package-dependencies: docker-up
	@printf "%s\n" \
		"# ${PROJECT} Version: $(VERSION)" \
		"# From NVIDIA NGC CONTAINER: $(DOCKER_IMAGE)" \
		"#" \
		> requirements.txt
ifeq ("${PKG_MANAGER}", "conda")
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"conda list --export >> requirements.txt \
			 && sed -i -e '/^$(PROJECT)/ s/./# &/' requirements.txt"
else ifeq ("${PKG_MANAGER}", "pip")
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"pip freeze -l --exclude $(PROJECT) >> requirements.txt"
endif

profile: docker-up
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"python -m cProfile -o $(PROFILE_PATH) $(PROFILE_PY)"

snakeviz: docker-up profile snakeviz-server
	@sleep 0.5
	@${BROWSER} http://0.0.0.0:$(PORT_PROFILE)/snakeviz/ &

snakeviz-server: docker-up
	@$(DOCKER_CMD) container exec \
		-w /usr/src/$(PROJECT)/profiles \
		$(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"snakeviz $(PROFILE_PROF) \
				--hostname 0.0.0.0 \
				--port $(PORT_PROFILE) \
				--server &"

test: timestamp := $(shell date +"%Y%m%d_%H%M%S")
test: docker-up format-style
	@$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		sh -c 'py.test $(PROJECT) | tee -a logs/tests/$(timestamp)_log.txt'

test-coverage: test
	@${BROWSER} htmlcov/index.html &

upgrade-packages: docker-up
ifeq ("${PKG_MANAGER}", "pip")
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"pip3 install -U pip \
			 && pip3 freeze | \
				grep -v $(PROJECT) | \
				cut -d = -f 1 > requirements.txt \
			 && pip3 install -U -r requirements.txt \
			 && pip3 freeze > requirements.txt \
			 && sed -i -e '/^-e/d' requirements.txt"
else ifeq ("${PKG_MANAGER}", "conda")
	$(DOCKER_CMD) container exec $(CONTAINER_PREFIX)_python \
		/bin/bash -c \
			"conda update conda \
			 && conda update --all \
			 && pip freeze > requirements.txt \
			 && sed -i -e '/^-e/d' requirements.txt"
endif

