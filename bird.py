import pygame
from pygame.locals import *
from pygame.sprite import Sprite

#Todo: customizable sprites

class Bird(Sprite):

    def __init__(self, x_init, y_init):
        """
        Initialize a new bird sprite instance.
        Arguments:
            x_init (int): x-coordinate of starting position 
            y_init (int): y-coordinate of starting position
        """
        # Game surface
        self.surface = pygame.display.get_surface() 

        # Game frame counter
        self.count = 0

        # Whether we are in game play
        self.game_play = False

        # Bird position
        self.x = x_init
        self.y = y_init
        self.y_init = y_init

        # Bird dynamics - angle of rotation
        self.angle = 0 
        self.angle_threshold = 20
        self.angle_flap = 45
        self.rate_of_rotation = 3

        # Bird dynamics - velocity along the y axis
        self.velocity_y = -9
        self.velocity_flap = -9
        self.velocity_terminal = 10

        # Sprite images
        im_upflap = pygame.image.load('assets/bird_upflap.png').convert_alpha()
        im_midflap = pygame.image.load('assets/bird_midflap.png').convert_alpha()
        im_downflap = pygame.image.load('assets/bird_downflap.png').convert_alpha()

        # Sprite masks
        mask_upflap = pygame.mask.from_surface(im_upflap)
        mask_midflap = pygame.mask.from_surface(im_midflap)
        mask_downflap = pygame.mask.from_surface(im_downflap)

        # Oscillation state parameters
        self.osc_cycle = [0,1,2,3,4,5,6,7,8,7,6,5,4,3,2,1,0,
                          -1,-2,-3,-4,-5,-6,-7,-8,-7,-6,-5,-4,-3,-2,-1]

        # Flap state parameters
        self.im_cycle = [im_upflap, im_midflap, im_downflap, im_midflap]
        self.mask_cycle = [mask_upflap, mask_midflap, mask_downflap, mask_midflap]
        self.image = self.im_cycle[self.count]
        self.mask = self.mask_cycle[self.count]


    def update(self, key_press=False):
        """
        Update the bird sprite. 

        The default behavior in the game welcome screen is for the bird sprite 
        to oscillate up and down and flap its wings. 

        During game play, the bird sprite will respond to user keyboard input. 
        If the space bar is pressed, the bird  will tilt and climb up the 
        screen. If there is no key press, then the bird will fall due to the 
        influence of gravity.

        Arguments:
            key_press (bool): whether or not the space bar has been pressed
        """
        # If we are in game play, then respond to user key presses
        if self.game_play:

            # Update the bird's angle of rotation, velocity, and y position
            # according to whether there was a key press (wing flap)
            self.update_angle(key_press)
            self.update_velocity(key_press)
            self.y += self.velocity_y

        # Every 5 frames, update the player bird by changing the wing flap
        if self.count % 5 == 0:
            self.change_flap_state()

        # Every frame, have the player bird oscillate up and down. This is only
        # done when the game is not in play, i.e. at the welcome screen.
        if not self.game_play:
            self.oscillate()

        # Update global game counter
        self.count += 1


    def update_angle(self, is_flap):
        """
        Adjust the angle of the bird sprite. 
        If the bird has flapped its wings, tilt upward. Else, slowly rotate 
        back to a neutral position.

        Arguments:
            is_flap (bool): whether or not the bird has flapped its wings
        """
        if is_flap:
            self.angle = self.angle_flap
        else:
            self.angle -= self.rate_of_rotation
            if self.angle < self.angle_threshold:
                self.angle = self.angle_threshold
    
    def update_velocity(self, is_flap):
        """
        Adjust the bird sprite's velocity.
        If the bird has flapped its wings, then climb upward. Else, slowly
        decrease the bird's velocity until it reaches terminal velocity.

        Arguments:
            is_flap (bool): whether or not the bird has flapped its wings
        """
        if is_flap:
            self.velocity_y = self.velocity_flap
        else:
            self.velocity_y += 1
            if self.velocity_y > self.velocity_terminal:
                self.velocity_y = self.velocity_terminal

    def change_flap_state(self):
        """
        Change the flap state.
        """
        flap_state = self.count % len(self.im_cycle)
        self.image = self.im_cycle[flap_state]
        self.mask = self.mask_cycle[flap_state]


    def oscillate(self):
        """
        Oscillate up and down.
        """
        osc_state = self.count % len(self.osc_cycle)
        self.y = self.y_init + self.osc_cycle[osc_state]


    def check_collide(self, sprite):
        """
        Check if the player sprite has collided with another sprite.
        The bird can collide with the pipes or the ground.

        Arguments:
            sprite (pygame.sprite or list): A sprite instance or a list of 
                sprite instances. All must have the rect property.

        Returns:
            bool: True if collision with sprite instance, False otherwise
        """
        if isinstance(sprite, list):
            for s in sprite:
                if pygame.sprite.collide_mask(self, s):
                    return True
            return False
        else: 
            return pygame.sprite.collide_mask(self, sprite)


    def draw(self):
        """Draw the sprite onto the game display."""
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.surface.blit(rotated_image, (self.x, self.y))


    def set_game_play_mode(self, is_playing):
        """
        Set the game play attribute. 

        Arguments:
            is_playing (bool): whether or not we are in game play mode
        """
        self.game_play = is_playing
        

    @property
    def rect(self):
        """
        This property is needed for pygame.sprite.collide_mask
        """
        return Rect(self.x, self.y, self.image.get_width(), self.image.get_height())