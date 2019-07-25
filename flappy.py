import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite


class Bird(Sprite):
	"""
	Bird sprite, controlled by the player.
	"""
	# Initialize player
	def __init__(self):
		self.screen = pygame.display.get_surface() 
		self.x, self.y = 0.2*self.screen.get_width(), 0.45*self.screen.get_height()
		self.rotation = 0
		self.velocity = -9

		self.state = 0
		self.shift_state = 0
		self.shift_cycle = [0,1,2,3,4,5,6,7,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-7,-6,-5,-4,-3,-2,-1]

		# Sprite images
		self.im_upflap = pygame.image.load('assets/bird_upflap.png').convert_alpha()
		self.im_midflap = pygame.image.load('assets/bird_midflap.png').convert_alpha()
		self.im_downflap = pygame.image.load('assets/bird_downflap.png').convert_alpha()
		self.im_cycle = [self.im_upflap, self.im_midflap, self.im_downflap, self.im_midflap]
		self.image = self.im_cycle[self.state]

		# Masks
		self.mask_upflap = pygame.mask.from_surface(self.im_upflap)
		self.mask_midflap = pygame.mask.from_surface(self.im_midflap)
		self.mask_downflap = pygame.mask.from_surface(self.im_downflap)
		self.mask_cycle = [self.mask_upflap, self.mask_midflap, self.mask_downflap, self.mask_midflap]
		self.mask = self.mask_cycle[self.state]

	def update(self, key_press=False):
		if key_press:
			self.rotation = 45
			self.velocity = -9
			self.y += self.velocity
		else:
			# Rotate 3 degrees CW, with threshold at 20
			self.rotation -= 3
			if self.rotation < 20:
				self.rotation = 20
			# Update velocity, with terminal velocity at 10
			self.velocity += 1
			if self.velocity > 10:
				self.velocity = 10
			# Update position
			self.y += self.velocity

	def change_flap_state(self):
		self.state = (self.state + 1) % len(self.im_cycle)
		self.image = self.im_cycle[self.state]
		self.mask = self.mask_cycle[self.state]

	# Oscillate up and down during start screen
	def oscillate(self):
		self.shift_state = (self.shift_state + 1) % len(self.shift_cycle)
		self.y = 0.45*self.screen.get_height() + self.shift_cycle[self.shift_state]

	# Check if collided with anything
	def check_collide(self, sprite):
		pygame.sprite.collide_mask(self, sprite)

	# Draw sprite to game display
	def draw(self):
		rotated_image = pygame.transform.rotate(self.image, self.rotation)
		self.screen.blit(rotated_image, (self.x, self.y))

	@property
	def rect(self):
		return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

class Pipe(Sprite):
	"""
	Pipe sprite which are game obstacles.
	(Top and bottom pair)
	"""
	# Initialize pipe (randomly generated)
	def __init__(self, x):
		self.screen = pygame.display.get_surface()
		self.screen_height = self.screen.get_height()
		self.gap = 100 
		self.x = x

		# Sprite images
		pipe = pygame.image.load('assets/pipe.png').convert_alpha()

		# Randomly generate pipe pair
		midpoint = random.randrange(int(0.45*self.screen_height), int(0.7*self.screen_height))
		upper = midpoint - pipe.get_height() - self.gap/2
		lower = midpoint + self.gap/2
		self.y = upper

		# Create surface and mask
		self.image = pygame.Surface((pipe.get_width(), self.screen_height)).convert_alpha()
		self.image.fill((0, 0, 0, 0))
		self.image.blit(pipe, (0, lower))
		self.image.blit(pygame.transform.rotate(pipe, 180), (0, upper))
		self.mask = pygame.mask.from_surface(self.image)

	# Update pipe position (continually shift 4 pixels left)
	def update(self):
		self.x -= 4

	# Draw sprite to game display
	def draw(self):
		self.screen.blit(self.image, (self.x, self.y))

	@property
	def rect(self):
		return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class Base(Sprite):
	"""
	Ground sprite, which is a game obstacle.
	"""
	# Initialize base
	def __init__(self):
		# Sprite and mask
		self.screen = pygame.display.get_surface() 
		self.image = pygame.image.load('assets/base.png').convert_alpha()
		self.mask = pygame.mask.from_surface(self.image)
		
		# Position paramaters
		self.x = 0
		self.y = self.screen.get_height() - self.image.get_height()
		self.max_shift = self.image.get_width() - self.screen.get_width()

	# Update base (continually shift by 4 pixels and loop)
	def update(self):
		self.x = -((-self.x + 4) % self.max_shift)

	# Draw sprite to game display
	def draw(self):
		self.screen.blit(self.image, (self.x, self.y))

	@property
	def rect(self):
		return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


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


