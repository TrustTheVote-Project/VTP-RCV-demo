# Initial Design Thoughts Regarding the Client/Server VTP Demo Code

## 1) Background

Moving the design notes from [VoteTrackerPlus Discussino](https://github.com/TrustTheVote-Project/VoteTrackerPlus/discussions/51#discussioncomment-4772776) to here.

## 2) Uber Context

A high level description of starting and stopping the demo.  Maybe it works as a starting point for a real polling center, maybe not.

1. Install the VTP software (connected to the internet)
    - pull data and environment

2. Initialize the polling center/demo hardware (air gapped with the internet):
    - run a setup-vtp-demo from scratch into a new directory location
    - start the web server with client connections denied
    - test the web server

3. Open the polls
    - Allow client connections to proceed

4. Close the polls
    - prohibit new client connections

5. Shutdown the polls 
    - shut down all client connections
    - flush all pending CVR merges
    - report on client connection statistics

6. shutdown the polling center
    - stop the server
    - log some demo data

7. Upload/aggregate results with other precincts (connected to the internet)
    - push the election data back up

## Client/Server Endpoint Details

### A. Pre-demo steps (occurs during phase 1 above)

- Effectively covers steps 1, 2, and 3 above

### B. First API endpoint (occurs during phase 3 above)

- Phone connects to web server and requests a unique connection ID
- Returns a unique connection ID

### C. Second API endpoint (occurs during phase 3 above)

- Given a unique connection ID, phone requests a ballot
- Returns a ballot

### D. Third API endpoint (occurs during phase 3 above)

Given a unique connection ID, this endpoint will upload a ballot.  During the 2023/02/02 meeting, after a detailed 3-way discussion we decided that the JS client would validate the voter's contest ballot choices for proper ballot compliance.  The demo election data file (EDF), which is native VTP election data, contains the rules that defines a valid selection for each contest.  The NIST standard also defines this but appears (TBD) to not enforce compliance in that NIST allows (TBD) an election definition file to be incorrectly/incompletely defined by election officials.

Though this is not true with native VTP election data, regardless VTP supports an automatic CI pipeline which includes testing.  The goal is that with tests, human error in election data file definitions regarding valid contest selection will be caught prior to an election.

We also decided that the JS client would also support voter self adjudication of all the contests.  Self adjudication occurs when the voter has a chance to validate their contest selections prior to officially submitting their ballot.  Therefor, the JS client at a high level workflow would look like the following:

- Loop over each contest and:
    - present the contest to the voter
    - the voter makes their selection
    - JS verifies that the selection is EDF compliant
- Present to the user the effective selection summary of the ballot sans ballot verbiage.  This is effectively a pretty print of the ballot CVR via an aggregation of each contest CVR.
- Require the voter to accept the selection summary
- If yes, JS will call the third API endpoint
- If no, JS will either restart the loop or jump to a specific contest for a new voter selection

Note that the python server side will re-validate the incoming ballot CVR.  The entrypoint can return various errors to the client:

- a non compliant contest selection was found
- there was a problem on the server side

If there is no error, this endpoint returns:

- the voter's ballot check
- the voter's row offset into the ballot check

### E. Fourth API endpoint (occurs during phase 3 above)

- Given an connection ID, will invoke verify-ballot-receipt on the server side backend
- Supports various switches, each switch being a different UX button

Supports calling the python script verify-ballot-receipt with various switches. Each different python switch would map to a different button.  It is this endpoint which is of high interest regarding the VTP demo as this endpoint basically demonstrates E2EV.  As such we probably want to plan some time optimizing the UX experience for this - the better it is, the more compelling VoteTracker+ will be for the voter.
also requires a connection ID

### F. Fifth API endpoint (occurs during phase 3 above)

- Given an connection ID, will invoke tally-contests on the server side backend
- Supports various switches, each switch being a different UX button

Supports calling the python script tally-contests with various switches.  Each different python switch might map to a different button.  It is this endpoint which is of high interest to the RCV folks as it is this one where the voter can see how their ranked voted is counted across the rounds of rank choice voting.  As such we probably want to plan some time optimizing the UX experience for this - the better it is, the more compelling RCV should be for the voter.

## Other Odds and Ends

1. We decided to allow participants in the demo to vote as many times as they would like so to gain experience with RCV and VTP and to allow multiple people to use one phone.  This might be a bad decision - in retro spec it seems like it.  It may be that we want to minimize the number of things that can confuse the voter (even though in real life they will not be voting by phone).  Regardless, to prevent multiple votes the solution would need to work across multiple browsers.

2. The presenter needs to make certain that people understand that in a real election, the voter's secret number (the row offset) will not be observable by any other person, election official or voter, except in the existing case of accessibility needs where someone else may already have access to the selections depending on the specific election infrastructure.

