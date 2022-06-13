/* 
This implementation of the infamous tic-tac-toe game is based on
https://github.com/Cledersonbc/tic-tac-toe-minimax/. The code is
modified to allow for different levels of difficulty. In particular,
there are three levels:
- Level 1: Computer performs random moves
- Level 2: Computer performs optimal moves with a 0.3 chance of performing
		   a random move
- Level 3: Computer performs optimal moves only (unbeatable)
*/


/*Code of Minmax here*/
var board = [
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
];

var HUMAN = -1;
var COMP = +1;

var difficulty = 1;

/* Function to heuristic evaluation of state. */
function evalute(state) {
	var score = 0;

	if (gameOver(state, COMP)) {
		score = +1;
	}
	else if (gameOver(state, HUMAN)) {
		score = -1;
	} else {
		score = 0;
	}

	return score;
}

/* This function tests if a specific player wins */
function gameOver(state, player) {
	var win_state = [
		[state[0][0], state[0][1], state[0][2]],
		[state[1][0], state[1][1], state[1][2]],
		[state[2][0], state[2][1], state[2][2]],
		[state[0][0], state[1][0], state[2][0]],
		[state[0][1], state[1][1], state[2][1]],
		[state[0][2], state[1][2], state[2][2]],
		[state[0][0], state[1][1], state[2][2]],
		[state[2][0], state[1][1], state[0][2]],
	];

	for (var i = 0; i < 8; i++) {
		var line = win_state[i];
		var filled = 0;
		for (var j = 0; j < 3; j++) {
			if (line[j] == player)
				filled++;
		}
		if (filled == 3)
			return true;
	}

	return false;
}

/* This function test if the human or computer wins */
function gameOverAll(state) {
	return gameOver(state, HUMAN) || gameOver(state, COMP);
}

function emptyCells(state) {
	var cells = [];
	for (var x = 0; x < 3; x++) {
		for (var y = 0; y < 3; y++) {
			if (state[x][y] == 0)
				cells.push([x, y]);
		}
	}

	return cells;
}

/* A move is valid if the chosen cell is empty */
function validMove(x, y) {
	try {
		if (board[x][y] == 0) {
			return true;
		}
		else {
			return false;
		}
	} catch (e) {
		return false;
	}
}

/* Set the move on board, if the coordinates are valid */
function setMove(x, y, player) {
	if (validMove(x, y)) {
		board[x][y] = player;
		return true;
	}
	else {
		return false;
	}
}

/* *** AI function that choice the best move *** */
// Read more on https://github.com/Cledersonbc/tic-tac-toe-minimax/
function minimax(state, depth, player) {
	var best;

	if (player == COMP) {
		best = [-1, -1, -1000];
	}
	else {
		best = [-1, -1, +1000];
	}

	if (depth == 0 || gameOverAll(state)) {
		var score = evalute(state);
		return [-1, -1, score];
	}

	emptyCells(state).forEach(function (cell) {
		var x = cell[0];
		var y = cell[1];
		state[x][y] = player;
		var score = minimax(state, depth - 1, -player);
		state[x][y] = 0;
		score[0] = x;
		score[1] = y;

		if (player == COMP) {
			if (score[2] > best[2])
				best = score;
		}
		else {
			if (score[2] < best[2])
				best = score;
		}
	});

	return best;
}

/* It calls the minimax function */
function aiTurn() {
	var x, y;
	var move;
	var cell;

	var emptycells = emptyCells(board);
	if (emptycells.length == 9) {
		xy = emptycells[parseInt(Math.random() * emptycells.length)]
		x = xy[0]
		y = xy[1]
	} else if (difficulty == 1 && emptycells.length > 0) {
		xy = emptycells[parseInt(Math.random() * emptycells.length)]
		x = xy[0]
		y = xy[1]
	} else if (difficulty == 2 && Math.random() > 0.85 && emptycells.length > 0) {
		xy = emptycells[parseInt(Math.random() * emptycells.length)]
		x = xy[0]
		y = xy[1]
	}
	else {
		move = minimax(board, emptyCells(board).length, COMP);
		x = move[0];
		y = move[1];
	}

	if (setMove(x, y, COMP)) {
		cell = document.getElementById(String(x) + String(y));
		cell.innerHTML = "O";
	}
}

