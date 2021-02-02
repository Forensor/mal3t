# MAL3T
MAL3T (**MA**chine **L**earning **T**ic-**T**ac-**T**oe) is a personal project pointing towards acquiring knowledge in machine learning and Python programming language. It consists in playing tic-tac-toe against a self-improving AI (**T**ic-Tac-Toe **A**rtificial **I**ntelligence) that stores the moves it makes (wether it leads to win or lose) to choose the best decision.

### INFO
This program uses sqlite3 to store the moves TAI makes. You can choose to play cross, nought or let TAI learn by itself. To move you'll have to write the coordinates where you want to place your shape:

<p align="center"><img src="https://github.com/Forensor/mal3t/blob/master/img/coords.png"></p>
For instance, if you write 'a1', the shape will be placed in the inferior left corner. All games are stored in a database with a pgn format. This means that a game like: 'b2a3b3b1', would look like this:
<p align="center"><img src="https://github.com/Forensor/mal3t/blob/master/img/samplegame.png"></p>

### HOW DOES IT GET THE BEST MOVE?
Once a position is given, TAI looks for all the possible moves in that state. Then, it queries the database for each one to check if it would lead to win, lose, or an unknown result. If no move leads to a win, the next one will be chosen randomly (excluding losing moves). E.g. given the position: 'b2a3b3b1c3a1c1'; TAI would query for all the possible moves in the database like this:
<p align="center"><img src="https://i.imgur.com/Gi8lpno.png"></p>
So for this case, the chosen move will be 'a2'.
