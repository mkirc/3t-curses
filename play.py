import curses
from curses import wrapper
stdscr = curses.initscr()


class Game:
	def __init__(self, stdscr):
		self.stdscr = stdscr
		self.gameWin = curses.newwin(5, 5)
		self.helpWin = None
		self.y, self.x = self.gameWin.getyx()
		self.errMsg = { 1 : 'Cant go here, You FOOL!' }

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

	def makeHelpWin(self, errCode):

		msg = self.errMsg[errCode]
		if msg:
			self.helpWin = curses.newwin(3, len(msg) + 4, 30, 10 )
			self.helpWin.box()
			self.helpWin.addstr(1, 2, msg)
			self.helpWin.refresh()

	def makeMove(self):

		try:
			self.gameWin.move(self.y, self.x)
			if self.helpWin:
				self.helpWin.erase()
				self.helpWin.refresh()

		except Exception:
			self.makeHelpWin(1)
			self.y, self.x = self.gameWin.getyx()


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
			try:
				self.gameWin.addstr('X')
			except Exception:
				pass
		elif c == ord('O') or c == ord('o'):
			try:
				self.gameWin.addstr('O')
			except Exception:
				pass
		elif c == ord('r'):
			self.reset()
		elif c == ord('q'):
			self.quit()
		else:
			pass
			# self.gameWin.addstr(str(c))
			# # self.gameWin.addstr(str(d))
			# self.gameWin.refresh()

	def quit(self):
		exit()

	def reset(self):
		self.gameWin.erase()
		self.y, self.x = self.gameWin.getyx()



def main(stdscr):
	g = Game(stdscr)
	curses.use_default_colors()
	stdscr.clear()
	
	while True:

		g.drawGameWin()
		g.readInput()
		g.makeMove()

		stdscr.refresh()

		

wrapper(main)




# def doAction(inp):
# 	if type(inp) == tuple:
# 		win = inp[0]
# 		yOld, xOld = win.getyx()
# 		if type(inp[1]) == tuple:
# 			y, x = inp[1]
# 			try:
# 				win.move(y, x)
# 			except Exception as e:
# 				hwin = displayHelp('Cant go here, You FOOL!')
# 				win.move(yOld, xOld)
# 				return
# 		elif type(inp[1]) == str:
# 			if inp[1] == 'q':
# 				return 'q'
# 			elif inp[1] == 'r':
# 				# win.move(0, 0)
# 				win.erase()
# 				return
# 			elif inp[1] == 'x':
# 				win.addstr('X')
# 				return
# 			elif inp[1] == 'o':
# 				win.addstr('O')
# 				return

# class HelpWin:

# 	def __init__(self):
# 		self.win = None
# 		self.msg = None
# 	def makeMsg:
# 		self.win = curses.newwin(3, len(self.msg) + 4, 30, 10 )
# 		self.win.box()
# 		self.win.addstr(1, 2, self.msg)
# 		self.win.refresh()
# 		return self.hwin

# 	def setMsg(self, errMsg):

# 		if type(errMsg) == str:
# 			self.msg = errMsg
# 		else:
# 			self.msg = 'Wrong Error format!'
# 		return self.msg

