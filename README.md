# Welcome to the jungle
### _We've got code and games_

Code for ball-in-play project using StatsBomb open data. Data and guides can be found in StatsBomb's repo: https://github.com/statsbomb/open-data/. Details of the `statsbombpy` package can be found here: https://github.com/statsbomb/statsbombpy

## Intro
This repo contains four _main_ things to know about.
1) `calculate_match_timings.py` file: contains the function to calculate ball-in-play time from a StatsBomb match events dataframe. A brief explanation on the method will be written just below.
2) `utils` folder: contains assorted helpful files
3) `create_analysis.py` file: implements the functions. It features a long list of commented-out lines for producing the files used in the newsletter post.
4) `summary_analysis.py` file: pulls together the match-by-match statistics produced in `create_analysis.py` to produce a summary dataframe for each sample.

For the match ID list for the StatsBomb Icons series, see `utils/constants.py`.

## Methodology
_Statsbomb open event data documentation: https://github.com/statsbomb/open-data/blob/master/doc/Open%20Data%20Events%20v4.0.0.pdf_

The `calculation.md` file contains some rough notes as a starting point for the project, but quite quickly I realised that the best approach was probably based around finding 'restart' events. 

There are only a limited number of ways that play can be (re)started in a football match:
- Kick-off
- Goal kick
- Throw-in
- Free kick
- Corner kick
- Penalty
- Referee dropping the ball for a restart

These are much easier to find in event data than the ways that the ball can go out of play/otherwise dead in a football match (e.g. playing carrying/dribbling/miscontrolling/clearing the ball out of play). If you find the 'restart' events, and remove events which can take place during stoppages*, then you simply have to look back at the time that the prior event took place and you have your 'out of play' time.

*Substitutions are the main example, but as another StatsBomb have an event called 'Bad Behaviour' for cards given to players "due to an infringement outside of play", which could presumably mean during a break in play.

The 'restart time' is found by looking at the difference between the time (in seconds) between a 'restart event' and the event that took place before it (once the 'break in play' events have been removed). A match's total duration is found by searching for the (very convenient) 'Half End' events in the data and adding the maximum value for each period (each team receives a 'Half End' event, and the clock starts at zero for each period).

## Utils
`constants`: contains the list of competition and season ID combinations for the StatsBomb Icons series as well as the list of event types which could happen during breaks of play.

`debugging`: during the work on the project there were matches whose data I wanted to check. This file contains a function which takes a StatsBomb match ID and returns a dataframe of match events, limited to some basic information around event type, team, match time, and restart status. This is useful if a match's data looks unusual in some way.

`find_save_match_ids`: contains a function that can take a list of competition and season ID combination and save a list of match IDs in a single-column csv file, for iterating through the main `calculate_statsbomb_match_timings` function. The function is set up to save to a named csv in the `data` folder, but it would be trivial to add an argument in the function to save to a provided filename/space. At the bottom of the file are two commented-out lines which implement the function on an outdated set of competition and season IDs, an approach to gathering the StatsBomb Icons matches before realising that StatsBomb's articles provide the relevant match IDs. 
