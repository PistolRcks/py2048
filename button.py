#example: button = Button("button.png", 5, 5)
import pygame

class Button(object):
	def __init__(self, image, xpos, ypos):
		self.image = pygame.image.load(image) #string - Image to load
		self.xpos = xpos #int - X position on the screen
		self.ypos = ypos #int - Y position on the screen
		self.display = True #bool - Display the button
	def draw(self, screen):
		if self.display == True:
			screen.blit(self.image, [self.xpos, self.ypos])
	def clickable(self):
		x, y = pygame.mouse.get_pos()
		xsize, ysize = self.image.get_rect().size
		#Note that self.x/ypos denotes the top-left corner, while the self.x/ypos + x/ysize denotes the bottom-right
		if x >= self.xpos and x <= self.xpos + xsize and y > self.ypos and y < self.ypos + ysize:
			return True
		else:
			return False
