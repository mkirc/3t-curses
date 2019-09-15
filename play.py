import curses
import textwrap
import time
from curses import wrapper

stdscr = curses.initscr()


class Game:
	def __init__(self, stdscr):
		self.stdscr = stdscr
		self.pwinY = 1
		self.pwinX = 1
		self.hwinY = 6
		self.hwinX = 0
		self.maxY = 10 # pwin + hwin + offset
		self.maxX = 50 # pwin + hwin + offset
		self.gameWin = curses.newwin(5, 5, self.pwinY, self.pwinX)
		self.helpWin = None
		self.y, self.x = self.gameWin.getyx()
		self.errMsg = { 1 : 'Cant go here, You FOOL!',
						2 : 'You cannot sit here',
						3 : 'X wins!!!',
						4 : 'O wins!!!' ,
						5 : 'Draw!'}
		self.board = [[0 for x in range(5)] for y in range(5)] 
		self.nextPlayer = 'X'
		self.reMatch = True
		self.curMsg = ''
		self.wrapText = False



	def drawGameWin(self):

		self.gameWin.addstr(0, 1, '|')
		self.gameWin.addstr(0, 3, '|')
		self.gameWin.addstr(2, 1, '|')
		self.gameWin.addstr(2, 3, '|')
		self.gameWin.addstr(4, 1, '|')
		self.gameWin.addstr(4, 3, '|')
		self.gameWin.addstr(1, 0, '–+–+–')
		self.gameWin.addstr(3, 0, '–+–+–')
		# try:
		# 	self.gameWin.addstr(4, 0, ' | | ')
		# except Exception:
		# 	pass
		self.gameWin.move(self.y, self.x)

	def checkTermSize(self):

		curses.update_lines_cols()
		self.termY = curses.LINES
		self.termX = curses.COLS
		# self.stdscr.addstr(9,0 ,str((self.termY, self.termX)))
		self.stdscr.refresh()

	def setWinPosByTermSize(self):

		if self.termY <= self.maxY:
			if self.termX >= self.maxX:
				self.hwinY = 1
				self.hwinX = 6
				self.wrapText = False
				
			else:
				self.hwinY = 1
				self.hwinX = 6
				self.wrapText = True

		else:
			self.hwinY = 6
			self.hwinX = 0

	def getMsgByTermSize(self, errCode):

		if not self.curMsg:
			msg = self.errMsg[errCode]
			self.curMsg = msg
			return msg
		else:
			if self.wrapText:
				dif = self.termX * 2 - self.maxX - 6
				try:
					self.curMsg = textwrap.fill(self.curMsg, dif)
				except ValueError:
					pass
			return self.curMsg


	def makeHelpWin(self, errCode):

		msg = self.getMsgByTermSize(errCode)
		if msg:
			msgY = 1
			if '\n' in msg:
				longest = ''
				allChunks = []
				for chunk in msg.split('\n'):
					allChunks.append(chunk)
					if len(longest) <= len(chunk):
						longest = chunk
				length = len(longest)
				for chunk in allChunks:
					msgY += 1
				
				self.helpWin = curses.newwin(msgY + 2, length + 4, self.hwinY, self.hwinX)
				for count,chunk in enumerate(allChunks):
					self.helpWin.addstr(count + 1, 2, chunk)
				self.helpWin.box()
				self.helpWin.refresh()

			else:
				length = len(msg)

				self.helpWin = curses.newwin(msgY + 2, length + 4, self.hwinY, self.hwinX)
				self.helpWin.addstr(1, 2, msg)
				self.helpWin.box()
				self.helpWin.refresh()
			


	def makeMove(self):

		try:
			self.gameWin.move(self.y, self.x)
			if self.helpWin:
				self.helpWin.erase()
				self.helpWin.refresh()
				self.helpWin = None
				self.curMsg = None

		except Exception:
			self.makeHelpWin(1)
			self.y, self.x = self.gameWin.getyx()

	def tryToSet(self, char):
		if self.board[self.x][self.y] == 0:
			self.board[self.x][self.y] = char
			return True
		else:
			#self.gameWin.addstr('h')
			#self.makeHelpWin(2)
			return False

	def checkWinCond(self):
		returnVal = 0 # 3 for x wins;  4 for o wins; 5 for Draw
		countx = 0 #check rows and columns
		counto = 0
		ac = [] # list all moves


		# orthogonal win condition
		for i in [0, 2, 4]: 
			if self.board[i] == ['X', 0, 'X', 0, 'X']:
				returnVal = 3
				return returnVal 
			elif self.board[i] == ['O', 0, 'O', 0, 'O']:
				returnVal = 4
				return returnVal
			for j in [0, 2, 4]:
				if self.board[i][j] != 0:
					ac.append(self.board[i][j])
				if self.board[j][i] == 'X':
					countx += 1
					if countx == 3:
						returnVal = 3
						return returnVal
				elif self.board[j][i] == 'O':
					counto += 1
					if counto == 3:
						returnVal = 4
						return returnVal

			counto = 0
			countx = 0

		# diagonal win condition
		if [self.board[i][i] for i in [0, 2, 4]] == ['X' for i in range(3)]:
			return 3
		elif [self.board[i][i] for i in [0, 2, 4]] == ['O' for i in range(3)]:
			return 4
		elif [self.board[4-i][i] for i in [0, 2, 4]] == ['X' for i in range(3)]:
			return 3
		elif [self.board[4-i][i] for i in [0, 2, 4]] == ['O' for i in range(3)]:
			return 4

		# draw condition
		if len(ac) == 9:
			return 5

	def readInput(self):

		c = self.gameWin.getch()
		if c == 65:
			self.y -= 2
		elif c == 66:
			self.y += 2
		elif c == 68:
			self.x -= 2 
		elif c == 67:
			self.x += 2
		elif c == ord('X') or c == ord('x'): 
			if self.nextPlayer == 'X' and self.tryToSet('X'):
				try:
					self.gameWin.addstr('X')
				except Exception:
					pass
				self.nextPlayer = 'O'

		elif c == ord('O') or c == ord('o'):
			if self.nextPlayer == 'O' and self.tryToSet('O'):
				try:
					self.gameWin.addstr('O')
				except Exception:
					pass
				self.nextPlayer = 'X'
		elif c == ord('r'):
			self.reset()
		elif c == ord('q'):
			self.quit()
		else:
			pass
			# self.gameWin.addstr(str(c))
			# # self.gameWin.addstr(str(d))
			# self.gameWin.refresh()

	def reset(self):
		self.board = [[0 for x in range(5)] for y in range(5)] 
		self.gameWin.erase()
		self.nextPlayer = 'X'
		self.y, self.x = self.gameWin.getyx()



	def quit(self):
		exit()


def main(stdscr):
	g = Game(stdscr)
	curses.use_default_colors()
	stdscr.clear()
	while g.reMatch:
		g.reMatch = False
		while not g.checkWinCond():

			
			g.checkTermSize()
			g.setWinPosByTermSize()
			g.drawGameWin()
			g.readInput()
			g.makeMove()
			g.checkWinCond()
			stdscr.refresh()

		g.makeHelpWin(g.checkWinCond())
		c = g.gameWin.getch()
		if c == ord('r'):
			g.reset()
			g.reMatch = True
			


		
		

wrapper(main)
