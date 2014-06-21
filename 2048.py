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


TILES = [
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

def newtile():
	whichTile = randint(1,10)
	if whichTile == 10:
		n = 2
	else:
		n = 1
	empty = []
	for i in range(16):
		if grid[i] == 0:
			empty.append(i)
	if empty == []:
		return 0
	new = randint(0,len(empty)-1)
	grid[empty[new]] = n

def hasLost():
	canMove = False
	move = -1
	edge = [0, 4, 8, 12]
	for i in range(16):
		if moveable(i, move, edge) or combinable(i, move, edge):
			canMove = True
	move = 1
	edge = [3, 7, 11, 15]
	for i in range(16):
		if moveable(i, move, edge) or combinable(i, move, edge):
			canMove = True
	move = -4
	edge = [0, 1, 2, 3]
	for i in range(16):
		if moveable(i, move, edge) or combinable(i, move, edge):
			canMove = True
	move = 4
	edge = [12, 13, 14, 15]
	for i in range(16):
		if moveable(i, move, edge) or combinable(i, move, edge):
			canMove = True
	if not canMove:
		return True
	else:
		return False

def isEdge(i, edge):
	if i != edge[0] and i != edge[1] and i != edge[2] and i != edge[3]:
		return False
	else:
		return True

def moveable(i, move, edge):
	if not isEdge(i, edge):
		if grid[i] != 0 and grid[i + move] == 0:
			return True

def combinable(i, move, edge):
	if not isEdge(i, edge):
		if grid[i] != 0 and grid[i + move] == grid[i]:
			return True

def combine(i, move, edge): 	if combinable(i, move, edge): 		grid[i + move] =
grid[i] + 1 		grid[i] = 0 		global score, changed 		score += 2**(grid[i + move])
changed = True 		if grid[i + move] + 1 >= 11: 			message = "You win!"

def movetile(i, move, edge):
	if moveable(i, move, edge):
		grid[i + move] = grid[i]
		grid[i] = 0
		movetile(i + move, move, edge)
		global changed
		changed = True

def restart():
	global message, score, grid
	message = ""
	score = 0
	grid = [0, 0, 0, 0,
			0, 0, 0, 0,
			0, 0, 0, 0,
			0, 0, 0, 0 ]
	newtile()
	newtile()

def moveAll(move, edge):
	global changed
	global message
	changed = False
	if move == -1 or move == -4:
		for i in range(16):
			movetile(i, move, edge)
		for i in range(16):
			combine(i, move, edge)
		for i in range(16):
			movetile(i, move, edge)
	else:
		for i in reversed(range(16)):
			movetile(i, move, edge)
		for i in reversed(range(16)):
			combine(i, move, edge)
		for i in reversed(range(16)):
			movetile(i, move, edge)
	if not changed:
		if hasLost():
			message = "Game over."
		else:
			message = "Invalid move"
	else:
		message = ""
		newtile()

def quit_game():
	global running
	running = False

def move_left():
	move = -1
	edge = [0, 4, 8, 12]
	moveAll(move, edge)

def move_right():
	move = 1
	edge = [3, 7, 11, 15]
	moveAll(move, edge)

def move_up():
	move = -4
	edge = [0, 1, 2, 3]
	moveAll(move, edge)

def move_down():
	move = 4
	edge = [12, 13, 14, 15]
	moveAll(move, edge)

key_action = { pygame.K_LEFT : move_left,
		pygame.K_RIGHT : move_right,
		pygame.K_UP : move_up,
		pygame.K_DOWN : move_down,
		pygame.K_r : restart,
		pygame.K_q : quit_game,
		}

def redraw():
	pygame.display.set_caption("Score: "+str(score)+"        "+message)
	screen.fill(GRAY)
	xpos = 5
	ypos = 5
	for x in range(4):
		for i in range(4):
			screen.blit(TILES[grid[4 * x + i]], [xpos, ypos])
			xpos += 100
		xpos = 5
		ypos += 100
	button_restart.draw(screen)
	button_help.draw(screen)
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
