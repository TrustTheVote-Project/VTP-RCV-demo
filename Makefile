# Ancient Makefile implicit rule disabler
(%): %
%:: %,v
%:: RCS/%,v
%:: s.%
%:: SCCS/s.%
%.out: %
%.c: %.w %.ch
%.tex: %.w %.ch
%.mk:

# Variables
DOC_DIR     := docs
SRC_DIR     := src/vtp/web/api
TEST_DIR    := tests
BUILD_FILES := pyproject.toml poetry.lock
HOST        := 127.0.0.1
PORT        := 8000

# for uvicorn console logging: [critical|error|warning|info|debug|trace]
VERBOSITY   :=
# when set to non nil, will merge the ballots as they are cast, but this
# ONLY works when sequentially casting ballots in demo/test mode
MERGE_CONTESTS :=

# Use colors for errors and warnings when in an interactive terminal
INTERACTIVE := $(shell test -t 0 && echo 1)
ifdef INTERACTIVE
    RED	:= \033[0;31m
    END	:= \033[0m
else
    RED	:=
    END	:=
endif

ifdef VERBOSITY
    LOG_LEVEL := --log-level ${VERBOSITY}
else
    LOG_LEVEL :=
endif

# Let there be no default target
.PHONY: help
help:
	@echo "${RED}There is no default make target.${END}  Specify one of:"
	@echo "pylint             - runs pylint"
	@echo "pytest             - runs pytest"
	@echo "poetry-build 	  - performs a poetry local install"
	@echo "poetry-list-latest - will show which poetry packages have updates"
	@echo "requirements.txt   - updates the python requirements file"
	@echo "etags              - constructs an emacs tags table"
	@echo "conjoin            - conjoins the VoteTrackerPlus repos via"
	@echo "                     symlinks"
	@echo "run - will run the uvicorn web-api server (main:app) with"
	@echo "      host='${HOST}' for localhost operation only.  Set"
	@echo "      HOST=0.0.0.0 for LAN operation - ${RED}REQUIRES A FIREWALL${END}"
	@echo "      ${RED}FOR SECURITY${END}.  See https://www.uvicorn.org/settings"
	@echo "      for more info."
	@echo ""
	@echo "See ${BUILD_DIR}/README.md for more details and info"

# Run pylint
.PHONY: pylint
pylint:
	@echo "${RED}NOTE - isort and black disagree on 3 files${END} - let black win"
	isort ${SRC_DIR} ${TEST_DIR}
	black ${SRC_DIR} ${TEST_DIR}
	pylint --recursive y ${SRC_DIR} ${TEST_DIR}

.PHONY: poetry-build poetry-list-latest
poetry-build:
	poetry shell && poetry install
poetry-list-latest:
	poetry show -o
# Generate a requirements.txt for dependabot (ignoring the symlinks)
requirements.txt: ${BUILD_FILES}
	poetry export --with dev -f requirements.txt --output requirements.txt

.PHONY: run
run:
	cd src/vtp/web/api && MERGE_CONTESTS=${MERGE_CONTESTS}  uvicorn main:app --host ${HOST} --port ${PORT} ${LOG_LEVEL} --reload-dir ../../../../../VTP-web-client/static --reload-dir . --reload-include "*.py" --reload-include "*.js"

# Connect this repo to the VoteTrackerPlus repo assuming normal layout.
# This allows this repo to run without a VoteTrackerPlus install proper
# and to run out of the connected git repo directly.
.PHONY: conjoin
conjoin:
	ln -s ../../../VoteTrackerPlus/src/vtp/core src/vtp/core
	ln -s ../../../VoteTrackerPlus/src/vtp/ops src/vtp/ops
	ln -s ../../../../../VTP-web-client/static src/vtp/web/api/static

# Run tests
.PHONY: pytest
pytest:
	pytest ${TEST_DIR}

# emacs tags
ETAG_SRCS := $(shell find * -type f -name '*.py' -o -name '*.md' | grep -v defunct)
.PHONY: etags
etags: ${ETAG_SRCS}
	etags ${ETAG_SRCS}
