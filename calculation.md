_General notes on how to approach calculating ball-in-play time from events_

**Out of play events/qualifiers**
- Foul Committed (as long as advantage not played)
- Foul Won
- Own Goal For
- Half End
- Injury Stoppage
- Offside
- Own Goal Against
- Shield


Or should you just look for the end events, cut out any middle events, then look for the time of the following event

_Or,_ you could look at re-start events and then look backwards
**Start of play events**
- Referee Ball-drop
- Pass (Kick-off, throw-in, free-kick, corner, goal kick)
- Shot (Free-kick, Penalty, corner)



**Mid-break events**
- Camera On* (5)
- Substitution
- Bad Behaviour
- Starting XI
- Tactical Shift

## Ball out
Hat tip to Andy Rowlinson who pointed out to me that StatsBomb events also have an `out` marker, which would speed this process up greatly. Using this, the follow markers would denote something ending:
- 'Out' boolean
- Goal
- Foul
- Injury stoppage
- Offside

With the 'Out' boolean you should be able to calculate things in a similar way - although it turns out that passes don't use this boolean but use the 'Out' outcome instead.

# Timing notes

StatsBomb data appears to start from 0 for the timestamp each half, meaning some addition will be needed to be done based on the time of the Half End events

Also note: The 1979 U20 match had 40-minute halves, don't get freaked out that the timings are different (3888787)