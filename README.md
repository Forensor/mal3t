# MAL3T
MAL3T (**MA**chine **L**earning **T**ic-**T**ac-**T**oe) is a personal project pointing towards acquiring knowledge in this specific field and other programming languages. It consists in playing tic-tac-toe against a self-improving AI (**T**ic-Tac-Toe **A**rtificial **I**ntelligence) that stores the moves it makes (wether it leads to win or lose) to choose the best decision.

### INFO
This program uses sqlite3 to store the moves TAI keeps doing. You can choose to play cross, nought or let TAI learn by itself. To move you'll have to write the coordinates where you want to place your shape:

<p align="center"><img src="https://github.com/Forensor/mal3t/blob/master/img/coords.png"></p>
For instance, if you write 'a1', the shape will be placed in the inferior left corner. All games are stored in a database with a pgn format. This means if a game has a pgn stored like 'b2a3b3b1' would look like this:
<p align="center"><img src="https://github.com/Forensor/mal3t/blob/master/img/samplegame.png"></p>

### HOW DOES IT GET THE BEST MOVE?
Once a position is given, TAI looks for all possible moves in that state. Then, for each one of them it queries the database to see if that movement would lead to win, to lose or the result is unknown. For example given the position 'b2a3b3b1c3a1c1', TAI would query for possible moves in the database like this:
<p align="center"><img src="https://i.imgur.com/Gi8lpno.png"></p>
So the move chosen will be 'a2'.
