# VoteTrackerPlus Web API

A FastAPI interface to the VoteTrackerPlus (VTP) backend, to support a live participatory demo in the spring of 2023.

## Useful Links

- For an overview of the demo project, check out [the project mind map](https://www.mindmeister.com/map/2534840002?t=2nMk3h9Uha).
- This repo also includes the official [Design Notes](docs/DesignNotes.md).
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

1. Once the installation is complete, go to the source code directory: `cd src/vtp/web/api`
2. Run the `uvicorn` server like this: `uvicorn main:app`

If the poetry shell is active (see **Installation** above for details), you should see some output that looks like this:

```bash
➤ uvicorn main:app
INFO:     Started server process [288056]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

To test the API endpoints using the uvicorn server, go to the URL specified in your favorite browser. You'll see the version information for this API server.

Note that you can specify the IP address and port number you want the uvicorn server to use, but we're going to use the defaults here (<http://127.0.0.1:8000>).

If you want to update the code that controls the API endpoints, and see the changes on the uvicorn server as soon as you save your code, add the `--reload` switch, like this:

```bash
uvicorn main:app --reload
```

## Testing the API endpoints in your browser

Here are some examples of the API endpoints you can access when the uvicorn server is running. For the latest list of API endpoints, please review the code in `main.py`.

### Manual System Testing of VoteTrackerPlus

To perform manual end-to-end system testing of VoteTrackerPlus with a specific ElectionData (current default is VTP-mock-election.US.16), the backend needs to be installed on the same server as the uvicorn server:

```bash
# In a different shell so to be able to have a different poetry environment:
$ cd VoteTrackerPlus
$ poetry shell
$ cd ../VTP-mock-election.US.16
$ setup-vtp-demo
```

With the uvicorn server running and with a local installion of a VoteTrackerPlus election, which is nominally installed in /opt/VoteTrackerPlus/demo.01 by default, one should be able to connect to the index.html page of the uvicorn server and vote, get a ballot receipt, verify the receipt, inspect contest CVRs, and tally contests.
