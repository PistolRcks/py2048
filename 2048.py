#!/usr/bin/python
from random import randint
import pygame
from button import Button
import math

#GUI
button_restart = Button("restart.png", 342, 400)
button_help = Button("help.png", 371, 400)

done = False
animating = False
frame = 0
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
		grid[(i['grid_x'] * 4) + i['grid_y']] = 1
	for i in range(16):
		if grid[i] == 0:
			empty.append(i)

	pos = empty[randint(0, len(empty)-1)]
	xpos = pos % 4
	ypos = (pos - xpos) / 4

	tiles.append({
			'grid_x' : xpos,
			'grid_y' : ypos,
			'value' : value,
			'draw_x' : xpos * 100 + 5,
			'draw_y' : ypos * 100 + 5,
			'change_x' : 0,
			'change_y' : 0
			})

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
		if tile['grid_x'] + xmove > 3 or tile['grid_x'] + xmove < 0:
			return True
	elif ymove != 0:
		if tile['grid_y'] + ymove > 3 or tile['grid_y'] + ymove < 0:
			return True
	return False

def movable(tile, xmove, ymove):
	if not isEdge(tile, xmove, ymove):
		for i in tiles:
			if i['grid_x'] == tile['grid_x'] + xmove and i['grid_y'] == tile['grid_y'] + ymove:
				return False
		return True

def combinable(tile, xmove, ymove):
	#if not isEdge(tile, xmove, ymove):
		for i in tiles:
			if i['grid_x'] == tile['grid_x'] + xmove and i['grid_y'] == tile['grid_y'] + ymove and i['value'] == tile['value']:
				return True
def combineTile(tile, xmove, ymove):
	if combinable(tile, xmove, ymove):
		for i in tiles:
			if i['grid_x'] == tile['grid_x'] + xmove and i['grid_y'] == tile['grid_y'] + ymove:
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
			tile['grid_x'] += xmove
			tile['grid_y'] += ymove
			global changed
			changed = True
		else:
			break

# TODO: use this easing function in the animation
#def easeInQuad(time, start, change, duration):
#	time /= duration
#	return change * time * time + start

def initAnimation(tile, xmove, ymove):
	global animating
	animating = True
	if tile['grid_x'] * 100 + 5 == tile['draw_x']:
		tile['change_x'] = 0
	else:
		tile['change_x'] = math.fabs(tile['draw_x'] - (tile['grid_x'] * 100 + 5)) / 15 * xmove
	if tile['grid_y'] * 100 + 5 == tile['draw_y']:
		tile['change_y'] = 0
	else:
		tile['change_y'] = math.fabs(tile['draw_y'] - (tile['grid_y'] * 100 + 5)) / 15 * ymove
def animate():
	global animating, frame
	frame += 1
	if frame < 15:
		for tile in tiles:
			tile['draw_x'] += tile['change_x']
			tile['draw_y'] += tile['change_y']
	else:
		animating = False
		frame = 0

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
	for i in order:
		for tile in tiles:
			initAnimation(tile, xmove, ymove)
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

def quitGame():
	global done
	done = True

def moveLeft():
	moveAll(-1, 0, 'grid_x')

def moveRight():
	moveAll(1, 0, 'grid_x')

def moveUp():
	moveAll(0, -1, 'grid_y')

def moveDown():
	moveAll(0, 1, 'grid_y')

key_action = {
		pygame.K_LEFT : moveLeft,
		pygame.K_RIGHT : moveRight,
		pygame.K_UP : moveUp,
		pygame.K_DOWN : moveDown,
		pygame.K_r : restart,
		pygame.K_q : quitGame,
		}

def redraw():
	pygame.display.set_caption("Score: "+str(score)+"        "+message)
	screen.fill(GRAY)
	button_restart.draw(screen)
	button_help.draw(screen)
	for tile in tiles:
		screen.blit(IMAGES[tile['value']], [tile['draw_x'], tile['draw_y']])
	pygame.display.flip()

if __name__ == "__main__":
	restart()
	message = "Use arrow keys to move."
	redraw()

	while not done:

		if animating:
			animate()
			redraw()
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				elif event.type == pygame.KEYDOWN:
					try:
						global changed
						changed = False
						key_action[event.key]()
						animate()
						redraw()
					except KeyError:
						pass
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if button_restart.clicked():
						restart()
						redraw()
					elif button_help.clicked():
						message = "Use arrow keys to move."

		clock.tick(60)
	pygame.quit()
