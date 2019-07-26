import random

import pygame
from pygame.locals import *
from pygame.sprite import Sprite

# Import sprites
from bird import Bird
from pipe import Pipe
from base import Base
from game_text import GameText

# Import utility functions
from utils import *


class Game():

    def __init__(self, width=288, height=512):
        """
        Initialize the game.

        Argument:
            width (int): width of game screen in pixels
            height (int): height of game screen in pixels
        """
        pygame.init()

        # Frame rate of the game
        self.fps = 30

        # Game clock which ticks according to the game framerate
        self.clock = pygame.time.Clock()

        # Set up display
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Flappy Bird')

        # Set up game objects
        self.bg = pygame.image.load('assets/background.png').convert_alpha()
        self.game_text = GameText()
        self.player = Bird(0.2*width, 0.45*height)
        self.base = Base()
        self.pipes = []

        # List of flags indicating whether or not the pass through of the pipe 
        # pairs has been counted yet
        self.pipe_counted = [False, False]

        # Set game difficulty as [0,1,2] = [easy, medium, or hard]
        self.level = 2



    def update_display(self, mode):
        """
        Update the game display with the game background and sprites. 

        In the 'welcome' mode, we should additionally display the welcome text. 
        In the 'end' mode, we should display the game over text.

        Arguments:
            mode (str): Can be one of [welcome, main, game_over]
        """
        # Draw the background
        self.screen.blit(self.bg, (0,0))

        # Draw the sprites
        for pipe in self.pipes:
            pipe.draw()
        self.base.draw()
        self.player.draw()

        # Draw any messages
        self.game_text.draw(mode)

        # Update the entire game display
        pygame.display.flip()


    def welcome_loop(self):
        """
        Show the welcome screen.
        """
        while True:
            # This loop listens for events (input from user). If the user 
            # presses the space bar, exit the welcome_loop and begin the game.
            keys_pressed = listen()
            if 'spacebar' in keys_pressed:
                return
            if 'left_arrow' or 'right_arrow' in keys_pressed:
                self.level = self.game_text.update_level(keys_pressed)

            # Update player sprite, which should be oscillating up and down
            # and flappying its wings periodically
            self.player.update()

            # Update the base sprite, which should be scrolling past.
            self.base.update()

            # Update the display
            self.update_display('welcome')
            
            # Increment the clock
            self.clock.tick(self.fps)


    def main_loop(self):
        """
        The main game loop. 

        The user tries to accrue as many points as possible by passing the bird
        sprite through the pipe pairs. Bird movement is controlled using the 
        space bar. The game ends when the bird hits an obstacle (a pipe pair or 
        the ground).
        """
        # Tell bird sprite the game has started. It will stop oscillating.
        self.player.set_game_play_mode(True)

        # Start with two pipes off screen
        self.pipes = [Pipe(self.width*1.5, self.level), Pipe(self.width*2, self.level)] 

        # Start the game
        while True:

            # Check for key presses (user input). 
            spacebar_press = False
            keys_pressed = listen()
            if 'spacebar' in keys_pressed:
                spacebar_press = True

            # Check to see if the player bird has collided with any of the pipe
            # pairs or the base. If so, exit the game loop.
            obstacles = self.pipes + [self.base]
            if self.player.check_collide(obstacles):
                return

            # If the player passes through a pipe, add +1 to score
            for i in range(len(self.pipes)):
                if not self.pipe_counted[i]:
                    if self.pipes[i].x < self.player.x:
                        self.game_text.update_score() 
                        self.pipe_counted[i] = True

            # Update base sprite
            self.base.update()

            # Update player sprite
            self.player.update(spacebar_press)

            # Update pipes
            for pipe in self.pipes:
                pipe.update() 

            # Add a new pipe when one of the pipes has shifted off screen
            if self.pipes[0].x < 0 and len(self.pipes) < 3:
                self.pipes.append(Pipe(self.width+50, self.level))
                self.pipe_counted.append(False)

            # Remove pipe that has shifted left off screen
            if self.pipes[0].x < -self.pipes[0].image.get_width():
                self.pipes.pop(0)
                self.pipe_counted.pop(0)

            # Update the game display
            self.update_display('main')

            # Increment
            self.clock.tick(self.fps)


    def game_over(self):
        """
        The game over loop.
        Display the player's final score and the "Game Over" message.
        """
        while True:
            listen()
            self.update_display('game_over')



# Script entry point
if __name__ == '__main__':
    g = Game()
    g.welcome_loop()
    g.main_loop()
    g.game_over()