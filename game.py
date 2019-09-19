import curses
import textwrap
import time

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
		self.selectScr = curses.newwin(9, 20, 0, 0)
		self.pSelect = self.selectScr.subwin(5, 5, 1, 10)
		self.confSrc = self.selectScr.subwin(3, 18, 6, 0)
		self.helpWin = None
		self.y, self.x = self.gameWin.getyx()
		self.sely, self.selx = (1,1)
		self.errMsg = { 1 : 'Cant go here, You FOOL!',
						2 : 'You cannot sit here',
						3 : 'X wins!!!',
						4 : 'O wins!!!' ,
						5 : 'Draw!'}
		self.board = [[0 for x in range(5)] for y in range(5)]
		self.selArray = [[0 for x in range(5)] for y in range(5)]
		# self.selArray[:1][0] = 1
		self.player1 = None
		self.player2 = None
		self.preSelection = False
		self.confSelection = False
		self.nextPlayer = 'X'
		self.reMatch = True
		self.curMsg = ''
		self.wrapText = False

	def drawSelectScreen(self):

		self.selectScr.addstr(0, 0, 'Choose Player!')
		self.selectScr.addstr(2, 0, 'Player 1:')
		self.selectScr.addstr(4, 0, 'Player 2:')
		self.pSelect.addstr(1,0, '|')
		self.pSelect.addstr(1,2, '|')
		self.pSelect.addstr(1,4, '|')
		self.pSelect.addstr(3,0, '|')
		self.pSelect.addstr(3,2, '|')
		self.pSelect.addstr(3,4, '|')
		self.pSelect.addstr(0,0, '+-+-+')
		self.pSelect.addstr(2,0, '+-+-+')
		self.pSelect.addstr(4,0, '+-+-')
		try:
			self.pSelect.addstr(4,4, '+')
		except Exception:
			pass
		self.selectScr.refresh()
		self.pSelect.move(self.sely, self.selx)
		self.selectScr.refresh()

	def readSelectionInput(self):

		self.sely, self.selx = self.pSelect.getyx()
		c = self.pSelect.getch()
		if c == 65:
			self.sely -= 2
		elif c == 66:
			self.sely += 2
		elif c == 68:
			self.selx -= 2 
		elif c == 67:
			self.selx += 2
		elif c == ord('X') or c == ord('x') or c == curses.KEY_ENTER:
 
			self.makeSelection()
		
		elif c in [ord('y'), ord('Y')] and self.preSelection:
			self.confSelection = True 			
		elif c == ord('r'):
			self.resetSelection()
		elif c == ord('q'):
			self.quit()
		else:
			pass

	def makeSelection(self):

		for i in [1,3]:			
			for j in [1,3]:
				if self.sely == j:
					self.selArray[i][j] = 0
				self.selArray[self.selx][self.sely] = 1
				if self.selArray[i][j] == 1:
					self.pSelect.addstr(j, i, 'X')
				else:
					self.pSelect.addstr(j, i, ' ')

	def makeSelectionMove(self):

		try:
			self.pSelect.move(self.sely, self.selx)
			if self.helpWin:
				self.helpWin.erase()
				self.helpWin.refresh()
				self.helpWin = None
				self.curMsg = None
		except Exception:
			self.makeHelpWin(1)
			self.sely, self.selx = self.pSelect.getyx()

	def confirmSelection(self):

		confP1 = False
		confP2 = False

		for i in [1,3]:
			if self.selArray[i][1] == 1:
				confP1 = True
			if self.selArray[i][3] == 1:
				confP2 = True

		if confP1 and confP2:
			self.preSelection = True
			self.drawConfScreen()
		else:
			self.preSelection = False
			self.confSrc.erase()
			self.confSrc.refresh()

	def drawConfScreen(self):

			p1row = [self.selArray[i][1] for i in [1,3]]
			p2row = [self.selArray[i][3] for i in [1,3]]
			names = self.strFromSelection(p1row, p2row)
			assert len(names) == 2, 'Something in Selection went wrong.'
			self.confSrc.addstr(0 ,0,'Confirm Selection:')
			self.confSrc.addstr(1 ,0, str(names[0]))
			self.confSrc.addstr(1 ,4, 'vs.')			
			self.confSrc.addstr(1 ,8, str(names[1]))
			self.confSrc.addstr(1, 13, '[y/n]')
			self.confSrc.refresh()

	def strFromSelection(self, *args):

		out = []
		for arg in args:
			if arg == [1,0]:
				out.append('Hum')
			elif arg == [0,1]:
				out.append('Ai ')
		return out

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

	def resetSelection(self):
		self.selArray = [[0 for x in range(5)] for y in range(5)] 
		self.pSelect.erase()

	def quit(self):
		exit()
