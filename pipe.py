import random

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

# TODO: Easy, medium, hard settings for pipes, make it based off of bird height
# TODO: Collision with pipes
# TODO: pipes not populating

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
        midpoint = random.randrange(int(0.5*self.screen_height), int(0.65*self.screen_height))
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