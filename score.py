import pygame
from pygame.sprite import Sprite

# TODO: Check, should score be popping up at game end?
class Score(Sprite):

    def __init__(self):
        """
        Initialize a new score sprite instance. 
        """
        self.screen = pygame.display.get_surface() 
        self.y = self.screen.get_height()*0.1

        # Score value
        self.value = 0

        # Sprites
        self.digits = []
        for i in range(10):
            self.digits.append(pygame.image.load('assets/%i.png' % i).convert_alpha())


    def update(self):
        """
        Update the game score. 
        We call this function every time the bird makes it through a pair of 
        pipes, so we increment the score by 1.
        """
        self.value += 1


    def draw(self):
        """
        Draw the sprite to the game display.
        """
        # Extract a list of the individual digits in the score
        score_digits = [int(i) for i in list(str(self.value))]

        # Find the total width (in pixels) of the score
        score_width = sum([self.digits[i].get_width() for i in score_digits])

        # Blit the score digits onto the screen
        x = (self.screen.get_width() - score_width) / 2
        for i in score_digits:
            self.screen.blit(self.digits[i], (x, self.y))
            x += self.digits[i].get_width()

        # print(self.value, score_digits, score_width, x, "*********")