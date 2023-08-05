# synthSportPlayer Package

Last updated - 11/3/2021

The purpose of the code within this package is to simulate sports players/teams that compete against each other in both classic 1v1 elimination tournaments and round robin tournaments. Originally the classes & code were created in support of another project but grew larger than expected and therefore large enough to become it own package.
At this point in time it is planned that the code shall continue to be developed.

For the project homepage and issue tracking please see [the github repo.](https://github.com/DrJStrudwick/Synthetic-Sport-Player)

For documentation please see [the docs.](https://synthetic-sport-player.readthedocs.io/en/latest/index.html)

# Install & import
Install the project by running:
```
pip install synthSportPlayer-DJS
```
and import with:
```
import synthSportPlayer
```

There are 5 primary classes contained within this package:
1. `player` These are the teams/players that do the competeing. They are simply defined by a 'skill' level and a variance and whenever they have to 'compete' that is created from a normal distribution defined by these two properties.
2. `match` This is a match to handle two player competing where one will win and one will lose. The winner is determine by both players performing and the highest value wins. If they are equal then the winner is chosen randomly.
3. `tournament` This is an event that a collection of players enter and compete pair-wise with the winners moving forward to the next round, and is complete when there is one player remaining.
4. `robin` This is an event that a collection of players enter where every player will compete against every other player and recieve points for how many wins they had.
5. `season` This is a collection of tournaments that are played in order. At the end of the tournament the players recieve point based on how far they got in that tournament.

There are three extra child classes that were written. The first two extend both `tournament` and `season` to be able to have 'real-time' functionality for dashboarding purposes. The third is to facilitate byes in tournaments. They are:
1. `liveTourn`
2. `liveSeason`
3. `bye`

The main difference with `liveTourn` and `liveSeason` is their respective `playTourn` and `playSeason` function. In the parent classes the functions would run to completion of the tournament/season. In these child classes they move forward one step in the current tournament.
