import curses
from curses import wrapper
stdscr = curses.initscr()

class Window:
	def __init__(self):
		self.cwin = None
		self.height = None
		self.length = None
		self.y = None
		self.x = None

	def setWindow(self):
		self.cwin = curses.newwin(self.height, self.length, self.y, self.x)
		return


class PlayWindow(Window):
	def __init__(self):

		self.height = 10
		self.length = 10
		self.y = 10
		self.x = 10
		self.setWindow()

class HelpWindow(Window):
	def __init__(self):
		self.cwin = None
		self.msg = None
		self.height = 3
		self.length = None
		self.y = 30
		self.x = 10
		try:
			self.setMessage(self.msg)
		except AttributeError:
			pass
	

	def setMessage(self, msg):
		if msg and type(msg) == str:
			self.msg = msg
			self.length = len(msg) + 4
			self.setWindow()
			self.cwin.box()
			self.cwin.addstr(1, 2, self.msg)
			self.cwin.refresh()
			return 

	def clean(self):
		self.cwin = None
		return





class Action:
	def __init__(self, hwin):

		self.hwin = hwin

	def readInput(self, win, c):

			y, x = win.getyx()
			if c == curses.KEY_UP:
				y -= 1
			if c == curses.KEY_DOWN:
				y += 1 
			elif c == curses.KEY_LEFT:
				x -= 1 
			elif c == curses.KEY_RIGHT:
				x += 1
			elif c == ord('X') or c == ord('x'): 
				return (win, 'x')
			elif c == ord('O') or c == ord('o'):
				return (win, 'o')
			elif c == ord('r'):
				return (win, 'r')
			elif c == ord('q'):
				return (win, 'q')
			return (win, (y, x))

	def doAction(self, inp):

		if type(inp) == tuple:
			self.win = inp[0]
			self.yCur, self.xCur = self.win.getyx()
			if type(inp[1]) == tuple:
				return self.returnMove(inp[1])
				try: 
					self.hwin.clean()
				except AttributeError:
					pass
			elif type(inp[1]) == str:
				
				return self.returnCh(self)


		return self.current

	def returnMove(self, inp):
		y, x = inp
		try:
			self.win.move(y, x)
		except Exception as e:
			self.returnMsg('Cant go here')
			pass
		return

	def returnCh(self, inp):
		if inp == 'q':
			return 'q'
		elif inp == 'r':
			# win.move(0, 0)
			self.win.erase()
			return 
		elif inp == 'x':
			self.win.addstr('X')
			return
		elif inp == 'o':
			self.win.addstr('O')
			return

	def returnMsg(self, msg):
		if type(msg) == str:
			try:
				self.hwin.setMessage(msg)
			except AttributeError:
				pass
		return

# def readInput(win, c):

# 		y, x = win.getyx()
# 		if c == curses.KEY_UP:
# 			y -= 1
# 		if c == curses.KEY_DOWN:
# 			y += 1 
# 		elif c == curses.KEY_LEFT:
# 			x -= 1 
# 		elif c == curses.KEY_RIGHT:
# 			x += 1
# 		elif c == ord('X') or c == ord('x'): 
# 			return (win, 'x')
# 		elif c == ord('O') or c == ord('o'):
# 			return (win, 'o')
# 		elif c == ord('r'):
# 			return (win, 'r')
# 		elif c == ord('q'):
# 			return (win, 'q')
# 		return (win, (y, x))


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


# def displayHelp(errMsg):

# 	if type(errMsg) == str:
# 		length = len(errMsg)
# 	else:
# 		errMsg = 'Wrong Error format!'

# 	hwin = curses.newwin(3, length + 4, 30, 10 )
# 	hwin.box()
# 	hwin.addstr(1, 2, errMsg)
# 	hwin.refresh()
# 	return hwin

def main(stdscr):
	# stdscr.keypad(True)
	curses.use_default_colors()
	stdscr.clear()
	while True:
		c = stdscr.getch()
		# inp = readInput(stdscr, c)
		# ac = doAction(inp)

		pwin = PlayWindow()
		hwin = HelpWindow()
		a = Action(hwin)
		inp = a.readInput(pwin.cwin, c)
		ac = a.doAction(inp)
		

		if type(ac) == str:
			if ac == 'q':
				break

		pwin.cwin.refresh()
		stdscr.refresh()

		

wrapper(main)