/* main */
function clickedCell(cell) {
	var button = document.getElementById("bnt-restart");
	button.disabled = true;
	var conditionToContinue = gameOverAll(board) == false && emptyCells(board).length > 0;

	if (conditionToContinue == true) {
		var x = cell.id.split("")[0];
		var y = cell.id.split("")[1];
		var move = setMove(x, y, HUMAN);
		if (move == true) {
			cell.innerHTML = "X";
			if (gameOverAll(board) == false && emptyCells(board).length > 0)
				aiTurn();
		}
	}
	if (gameOver(board, COMP)) {
		var lines;
		var cell;
		var msg;

		if (board[0][0] == 1 && board[0][1] == 1 && board[0][2] == 1)
			lines = [[0, 0], [0, 1], [0, 2]];
		else if (board[1][0] == 1 && board[1][1] == 1 && board[1][2] == 1)
			lines = [[1, 0], [1, 1], [1, 2]];
		else if (board[2][0] == 1 && board[2][1] == 1 && board[2][2] == 1)
			lines = [[2, 0], [2, 1], [2, 2]];
		else if (board[0][0] == 1 && board[1][0] == 1 && board[2][0] == 1)
			lines = [[0, 0], [1, 0], [2, 0]];
		else if (board[0][1] == 1 && board[1][1] == 1 && board[2][1] == 1)
			lines = [[0, 1], [1, 1], [2, 1]];
		else if (board[0][2] == 1 && board[1][2] == 1 && board[2][2] == 1)
			lines = [[0, 2], [1, 2], [2, 2]];
		else if (board[0][0] == 1 && board[1][1] == 1 && board[2][2] == 1)
			lines = [[0, 0], [1, 1], [2, 2]];
		else if (board[2][0] == 1 && board[1][1] == 1 && board[0][2] == 1)
			lines = [[2, 0], [1, 1], [0, 2]];

		for (var i = 0; i < lines.length; i++) {
			cell = document.getElementById(String(lines[i][0]) + String(lines[i][1]));
			cell.style.color = "red";
		}

		msg = document.getElementById("message");
		msg.innerHTML = "You lose!";
	}

	if (gameOver(board, HUMAN)) {
		var lines;
		var cell;
		var msg;

		if (board[0][0] == -1 && board[0][1] == -1 && board[0][2] == -1)
			lines = [[0, 0], [0, 1], [0, 2]];
		else if (board[1][0] == -1 && board[1][1] == -1 && board[1][2] == -1)
			lines = [[1, 0], [1, 1], [1, 2]];
		else if (board[2][0] == -1 && board[2][1] == -1 && board[2][2] == -1)
			lines = [[2, 0], [2, 1], [2, 2]];
		else if (board[0][0] == -1 && board[1][0] == -1 && board[2][0] == -1)
			lines = [[0, 0], [1, 0], [2, 0]];
		else if (board[0][1] == -1 && board[1][1] == -1 && board[2][1] == -1)
			lines = [[0, 1], [1, 1], [2, 1]];
		else if (board[0][2] == -1 && board[1][2] == -1 && board[2][2] == -1)
			lines = [[0, 2], [1, 2], [2, 2]];
		else if (board[0][0] == -1 && board[1][1] == -1 && board[2][2] == -1)
			lines = [[0, 0], [1, 1], [2, 2]];
		else if (board[2][0] == -1 && board[1][1] == -1 && board[0][2] == -1)
			lines = [[2, 0], [1, 1], [0, 2]];

		for (var i = 0; i < lines.length; i++) {
			cell = document.getElementById(String(lines[i][0]) + String(lines[i][1]));
			cell.style.color = "green";
		}

		msg = document.getElementById("message");
		msg.innerHTML = "You win!";
	}

	if (emptyCells(board).length == 0 && !gameOverAll(board)) {
		var msg = document.getElementById("message");
		msg.innerHTML = "Draw!";
	}

	if (gameOverAll(board) == true || emptyCells(board).length == 0) {
		button.value = "Restart";
		button.style = "visibility: block;"
		button.disabled = false;
	}
}

/* Restart the game*/
function restartBnt(button) {
	if (button.value == "Start playing") {
		aiTurn();
		button.disabled = true;
	}
	else if (button.value == "Restart") {
		var htmlBoard;
		var msg;

		for (var x = 0; x < 3; x++) {
			for (var y = 0; y < 3; y++) {
				board[x][y] = 0;
				htmlBoard = document.getElementById(String(x) + String(y));
				htmlBoard.style.color = "#444";
				htmlBoard.innerHTML = "";
			}
		}
		msg = document.getElementById("message");
		msg.innerHTML = "";
	}
}

/* Change Level*/
function changeLevel(button) {
	if (button.value == "Level1") {
		button.classList.add("active");
		document.getElementById("btn-level2").classList.remove("active");
		document.getElementById("btn-level3").classList.remove("active");
		difficulty = 1;
	} else if (button.value == "Level2") {
		button.classList.add("active");
		document.getElementById("btn-level1").classList.remove("active");
		document.getElementById("btn-level3").classList.remove("active");
		difficulty = 2;
	}
	else {
		button.classList.add("active");
		document.getElementById("btn-level1").classList.remove("active");
		document.getElementById("btn-level2").classList.remove("active");
		difficulty = 3;
	}
}
