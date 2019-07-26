import sys
import pygame
from pygame.locals import *


def listen():
    """
    Listen and log key presses from user (spacebar, arrow keys). 
    Will automatically exit game if it gets a quit signal.

    Returns:
        list (str): a list of the names of the keys pressed
    """
    keypress = []

    for event in pygame.event.get():

        # If spacebar is pressed
        if event.type == KEYDOWN and event.key == K_SPACE:
            keypress.append('spacebar')

        # If arrows pressed
        if event.type == KEYDOWN and event.key == K_RIGHT:
            keypress.append('right_arrow')

        if event.type == KEYDOWN and event.key == K_LEFT:
            keypress.append('left_arrow')

        # If quit triggered
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    return keypress


 
def midpoint_to_upper_lh_corner():
    """
    A method that converts from the midpoint to the edge.
    """
    return