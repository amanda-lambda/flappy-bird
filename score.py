import pygame
# from pygame.locals import *
from pygame.sprite import Sprite

class Score(Sprite):
	"""
	Number sprites, to be used to display the score.
	"""
	# Initialize base
	def __init__(self):
		self.value = 0
		self.screen = pygame.display.get_surface() 
		self.y = self.screen.get_height()*0.1

		# Sprites
		self.digits = []
		for i in range(10):
			self.digits.append(pygame.image.load('assets/%i.png' % i).convert_alpha())

	# Update score (+1 for making it through the pipe)
	def update(self):
		self.value += 1

	# Draw sprite to game display
	def draw(self):
		score_digits = [int(i) for i in list(str(self.value))]
		score_width = sum([self.digits[i].get_width() for i in score_digits])
		x = (self.screen.get_width() - score_width) / 2
		for i in score_digits:
			self.screen.blit(self.digits[i], (x, self.y))
			x += self.digits[i].get_width()