#!/usr/bin/python

import sys
import os.path
import json
import curses

def init_curses(_width=20, _height=20, _pos=(0,0)):
	curses.initscr()
	curses.noecho()
	curses.cbreak()
	curses.curs_set(0)

	window = curses.newwin(_width + 2, _height + 2, _pos[0], _pos[1])
	window.border(0)
	window.keypad(1)

	return window

def close_curses():
	curses.echo()
	curses.nocbreak()
	curses.curs_set(1)
	curses.endwin()

def initialize(_width=20, _height=20, _config=None):
	world = []

	for i in xrange(_width):
		world.append([])
		for j in xrange(_height):
			world[i].append(0)

	if _config != None:
		for cell in _config:
			row = cell[0]
			col = cell[1]
			world[row][col] = 1

	return world

def display(_win, _world):
	for i in xrange(len(_world)):
		for j in xrange(len(_world[0])):
			cell = _world[i][j]
			if cell == 0:
				_win.addstr(i+1, j + 1, ' ')
			else:
				_win.addstr(i+1, j + 1, '0')

def neighboursAlive(_world, _pos):
	nh = 0

	r = 3
	for i in xrange(r):
		row = _pos[0] + i - 1
		if row < 0:
			row = len(_world) - 1
		else:
			if row >= len(_world):
				row = 0

		for j in xrange(r):
			col = _pos[1] + j - 1
			if col < 0:
				col = len(_world[0]) - 1
			else:
				if col >= len(_world[0]):
					col = 0

			if row != _pos[0] or col != _pos[1]:
				nh = nh + _world[row][col]

	return nh

def transition(_world):
	tmp = initialize(len(_world), len(_world[0]))

	for i in xrange(len(_world)):
		for j in xrange(len(_world[0])):
			cell = _world[i][j]
			tmp[i][j] = cell

			nh = neighboursAlive(_world, (i, j))

			if cell == 0:
				if nh == 3:
					tmp[i][j] = 1
			else:
				if nh < 2 or nh > 3:
					tmp[i][j] = 0

	return tmp

if __name__ == "__main__":
	
	filename = 'world.json'
	if len(sys.argv) > 1:
		filename = sys.argv[1]

	width = 20
	height = 20
	cells = None
	if os.path.isfile(filename) == True:
		json_data = open(filename)
		data = json.load(json_data)
		cells = data["cells"]
		if data["width"] != None:
			width = data["width"]
			height = data["height"]
		json_data.close()

	world = initialize(width, height, cells)

	win = init_curses(width, height)
	while True:
		display(win, world)
		key = win.getch()
		if key == 27:
			break
		world = transition(world)

	close_curses()