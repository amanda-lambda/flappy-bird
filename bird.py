import pygame
from pygame.locals import *
from pygame.sprite import Sprite

class Bird(Sprite):
    """
    Bird sprite, controlled by the player.
    """
    # Initialize player
    def __init__(self):
        self.screen = pygame.display.get_surface() 
        self.x, self.y = 0.2*self.screen.get_width(), 0.45*self.screen.get_height()
        self.rotation = 0
        self.velocity = -9

        self.state = 0
        self.shift_state = 0
        self.shift_cycle = [0,1,2,3,4,5,6,7,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-7,-6,-5,-4,-3,-2,-1]

        # Sprite images
        self.im_upflap = pygame.image.load('assets/bird_upflap.png').convert_alpha()
        self.im_midflap = pygame.image.load('assets/bird_midflap.png').convert_alpha()
        self.im_downflap = pygame.image.load('assets/bird_downflap.png').convert_alpha()
        self.im_cycle = [self.im_upflap, self.im_midflap, self.im_downflap, self.im_midflap]
        self.image = self.im_cycle[self.state]

        # Masks
        self.mask_upflap = pygame.mask.from_surface(self.im_upflap)
        self.mask_midflap = pygame.mask.from_surface(self.im_midflap)
        self.mask_downflap = pygame.mask.from_surface(self.im_downflap)
        self.mask_cycle = [self.mask_upflap, self.mask_midflap, self.mask_downflap, self.mask_midflap]
        self.mask = self.mask_cycle[self.state]

    def update(self, key_press=False):
        if key_press:
            self.rotation = 45
            self.velocity = -9
            self.y += self.velocity
        else:
            # Rotate 3 degrees CW, with threshold at 20
            self.rotation -= 3
            if self.rotation < 20:
                self.rotation = 20
            # Update velocity, with terminal velocity at 10
            self.velocity += 1
            if self.velocity > 10:
                self.velocity = 10
            # Update position
            self.y += self.velocity

    def change_flap_state(self):
        self.state = (self.state + 1) % len(self.im_cycle)
        self.image = self.im_cycle[self.state]
        self.mask = self.mask_cycle[self.state]

    # Oscillate up and down during start screen
    def oscillate(self):
        self.shift_state = (self.shift_state + 1) % len(self.shift_cycle)
        self.y = 0.45*self.screen.get_height() + self.shift_cycle[self.shift_state]

    # Check if collided with anything
    def check_collide(self, sprite):
        pygame.sprite.collide_mask(self, sprite)

    # Draw sprite to game display
    def draw(self):
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.screen.blit(rotated_image, (self.x, self.y))

    @property
    def rect(self):
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())