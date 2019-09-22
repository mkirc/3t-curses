from pprint import pprint
from copy import deepcopy

class MiniMax:

	def __init__(self, board, aiPlayer):

		self.moves = {}
		self.bf = BoardFactory()
		self.initBoard = self.bf.returnBoard(board,	aiPlayer)
		self.initBoard.minimax()
		self.moves = self.initBoard.moves


	def getEmptyFields(self):

		e = []
		for i in [0, 2, 4]:
			for j in [0, 2, 4]:
				if self.initBoard[i][j] == 0:
					e.append((i, j))
		return e

	def playerSwitch(self):

		if self.player == 'X':
			self.player = 'O'
		elif self.player == 'O':
			self.player = 'X'

	def isTermState(self):
		if self.winCondition(self.initBoard, 'X'):
			return 1
		elif self.winCondition(self.initBoard, 'O'):
			return -1
		elif len(self.emptyFields) == 0:
			print('wtf')

	def winCondition(self, board, player):

		countx = 0 #check rows and columns
		counto = 0


		# orthogonal win condition
		for i in [0, 2, 4]:
			if [board[i][j] for j in [0, 2, 4]] == [player for i in range(3)]:
				return True
			for j in [0, 2, 4]:
				if board[j][i] == player:
					countx += 1
					if countx == 3:
						return True

			counto = 0
			countx = 0

		# diagonal win condition
		if [board[i][i] for i in [0, 2, 4]] == [player for i in range(3)]:
			return True

		elif [board[4-i][i] for i in [0, 2, 4]] == [player for i in range(3)]:
			return True			



class Board:

	def __init__(self, board, player):

		self.board = board
		self.score = None
		self.player = player
		self.moves = {}
		self.bf = BoardFactory()

	def playerSwitch(self):

		if self.player == 'X':
			self.player = 'O'
		elif self.player == 'O':
			self.player = 'X'

	def minimax(self):

		if not len(self.getEmptyFields()) == 0:
			for f in self.getEmptyFields():
				newBoard = self.bf.returnBoard(deepcopy(self.board), self.player)
				newBoard.board[f[0]][f[1]] = self.player

				if newBoard.isTermState():
					newBoard.score = newBoard.isTermState()
					self.score = newBoard.score
					self.moves[f] = self.score
				else:
					newBoard.playerSwitch()
					newBoard.minimax()
					self.moves[f] = newBoard.moves
				newBoard = None

	def getEmptyFields(self):

		e = []
		for i in [0, 2, 4]:
			for j in [0, 2, 4]:
				if self.board[i][j] == 0:
					e.append((i, j))
		return e

	def isTermState(self):

		if self.winCondition(self.board,'X'):
			return 1
		elif self.winCondition(self.board,'O'):
			return -1
		elif len(self.getEmptyFields()) == 0:
			return 0



	def winCondition(self, board, player):

		countx = 0 #check rows and columns
		counto = 0
		# orthogonal win condition
		for i in [0, 2, 4]: 
			if [board[i][j] for j in [0, 2, 4]] == [player for i in range(3)]:
				return True
			for j in [0, 2, 4]:
				if board[j][i] == player:
					countx += 1
					if countx == 3:
						return True

			counto = 0
			countx = 0

		# diagonal win condition
		if [board[i][i] for i in [0, 2, 4]] == [player for i in range(3)]:
			return True

		elif [board[4-i][i] for i in [0, 2, 4]] == [player for i in range(3)]:
			return True			


class BoardFactory:
	def __init__(self):
		pass

	def returnBoard(self, board, player):

		return Board(board, player)	

def main():
	'''
	xox
	xox
	  o
	'''

	# b = [
	# 	['X', 0, 'X', 0, 0], 
	# 	[0, 0, 0, 0, 0], 
	# 	['O', 0, 'O', 0, 0], 
	# 	[0, 0, 0, 0, 0], 
	# 	['X', 0, 'X', 0, 'O']
	# 	]

	b = [
		['X', 0, 0, 0, 0], 
		[0, 0, 0, 0, 0], 
		['O', 0, 0, 0, 0], 
		[0, 0, 0, 0, 0], 
		['X', 0, 0, 0, 0]
		]

	# b = [
	# 	['X', 0, 'X', 0, 'O'], 
	# 	[0, 0, 0, 0, 0], 
	# 	['O', 0, 'O', 0, 'X'], 
	# 	[0, 0, 0, 0, 0], 
	# 	['X', 0, 'X', 0, 'O']
	# 	]

	m = MiniMax(b, 'O')
	# m.minimax()
	pprint(m.moves)


main()
