#!/usr/bin/python
from random import randint
import pygame
from button import Button

#GUI
button_restart = Button("restart.png", 342, 400)
button_help = Button("help.png", 371, 400)

done = False
score = 0
message = ""
pygame.init()
clock = pygame.time.Clock()
size = (400, 430)
screen = pygame.display.set_mode(size)
GRAY = (150, 150, 150)
auto = False

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

#For debugging.
"""
def putTile(xpos, ypos, value):
	tiles.append({
			'grid_x' : xpos,
			'grid_y' : ypos,
			'value' : value,
			'draw_x' : xpos * 100 + 5,
			'draw_y' : ypos * 100 + 5,
			'change_x' : 0,
			'change_y' : 0
			})
"""
def newTile():
	n = randint(1, 10)
	if n == 10:
		value = 2 #There's a 1/10 chance that the new tile will be a 4 instead of a 2
	else:
		value = 1

	#Check if there are any empty spaces
	grid = []
	empty = []
	for i in range(16): #Fill the grid with zeroes
		grid.append(0)
	for i in tiles: #Tiles which exist will be changed to 1 in the grid table
		grid[(i['grid_y'] * 4) + i['grid_x']] = 1
	for i in range(16):
		if grid[i] == 0: #Rows which are zero can be appended to the list of empty slots
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
	if not isEdge(tile, xmove, ymove):
		for i in tiles:
			if i['grid_x'] == tile['grid_x'] + xmove and i['grid_y'] == tile['grid_y'] + ymove and i['value'] == tile['value']:
				return True
def combineTile(tile, xmove, ymove):
	for i in tiles:
		if i['grid_x'] == tile['grid_x'] + xmove and i['grid_y'] == tile['grid_y'] + ymove and combinable(tile, xmove, ymove):
			tiles.remove(i)
			tile['change_x'] += xmove
			tile['change_y'] += ymove
			tile['grid_x'] += xmove
			tile['grid_y'] += ymove
			tile['value'] += 1
			global score, message
			score += 2 ** tile['value']
			if tile['value'] >= 11:
				message = "You win!"
def moveTile(tile, xmove, ymove):
	while True:
		if movable(tile, xmove, ymove):
			tile['grid_x'] += xmove
			tile['grid_y'] += ymove
			tile['change_x'] += xmove
			tile['change_y'] += ymove
		else:
			break
def changed():
	for tile in tiles:
		if tile['change_x'] != 0 or tile['change_y'] != 0:
			return True
	return False
def animate():
	for i in range(10):
		for tile in tiles:
			tile['draw_x'] += tile['change_x'] * 10
			tile['draw_y'] += tile['change_y'] * 10
		redraw()
		clock.tick(60)
def moveAll(xmove, ymove, target):
	for tile in tiles:
		tile['change_x'] = 0
		tile['change_y'] = 0
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

def autoPlay(): #Random automatic 2048! Partially for debugging, partially for fun
	if auto and not hasLost():
		dir = [moveUp, moveRight, moveLeft, moveDown]
		choices = []
		allowed = [0,0,0,0]
		for tile in tiles:
			if movable(tile, 0, -1) or combinable(tile, 0, -1): #Check if we can move (or combine) every tile up
				allowed[0] += 1 #If so, add one to the list of allowed directions (in that direction)
			if movable(tile, 1, 0) or combinable(tile, 1, 0): #Same goes for right
				allowed[1] += 1
			if movable(tile, 0, 1) or combinable(tile, 0, 1): #Same goes for down
				allowed[2] += 1
			if movable(tile, -1, 0) or combinable(tile, -1, 0): #Same goes for left
				allowed[3] += 1
		for i in range(4):
			if allowed[i-1] is not len(tiles): #If all tiles can move in a certain direction, append it to the list of possible directions
			 	choices.append(dir[i-1])
		dir[randint(1,len(choices))-1]() #Get a random choice from all of the possible directions and move in that direction
def autoSwitch():
	global auto
	auto = not auto

key_action = {
		pygame.K_LEFT : moveLeft,
		pygame.K_RIGHT : moveRight,
		pygame.K_UP : moveUp,
		pygame.K_DOWN : moveDown,
		pygame.K_r : restart,
		pygame.K_q : quitGame,
		pygame.K_a : autoSwitch,
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
		if auto:
			autoPlay()
			message = "Auto is on."
			animate()
			if len(tiles) == 16:
				if hasLost():
					message = "Game over"
					auto = False
					print("List of tiles is: ")
					for tile in tiles:
						print("In pos ["+str(tile["grid_x"])+","+str(tile["grid_y"])+"] with value of "+str(2**tile["value"]))
			elif changed():
				newTile()
			redraw()
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				elif event.type == pygame.KEYDOWN or auto:
					try:
						key_action[event.key]()
						animate()
						if len(tiles) == 16:
							if hasLost():
								message = "Game over"
						elif not changed():
							message = "Invalid move."
						else:
							message = ""
							newTile()
						redraw()
					except KeyError:
						pass
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if button_restart.clickable():
						restart()
						redraw()
					elif button_help.clickable():
						message = "Use arrow keys to move."
						redraw()

		clock.tick(10)
	pygame.quit()
