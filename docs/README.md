# Initial stub at an overview for the client/server side VTP demo code

## Background

TBD

### Pre-demo steps
This occurs with the demo laptop connected to the internet and having GitHub access etc
From within the chosen VTP poetry python environment AND chosen mock demo git repo (and git submodules), run setup-vtp-demo
setup-vtp-demo can do what it does now (it currently creates 4 scanner repos/workspaces and that is ok for now)
Initialize the demo on-site - assumes no internet connection

this happens at the fair
start the web server
test the web server

### First API endpoint

phone connects to web server and requests a unique connection ID
returns a unique connection ID

### Second API endpoint

given a unique connection ID, phone requests a ballot
returns a ballot

### Third API endpoint

given a unique connection ID, uploads a ballot
We decided for the moment that the (JS) client side will validate the contest selections and directly support voter self-adjudication of the ballot. The VTP python code currently also supports this. However, the data that the VTP python code returns to the client via endpoint 3 contains the information necessary for the client side (JS) to directly self adjudication. Another solution is to create another endpoint that manages the self adjudication of the ballot so that no JS needs to be written/debugged/tested to support this. In hindsight, I think I now vote for an additional endpoint to use the existing python self adjudication code.
Question - is it ok for the VTP python code to continue to validate the completed ballot and to throw an exception back to the client side if the completed ballot is non-compliant post JS self-adjudication?

### Fourth API endpoint

supports calling the python script verify-ballot-receipt with various switches. Each different python switch would map to a different button
it is this endpoint which is of high interest regarding the VTP demo. This is the endpoint that basically demonstrates E2EV. As such we probably want to plan some time optimizing the UX experience for this - the better it is, the more compelling VoteTracker+ will be for the voter.
also requires a connection ID

### Fifth API endpoint

supports calling the python script tally-contests with various switches. Each different python switch might map to a different button
it is this endpoint which is of high interest to the RCV folks as it is this one where the voter can see how their ranked voted is counted across the rounds of rank choice voting. As such we probably want to plan some time optimizing the UX experience for this - the better it is, the more compelling RCV should be for the voter.
Other action items and decisions/observations:

Rename the 'local-remote' git repo in all documentation to the 'tabulation' repo - the name local-remote is confusing.

Maybe finesse two different names for the current VTP scanner app repos/workspaces to either scanner repos/workspaces when talking about voting center VTP deployments and client repos/workspaces when talking about the RCV/VTP demo.

We decided to allow participants in the demo to vote as many times as they would like so to gain experience with RCV and VTP and to allow multiple people to use one phone. This might be a bad decision - in retro spec it seems like it. I think we want as few things as possible to confuse the voter (even though in real life they will not be voting by phone). However, to prevent multiple votes the solution would need to work across multiple browsers - it may be too much work for the demo.

The presenter needs to make certain that people understand that in a real election, the voter's secret number (the row offset) will not be observable by any other person, election official or voter, except in the existing case of accessibility needs where someone else may already have access to the selections depending on the specific election infrastructure.
