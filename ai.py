from pprint import pprint
from copy import deepcopy

class MiniMax:

	def __init__(self, board, aiPlayer, huPlayer):

		self.aiPlayer = aiPlayer
		self.huPlayer = huPlayer
		self.moves = []
		self.bf = BoardFactory()
		self.initBoard = self.bf.returnBoard(board,	aiPlayer)
		self.initBoard.minimax()
		self.moves = self.initBoard.moves
		self.bestMove = None
		self.subMoves = []


	def findEndMove(self, moves, c=0):

		
		for m in moves:
			lvl = c
			for k, v in m.items():
				if type(v[1]) == int:
					if lvl:
						ws = ' '*lvl + '|' + '–'
						print(ws, v[0], k, v[1])
					else:
						print(v[0], k, v[1])
				if type(v[1]) == list:
					if lvl:
						ws = ' '*lvl + '|' + '+'
						print(ws, v[0], k)
					else:
						print(v[0], k)
					lvl += 1
					self.findEndMove(v[1], lvl)

	def findSubMoves(self, moves, c=0, tlist=[]):

		for m in moves:
			lvl = c
			for k, v in m.items():
				if type(v[1]) == int:
					if lvl:
						tlist.append((v[0], k, v[1]))
						if not tlist in self.subMoves:
							self.subMoves.append(tlist)
					else:
						tlist = []
						self.subMoves.append([(v[0], k, v[1])])
				
				if type(v[1]) == list:
					if lvl:
						tlist.append((v[0], k))
					else:
						tlist = []
						tlist.append((v[0], k))					
					lvl += 1
					self.findSubMoves(v[1], lvl, tlist)


	def findBestMove(self):

		allScores = []
		for m in self.subMoves:
			curScore = 0
			for t in m:
				if len(t) >= 3:
					if type(t[2]) == int:
						curScore += t[2]
			allScores.append((m[0], curScore))
		for s in allScores:
			print(s)

		

class Board:

	def __init__(self, board, player):

		self.board = board
		self.parent = None
		self.score = 0
		self.player = player
		self.moves = []
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
				newBoard.parent = self

				if newBoard.isTermState():
					move = {}
					newBoard.score = newBoard.isTermState()
					move[f] = self.player, newBoard.score
					self.moves.append(move)

				else:
					move = {}
					newBoard.playerSwitch()
					newBoard.minimax()
					if len(newBoard.moves) >= 1:
						move[f] = self.player, newBoard.moves
						self.moves.append(move)
					else:
						move[f] = self.player, 0
						self.moves.append(move)
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

	b = [
		['X', 0, 'X', 0, 0], 
		[0, 0, 0, 0, 0], 
		['O', 0, 'O', 0, 0], 
		[0, 0, 0, 0, 0], 
		['X', 0, 'X', 0, 'O']
		]

	# b = [
	# 	['X', 0, 0, 0, 0], 
	# 	[0, 0, 0, 0, 0], 
	# 	['O', 0, 0, 0, 0], 
	# 	[0, 0, 0, 0, 0], 
	# 	['X', 0, 0, 0, 0]
	# 	]

	# b = [
	# 	['X', 0, 'X', 0, 'O'], 
	# 	[0, 0, 0, 0, 0], 
	# 	['O', 0, 'O', 0, 'X'], 
	# 	[0, 0, 0, 0, 0], 
	# 	['X', 0, 'X', 0, 'O']
	# 	]

	m = MiniMax(b, 'O', 'X')
	# m.minimax()
	# for i in m.moves:
	# 	for k,v in i.items():
	# 		print(k)
	m.findSubMoves(m.moves)
	print('# PossibleMoves: ' + str(len(m.subMoves)))
	m.findBestMove()
	print(m.subMoves[-1])

	# m.findEndMove(m.moves)

	# pprint(m.moves)


main()