class Game():
	"""
	The game entry point.
	Handles initialization, graphics, and main loops.
	"""
	# Initialize the game
	def __init__(self, width=288, height=512):
		pygame.init()
		self.fps = 30
		self.width, self.height = width, height
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Flappy Bird')

		# Load in sprites
		self.bg = pygame.image.load('assets/background.png').convert_alpha()
		self.msg = pygame.image.load('assets/start_msg.png').convert_alpha()
		self.player = Bird()
		self.base = Base()
		self.pipes = []
		self.score = Score()

	# Start the game (show welcome screen)
	def welcome_loop(self):
		i = 1
		while True:
			# Wait for key event
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
				if event.type == KEYDOWN and event.key == K_SPACE:
					return

			# Update player (flap, y_oscillation)
			if i % 5 == 0:
				self.player.change_flap_state()
			self.player.oscillate()

			# Shift base
			self.base.update()

			# Draw sprites on screen
			self.screen.blit(self.bg, (0,0))
			self.screen.blit(self.msg, (0,0))
			self.base.draw()
			self.player.draw()
			pygame.display.flip()
			
			# Increment
			self.clock.tick(self.fps)
			i += 1

	def main_loop(self):
		# Add two pipes
		self.pipes.append(Pipe(self.width*2))
		self.pipes.append(Pipe(self.width*2.5))

		# Start the game
		i = 1
		while True:
			# Event detection
			key_press = False
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
				if event.type == KEYDOWN and event.key == K_SPACE:
					key_press = True

			# Check for collisions
			collide_pipe = any([self.player.check_collide(pipe) for pipe in self.pipes])
			collide_base = self.player.check_collide(self.base)
			print(collide_pipe, collide_base)
			if collide_pipe or collide_base:
				print("DONE")
				return

			# Check if we made it through a pipe, then add +1 to score
			for pipe in self.pipes:
				if pipe.x == self.player.x:
					self.score.update() 

			# Update base sprite
			self.base.update()

			# Update player sprite
			if i % 3 == 0:
				self.player.change_flap_state()
			self.player.update(key_press)

			# Update pipes 
			[pipe.update() for pipe in self.pipes]
			# Add pipe when pipe has almost shifted off screen
			if self.pipes[0].x == 0:
				self.pipes.append(Pipe(self.width+50))
			# Remove pipe that has shifted left off screen
			if self.pipes[0].x < -self.pipes[0].image.get_width():
				self.pipes.pop(0)

			# Draw sprites
			self.screen.blit(self.bg, (0,0))
			[pipe.draw() for pipe in self.pipes]
			self.base.draw()
			self.player.draw()
			self.score.draw()
			pygame.display.flip()

			# Increment
			self.clock.tick(self.fps)
			i += 1

	def game_over(self):
		self.screen.blit(self.bg, (0,0))
		[pipe.draw() for pipe in self.pipes]
		self.base.draw()
		self.player.draw()
		self.score.draw()

# Script entry point
if __name__ == '__main__':
	g = Game()
	g.welcome_loop()
	g.main_loop()
	g.game_over()