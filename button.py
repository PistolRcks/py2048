#example: button = Button("button.png", 5, 5)
import pygame

class Button(object):
	def __init__(self, image, xpos, ypos):
		self.image = pygame.image.load(image)
		self.xpos = xpos
		self.ypos = ypos
		self.display = True
	def draw(self, screen):
		if self.display == True:
			screen.blit(self.image, [self.xpos, self.ypos])
	def clicked(self):
		pos = pygame.mouse.get_pos()
		x = pos[0]
		y = pos[1]
		size = self.image.get_rect().size
		xsize = size[0]
		ysize = size[1]
		xmin = self.xpos
		ymin = self.ypos
		xmax = self.xpos + xsize
		ymax = self.ypos + ysize
		if x >= xmin and x <= xmax and y > ymin and y < ymax:
			return True
		else:
			return False
