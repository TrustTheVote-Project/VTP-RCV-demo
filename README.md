# VoteTrackerPlus Web API

A FastAPI interface to the VoteTrackerPlus (VTP) backend, to support a live participatory demo in the spring of 2023.

## Useful Links

- For an overview of the demo project, check out [the project mind map](https://www.mindmeister.com/map/2534840002?t=2nMk3h9Uha).
- This repo also includes the official [Design Notes](docs/DesignNotes.md).
- The API endpoints in this project are a web interface to the [VoteTrackerPlus backend](https://github.com/TrustTheVote-Project/VoteTrackerPlus).

## Installation

This Python project uses [poetry](https://python-poetry.org/) for dependency and package management. To run the code in this repo, first [install poetry](https://python-poetry.org/docs/#installation) on your development workstation. Then,

1. Clone or copy the code to a directory where you keep your GitHub repositories.
2. Enter the `VTP-web-api` directory you just created, like this: `cd ~/repos/VTP-web-api`
3. To install the required Python packages, run `poetry install`
4. To use the new virtual environment you just created, and run the API server & tests (see below for details), run `poetry shell`

Note: if you want to use a certain Python version, you can tell poetry, like this:

```bash
poetry env use 3.9
```

This command will set up a virtual environment using Python 3.9. Note that the specified Python version must already be installed on your computer.

This project requires Python 3.9 or later.

## Run the API server

1. Once the installation is complete, go to the source code directory: `cd src/vtp/web/api`
2. Run the `uvicorn` server like this: `uvicorn main:api`

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

## Testing the API endpoints in your browser

Here are some examples of the API endpoints you can access when the uvicorn server is running. For the latest list of API endpoints, please review the code in `main.py`.

### Request a Voter ID

To request an empty ballot, the web client first needs to receive a VoteStoreID. This indicates that the VTP backend has created a git repository to store the voter's cast ballot. The VoteStoreID matches the voter with their vote store repository.

To request a VoteStoreID, go to this endpoint: `http://127.0.0.1:8000/vote/`

You'll receive a VoteStoreID, like this:

```json
{"VoteStoreID": "206203"}
```

For the next step, copy the VoteStoreID.

### Request a blank ballot

To request a blank ballot, the client needs to provide a valid VoteStoreID. If you've copied the VoteStoreID from the "/vote/" endpoint, you can request a ballot like this:`http://127.0.0.1:8000/vote/206203`

If you provide an ID that doesn't match an existing ID, you'll get an error message back, but if you provide a valid ID, you'll get an empty ballot back from the server in JSON format.

## Testing

If you'd rather not test the API by hand, you can use pytest. Note that you still need an active `poetry shell` environment.

1. Go to the root of the repo, like this: `cd ~/repos/VTP-web-api` -- of course, your path may vary!
2. Run `pytest`
3. To see a table of code coverage, run `pytest --cov-report term-missing --cov=src/`
