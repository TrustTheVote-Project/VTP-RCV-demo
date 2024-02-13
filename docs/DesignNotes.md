# Initial Design Thoughts Regarding the Client/Server VTP Demo Code

## Background

Moving the design notes from [VoteTrackerPlus Discussino](https://github.com/TrustTheVote-Project/VoteTrackerPlus/discussions/51#discussioncomment-4772776) to here.

## Uber Context

A high level description of starting and stopping the demo.  Maybe it works as a starting point for a real polling center, maybe not.

1. Install the VTP software (connected to the internet)
    - pull data and environment
    - this happens at home at not necessarily at the demo location

2. Initialize the polling center/demo hardware (air gapped with the internet):
    - power on the devices (laptop and firewall/router/AP)
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

This part is considered the demo's _design targat_ and not a project plan.  The actual project plan is used to create the [kanban board](https://github.com/orgs/TrustTheVote-Project/projects/5).  See that web page for the action plan.

### Pre-demo steps (occurs during phase 1 above)

- Effectively covers steps 1, 2, and 3 above
- We may want a _test_ endpoint that returns server status - TBD

### First API endpoint (occurs during phase 3 above)

- Phone connects to the VTP demo web server, and the web server requests a ballot-store GUID from VoteTracker+
- VTP backend generates the ballot-store and its GUID and if successful returns the GUID to the web server
- web server returns the ballot-store GUID to the client

Note - since this is a restful based experience, initially there should be a n minute timeout on the backend to clean up defunct GUIDs.  Maybe sometime later a heartbeat or the equivalent can be implemented.

### Second API endpoint (occurs during phase 3 above)

- Given a GUID, phone requests a blank ballot from web server
- web server requests a ballot from VoteTracker+
- VoteTracker+ returns a blank ballot or raises an error
- web server returns a blank ballot

### Third API endpoint (occurs during phase 3 above)

Note - to keep the client side UI implementation simple so to be able to make the necessary milestones, even though the client will get the entire ballot, the client side is _implemented_ at a per contest basis and not really at a per ballot basis.  Specifically, the UI will handle the first contest since by default the backend sends the ballot with the first contest as the default.  Thus:

- UI displays first contest and handles UI input
- may submit a selection for the specified contest while also specifying the next contest
- may solely specify the next contest
- may quit, removing the GUID from the backend, voiding the VTP voting process
- may submit the ballot as is without completing all the contests
  - contests may have undervotes, including no votes

Note - as the contests are submitted, the ballot sent to the client from the backend is less and less blank.  This allows the per contest centric UI to know the default next contest as well as being able to revisit a previous completed, partially completed, or skipped contest.  And know when the ballot is complete.

Note that the python server side will re-validate the incoming ballot CVR.  The entrypoint can return various errors to the client:

- a non compliant contest selection was found
- there was a problem on the server side

If there is no error, this endpoint returns:

- the voter's ballot check
- the voter's row offset into the ballot check

### Fourth API endpoint (occurs during phase 3 above)

- Given an connection ID, will invoke verify-ballot-receipt on the server side backend
- Supports various switches, each switch being a different UX button

Supports calling the backend python script verify-ballot-receipt with various switches. Each different python switch would map (TBD) to a different button.  It is this endpoint which is of high interest regarding the VTP demo as this endpoint basically demonstrates E2EV.  As such we probably want to plan some time optimizing the UX experience for this - the better it is, the more compelling VoteTracker+ will be for the voter.

Regardless, the output is basically in console log format with the digests being converted into real links.

### Fifth API endpoint (occurs during phase 3 above)

- Given an connection ID, will invoke tally-contests on the server side backend
- Supports various switches, each switch being a different UX button

Supports calling the backend python script tally-contests with various switches.  Each different python switch would map (TBD) to a different button.  It is this endpoint which is of high interest to the RCV folks as it is this one where the voter can see how their ranked voted is counted across the rounds of rank choice voting.  As such we probably want to plan some time optimizing the UX experience for this - the better it is, the more compelling RCV should be for the voter.

Regardless, the output is basically in console log format with the digests being converted into real links.

## Other Odds and Ends

1. We decided to allow participants in the demo to vote as many times as they would like so to gain experience with RCV and VTP and to allow multiple people to use one phone.

2. The presenter needs to make certain that people understand that in a real election, the voter's secret number (the row offset) will not be observable by any other person, election official or voter, except in the existing case of accessibility needs where someone else may already have access to the selections depending on the specific election infrastructure.

