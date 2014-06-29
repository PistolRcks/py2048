#!/usr/bin/python
from random import randint
import pygame
from button import Button

#GUI
button_restart = Button("restart.png", 342, 400)
button_help = Button("help.png", 371, 400)

done = False
score = 0
pygame.init()
clock = pygame.time.Clock()
size = (400, 430)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("2048")
GRAY = (150, 150, 150)

tiles = []

IMAGES = [
		pygame.image.load("0.png"),
		pygame.image.load("2.png"),
		pygame.image.load("4.png"),
		pygame.image.load("8.png"),
		pygame.image.load("16.png"),
		pygame.image.load("32.png"),
		pygame.image.load("64.png"),
		pygame.image.load("128.png"),
		pygame.image.load("256.png"),
		pygame.image.load("512.png"),
		pygame.image.load("1024.png"),
		pygame.image.load("2048.png")
		]

def newTile():
	n = randint(1, 10)
	if n == 10:
		value = 2
	else:
		value = 1

	grid = []
	empty = []
	for i in range(16):
		grid.append(0)
	for i in tiles:
		grid[(i['ypos'] * 4) + i['xpos']] = 1
	for i in range(16):
		if grid[i] == 0:
			empty.append(i)

	pos = empty[randint(0, len(empty)-1)]
	xpos = pos % 4
	ypos = (pos - xpos) / 4

	tiles.append({'xpos': xpos, 'ypos': ypos, 'value': value})

def hasLost():
	for tile in tiles:
		if ( movable(tile, 0,-1) or combinable(tile, 0,-1) or
		     movable(tile, 0, 1) or combinable(tile, 0, 1) or
			   movable(tile,-1, 0) or combinable(tile,-1, 0) or
			   movable(tile, 1, 0) or combinable(tile, 1, 0)  ):
			return False
	return True

def isEdge(tile, xmove, ymove):
	if xmove != 0:
		if tile['xpos'] + xmove > 3 or tile['xpos'] + xmove < 0:
			return True
	elif ymove != 0:
		if tile['ypos'] + ymove > 3 or tile['ypos'] + ymove < 0:
			return True
	return False

def movable(tile, xmove, ymove):
	if not isEdge(tile, xmove, ymove):
		for i in tiles:
			if i['xpos'] == tile['xpos'] + xmove and i['ypos'] == tile['ypos'] + ymove:
				return False
		return True

def combinable(tile, xmove, ymove):
	#if not isEdge(tile, xmove, ymove):
		for i in tiles:
			if i['xpos'] == tile['xpos'] + xmove and i['ypos'] == tile['ypos'] + ymove and i['value'] == tile['value']:
				return True
def combineTile(tile, xmove, ymove):
	if combinable(tile, xmove, ymove):
		for i in tiles:
			if i['xpos'] == tile['xpos'] + xmove and i['ypos'] == tile['ypos'] + ymove:
				tiles.remove(tile)
				i['value'] += 1
				global score, message, changed
				changed = True
				score += 2 ** i['value']
				if i['value'] >= 11:
					message = "You win!"
def moveTile(tile, xmove, ymove):
	while True:
		if movable(tile, xmove, ymove):
			tile['xpos'] += xmove
			tile['ypos'] += ymove
			global changed
			changed = True
		else:
			break

def moveAll(xmove, ymove, target):
	global changed
	changed = False
	if xmove == 1 or ymove == 1:
		order = [3, 2, 1, 0]
	else:
		order = [0, 1, 2, 3]
	for i in order:
		for tile in tiles:
			if tile[target] == i:
				moveTile(tile, xmove, ymove)
	for i in order:
		for tile in tiles:
			if tile[target] == i:
				combineTile(tile, xmove, ymove)
	for i in order:

		for tile in tiles:
			if tile[target] == i:
				moveTile(tile, xmove, ymove)
	global message
	if len(tiles) == 16:
		if hasLost():
			message = "Game over"
	elif not changed:
		message = "Invalid move."
	else:
		message = ""
		newTile()

def restart():
	global message, score, tiles
	message = ""
	score = 0
	tiles = []
	newTile()
	newTile()


"""
def moveAll(xmove, ymove):
	itiles = tiles
	if xmove == -1:
		for i in range(4):
			for tile in tiles:
				if tile['xpos'] == i:
					moveTile(tile, xmove, ymove)
	elif ymove == -1:
		for i in range(4):
			for tile in tiles:
				if tile['ypos'] == i:
					moveTile(tile, xmove, ymove)
	elif xmove == 1:
		for i in reversed(range(4)):
			for tile in tiles:
				if tile['xpos'] == i:
					moveTile(tile, xmove, ymove)
	elif ymove == 1:
		for i in reversed(range(4)):
			for tile in tiles:
				if tile['ypos'] == i:
					moveTile(tile, xmove, ymove)
	global message
	if itiles == tiles:
		if hasLost():
			message = "Game over."
		else:
			message = "Invalid move."
	else:
		message = ""
		newTile()
"""

def quit_game():
	global running
	running = False

def moveLeft():
	moveAll(-1, 0, 'xpos')

def moveRight():
	moveAll(1, 0, 'xpos')

def moveUp():
	moveAll(0, -1, 'ypos')

def moveDown():
	moveAll(0, 1, 'ypos')

key_action = {
		pygame.K_LEFT : moveLeft,
		pygame.K_RIGHT : moveRight,
		pygame.K_UP : moveUp,
		pygame.K_DOWN : moveDown,
		pygame.K_r : restart,
		pygame.K_q : quit_game,
		}

def redraw():
	pygame.display.set_caption("Score: "+str(score)+"        "+message)
	screen.fill(GRAY)
	button_restart.draw(screen)
	button_help.draw(screen)
	for tile in tiles:
		screen.blit(IMAGES[tile['value']], [tile['xpos'] * 100 + 5, tile['ypos'] * 100 + 5])
	pygame.display.flip()


restart()
message = "Use arrow keys to move."
redraw()

while not done:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		elif event.type == pygame.KEYDOWN:
			try:
				global changed
				changed = False
				key_action[event.key]()
				redraw()
			except KeyError:
				pass
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if button_restart.clicked():
				restart()
				redraw()
			elif button_help.clicked():
				message = "Use arrow keys to move."

	clock.tick(30)
pygame.quit()
