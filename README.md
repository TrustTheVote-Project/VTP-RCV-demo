# VoteTrackerPlus Web API

A FastAPI interface to the VoteTrackerPlus (VTP) backend, to support a live participatory demo in the spring of 2023.

## Useful Links

The general layout and relationship of the various VTP repos is described in the [VTP-dev-env](https://github.com/TrustTheVote-Project/VTP-dev-env) repository - see the README there first.

See the [VoteTrackerPlus](https://github.com/TrustTheVote-Project/VoteTrackerPlus) repository for general VTP design and project information - that repo is the primary VTP repo.

See the [developer readme](https://github.com/TrustTheVote-Project/VoteTrackerPlus/tree/main/src/vtp) in the VoteTrackerPlus repo for even more details.

- For an overview of the demo project, check out [the project mind map](https://www.mindmeister.com/map/2534840002?t=2nMk3h9Uha).
- This repo also includes web-api [Design Notes](docs/DesignNotes.md).
- The API endpoints in this project are a web interface to the [VoteTrackerPlus backend](https://github.com/TrustTheVote-Project/VoteTrackerPlus).

## Installation

This Python project uses [poetry](https://python-poetry.org/) for dependency and package management. To run the code in this repo, first [install poetry](https://python-poetry.org/docs/#installation) on your development workstation. Then,

See the [VTP-dev-env](https://github.com/TrustTheVote-Project/VTP-dev-env) for a general overview of VoteTrackerPlus software development.  Clone the VTP-dev-env repo to clone this one.

See the [VTP development readme](https://github.com/TrustTheVote-Project/VoteTrackerPlus/tree/main/src/vtp) section 4 for one time steps to set up poetry and a python development environment.  Note that this repo and the the VoteTrackerPlus repo have their own and separate python development environments - each repo has their own and separate pyproject.toml file.

With poetry properly installed on your system:

```bash
$ poetry install
$ poetry shell
```

This project requires Python 3.10 or later.

## Run the API server

Once the installation is complete, the top level Makefile wraps starting the uvicorn server.  Note that nominally the python backend needs to be instantiated.  The backend tabulation server does not need to be running for the web-api to fully function.

The below assumes that the VTP-dev-env has been cloned and used to create this repo.

```bash
$ make help
$ make conjoin
$ make run
```

If the poetry shell is active, you should see some output that looks like this:

```bash
➤ uvicorn main:app
INFO:     Started server process [288056]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

## Testing the API endpoints in your browser

To test the API endpoints using the uvicorn server, go to the URL specified in the above output in your favorite browser. You'll see the version information for this API server.

To include the python backend, in another terminal window configure the VoteTrackerPlus repo and perform a local installation of the ElectionData repo.  See the [README](https://github.com/TrustTheVote-Project/VoteTrackerPlus) for more info.

With the uvicorn server running and with a local installion of a VoteTrackerPlus election, which is nominally installed in /opt/VoteTrackerPlus/demo.01 by default, one should be able to connect to the index.html page of the uvicorn server and vote, get a ballot receipt, verify the receipt, inspect contest CVRs, and tally contests.
