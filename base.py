import pygame
from pygame.locals import *
from pygame.sprite import Sprite


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