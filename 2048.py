#!/usr/bin/python
from random import randint
import pygame
pygame.init()
done = False
clock = pygame.time.Clock()
size = (400, 400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("2048")
GRAY = (150, 150, 150)
score = 0
pressed = False
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
def combine(i, move, edge):
	if grid[i] != 0 and i != edge[0] and i != edge[1] and i != edge[2] and i != edge[3]:
		if grid[i + move] == grid[i]:
			grid[i + move] = grid[i] + 1 
			grid[i] = 0
			global score, changed
			score += 2**(x+1)
			changed = True
			if x + 1 >= 11:
				message = "You win!"
def movetile(i, move, edge):
	if grid[i] != 0 and i != edge[0] and i != edge[1] and i != edge[2] and i != edge[3]:
		if grid[i + move] == 0:
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

restart()
message = "Use arrow keys to move."

while not done:
	pressed = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_LEFT:
				move = -1
				edge = [0, 4, 8, 12]
				pressed = True
			if event.key == pygame.K_RIGHT:
				move = 1
				edge = [3, 7, 11, 15]
				pressed = True
			if event.key == pygame.K_UP:
				move = -4
				edge = [0, 1, 2, 3]
				pressed = True
			if event.key == pygame.K_DOWN:
				move = 4
				edge = [12, 13, 14, 15]
				pressed = True
			
			if event.key == pygame.K_r:
				restart()
				continue
			if event.key == pygame.K_q
				done = True
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
	pygame.display.flip()
	if pressed == True:
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
			message = "Invalid move."
			continue
		else:
			message = ""
		newtile()
	
	clock.tick(30)
pygame.quit()
