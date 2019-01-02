#!/usr/bin/python2.7
import random
import pygame
from button import Button
from game import Board

#GUI
button_restart = Button("restart.png", 342, 400)
button_help = Button("help.png", 371, 400)

done = False
message = ""
pygame.init()
clock = pygame.time.Clock()
size = (400, 430)
screen = pygame.display.set_mode(size)
GRAY = (150, 150, 150)
auto = False
board = Board(4, 4)
animate_percentage = 0
last_direction = 'up'

# Creates a copy of the board's grid so that it can be compared against a later version
def copy(board):
    grid = []
    for value in board.grid:
        grid.append(value)
    return grid

old_grid = copy(board)

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

def quitGame():
    global done
    done = True

def move(direction):
    global animate_percentage, old_grid, last_direction
    animate_percentage = 0
    old_grid = copy(board)
    if board.move(direction):
        board.new_tile()
    last_direction = direction

def move_left(): move('left')
def move_right(): move('right')
def move_up(): move('up')
def move_down(): move('down')

def autoPlay(): #Random automatic 2048! Partially for debugging, partially for fun
    if auto:
        directions = [move_up, move_right, move_left, move_down]
        random.choice(directions)()

def autoSwitch():
    global auto
    auto = not auto

def restart():
    global board
    board = Board(4, 4)
    old_grid = copy(board)
    board.new_tile()
    board.new_tile()

key_action = {
    pygame.K_LEFT : move_left,
    pygame.K_RIGHT : move_right,
    pygame.K_UP : move_up,
    pygame.K_DOWN : move_down,
    pygame.K_r : restart,
    pygame.K_q : quitGame,
    pygame.K_a : autoSwitch,
}

def draw_tile(x, y, offsetx=0, offsety=0, scale=100):
    screen.blit(
            pygame.transform.scale(
                IMAGES[board.get(x, y)],
                (scale * 90 / 100, scale * 90 / 100)),
            ((x * 100 + .5 * (100 - scale) + 5) + offsetx, (y * 100 + (.5 * (100 - scale) + 5)) + offsety))

def draw(direction):
    global animate_percentage
    pygame.display.set_caption("Score: " + str(board.score) + "        " + message)
    screen.fill(GRAY)
    button_restart.draw(screen)
    button_help.draw(screen)
    changed = board
    ranges = {
        'left': range(board.width),
        'right': range(board.width),
        'up': range(board.height),
        'down': range(board.height),
    }

    if direction == 'left' or direction == 'right':
        for y in range(board.height):
            animated = False
            for x in ranges[direction]:
                if board.get(x, y) != old_grid[y * board.width + x]:
                    animated = True
                if animated and board.get(x, y) != 0:
                    if direction == 'left':
                        draw_tile(x, y, 1 * (100 - animate_percentage), 0, animate_percentage)
                    else:
                        draw_tile(x, y, -(1 * (100 - animate_percentage)), 0, animate_percentage)
                elif board.get(x, y) != 0:
                    draw_tile(x, y)
    else:
        for x in range(board.width):
            animated = False
            for y in ranges[direction]:
                if board.get(x, y) != old_grid[y * board.width + x]:
                    animated = True
                if animated and board.get(x, y) != 0:
                    if direction == 'up':
                        draw_tile(x, y, 0, 1 * (100 - animate_percentage), animate_percentage)
                    else:
                        draw_tile(x, y, 0, -(1 * (100 - animate_percentage)), animate_percentage)
                elif board.get(x, y) != 0:
                    draw_tile(x, y)
    animate_percentage = min(100, animate_percentage + 12)
    pygame.display.flip()

if __name__ == "__main__":
    restart()
    message = "Use arrow keys to move."

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                try:
                    key_action[event.key]()
                except KeyError:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_restart.clickable():
                    restart()
                elif button_help.clickable():
                    message = "Use arrow keys to move."

        if auto:
            if animate_percentage >= 100:
                autoPlay()
                message = "Auto is on."
        draw(last_direction)
        clock.tick(60)
    pygame.quit()
