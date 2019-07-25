import pygame
from pygame.locals import *
from pygame.sprite import Sprite


class Base(Sprite):
  
    # Initialize base
    def __init__(self):
        """
        Initialize the ground sprite.
        """
        # Game screen
        self.screen = pygame.display.get_surface() 

        # Sprite and mask
        self.image = pygame.image.load('assets/base.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        # Position 
        self.x = 0
        self.y = self.screen.get_height() - self.image.get_height()
        self.max_shift = self.image.get_width() - self.screen.get_width()


    def update(self):
        """
        Update the position of the base sprite.
        The base should continually shift by 4 pixels and loop.
        """
        self.x = -((-self.x + 4) % self.max_shift)


    def draw(self):
        """
        Draw the sprite to the game display.
        """
        self.screen.blit(self.image, (self.x, self.y))

    @property
    def rect(self):
        """
        This property is needed for pygame.sprite.collide_mask
        """
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())