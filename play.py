import curses
# import textwrap
# import time
from curses import wrapper
from game import Game

stdscr = curses.initscr()




def main(stdscr):
	g = Game(stdscr)
	curses.use_default_colors()
	stdscr.clear()
	while not g.confSelection:
		g.drawSelectScreen()
		g.readSelectionInput()
		g.makeSelectionMove()
		g.confirmSelection()
		stdscr.refresh()		
	
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
