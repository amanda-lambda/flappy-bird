import random

import pygame
from pygame.locals import *
from pygame.sprite import Sprite


class Pipe(Sprite):

    def __init__(self, x_init, difficulty):
        """
        Initialize a new pipe pair sprite instance. 
        The pipe placement on the y-axis is randomly generated.

        Arguments:
            x_init (int): x-coordinate of starting position 
            difficulty (int): either 'easy', 'medium', or 'hard' = [0,1,2]. 
                Will determine the size of the gaps between pipes.
        """
        # Game surface
        self.surface = pygame.display.get_surface()
        screen_height = self.surface.get_height()

        # Pipe position 
        self.x = x_init

        # Size of gap between pipes (in pixels)
        if difficulty == 0:
            self.gap = 125
        elif difficulty == 1:
            self.gap = 100
        elif difficulty == 2:
            self.gap = 75

        # Sprite images
        pipe_lower = pygame.image.load('assets/pipe.png').convert_alpha()
        pipe_upper = pygame.transform.rotate(pipe_lower, 180)
        pipe_width = pipe_lower.get_width()
        pipe_height = pipe_lower.get_height()

        # Randomly generate coordinates for upper and lwer pipe
        midpoint = random.randrange(int(0.5*screen_height), 
                                    int(0.65*screen_height))
        y_upper = midpoint - pipe_height - self.gap/2
        y_lower = midpoint + self.gap/2
        self.y = y_upper

        # Create surface and mask
        self.image = pygame.Surface((pipe_width, screen_height)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.image.blit(pipe_lower, (0, y_lower))
        self.image.blit(pipe_upper, (0, y_upper))
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        """
        Update the pipe pair's x-position by continually shifting 4 pixels to
        the left.
        """
        self.x -= 4


    def draw(self):
        """
        Draw the sprite to the game display.
        """
        self.surface.blit(self.image, (self.x, self.y))

    @property
    def rect(self):
        """
        This property is needed for pygame.sprite.collide_mask
        """
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())