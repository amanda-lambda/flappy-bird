import pygame
from pygame.locals import *

def listen_spacebar():
    """
    Listen for a spacebar keypress.
    
    Returns:
        bool: True if spacebar pressed, False otherwise
    """
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_SPACE:
            return True
    return False


def listen_quit():
    """
    Listen for a quit keypress.
    
    Returns:
        bool: True if exit initiated, False otherwise
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
