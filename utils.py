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
