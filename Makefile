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

# Use colors for errors and warnings when in an interactive terminal
INTERACTIVE := $(shell test -t 0 && echo 1)
ifdef INTERACTIVE
    RED	:= \033[0;31m
    END	:= \033[0m
else
    RED	:=
    END	:=
endif

# Let there be no default target
.PHONY: default
default:
	@echo "${RED}There is no default make target.${END}  Specify one of:"
	@echo "pylint    - runs pylint"
	@echo "pytest    - runs pytest"
	@echo "reqs      - generates a new requirements.txt file"
	@echo "etags     - constructs an emacs tags table"
	@echo "conjoin   - conjoins the VoteTrackerPlus repo via symlinks"
	@echo ""
	@echo "See ${BUILD_DIR}/README.md for more details and info"

# Run pylint
.PHONY: pylint
pylint:
	@echo "${RED}NOTE - isort and black disagree on 3 files${END} - let black win"
	isort ${SRC_DIR} ${TEST_DIR}
	black ${SRC_DIR} ${TEST_DIR}
	pylint --recursive y ${SRC_DIR} ${TEST_DIR}

# Connect this repo to the VoteTrackerPlus repo assuming normal layout.
# This allows this repo to run without a VoteTrackerPlus install proper
# and to run out of the connected git repo directly.
.PHONY: conjoin
conjoin:
	ln -s ../../../VoteTrackerPlus/src/vtp/core src/vtp/core
	ln -s ../../../VoteTrackerPlus/src/vtp/ops src/vtp/ops

# Run tests
.PHONY: pytest
pytest:
	pytest ${TEST_DIR}

# emacs tags
ETAG_SRCS := $(shell find * -type f -name '*.py' -o -name '*.md' | grep -v defunct)
.PHONY: etags
etags: ${ETAG_SRCS}
	etags ${ETAG_SRCS}

# Generate a requirements.txt for dependabot (ignoring the symlinks)
.PHONY: reqs
reqs requirements.txt: pyproject.toml poetry.lock
	poetry export --with dev -f requirements.txt --output requirements.txt
