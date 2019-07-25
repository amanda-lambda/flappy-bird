import random

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

# Import sprites
from bird import Bird
from pipe import Pipe
from base import Base
from score import Score


class Game():
    """
    The game entry point.
    Handles initialization, graphics, and main loops.
    """

    def __init__(self, width=288, height=512):
        """Initialize the game.
        Args:
            width (int): width of game screen in pixels
            height (int): height of game screen in pixels
        """
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
        """Start the game (show welcome screen)"""
        # A counter for the number of frames which have elapsed so far
        i = 1
        while True:
            # This loop listens for events (input from user). If the user presses the 
            # space bar, exit from the welcome_loop and begin the game.
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return

            # Every 5 frames, update the player bird by changing the wing flap
            if i % 5 == 0:
                self.player.change_flap_state()

            # Every frame, have the player bird oscillate up and down.
            self.player.oscillate()

            # Every frame, update the base 
            self.base.update()

            # Draw sprites on screen
            self.screen.blit(self.bg, (0,0))
            self.screen.blit(self.msg, (0,0))
            self.base.draw()
            self.player.draw()
            pygame.display.flip()
            
            # Increment the clock
            self.clock.tick(self.fps)
            i += 1

    def main_loop(self):
        # Add two pipes to the screen
        self.pipes.append(Pipe(self.width*2))
        self.pipes.append(Pipe(self.width*2.5))

        # Start the game
        i = 1
        while True:
            # Check for key presses (user input). Set key_press to be true when 
            # the space bar is pressed
            key_press = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN and event.key == K_SPACE:
                    key_press = True

            # Check to see if the player bird had any collisions with the pipes
            collide_pipe = any([self.player.check_collide(pipe) for pipe in self.pipes])
            collide_base = self.player.check_collide(self.base)
            print(collide_pipe, collide_base)
            if collide_pipe or collide_base:
                print("DONE")
                return

            # If the player passes through a pipe, add +1 to score
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
            for pipe in self.pipes:
                pipe.update() 
            # Add pipe when pipe has almost shifted off screen
            if self.pipes[0].x == 0:
                print("Pipe has moved off screen")
                self.pipes.append(Pipe(self.width+50))
                print("Adding a new pipe at ", self.width+50)
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