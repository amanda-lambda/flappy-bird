import pygame


class GameText():

    def __init__(self):
        """
        Initialize a new text instance. 
        This handles any global game text, game scores, as well as menu text.
        """
        # Game surface
        self.surface = pygame.display.get_surface() 

        # Sprites
        self.msg_start = pygame.image.load('assets/start_msg.png').convert_alpha()
        self.msg_end = pygame.image.load('assets/end_msg.png').convert_alpha()
        self.digits = []
        for i in range(10):
            self.digits.append(pygame.image.load('assets/%i.png' % i).convert_alpha())

        # Location of game_over message
        self.x_msg_end = (self.surface.get_width() - self.msg_end.get_width()) / 2
        self.y_msg_end = 0.3 * self.surface.get_height()

        # Location of level selection digits. We want them to be evently spaced
        # apart
        digit_gap = 50
        x_level_1 = (self.surface.get_width() - self.digits[0].get_width()) / 2
        x_level_0 = x_level_1 - digit_gap - self.digits[1].get_width()
        x_level_2 = x_level_1 + digit_gap + self.digits[1].get_width()
        self.x_level = [x_level_0, x_level_1, x_level_2]
        self.y_level = 0.7 * self.surface.get_height()

        # The location of the score
        self.y_score = self.surface.get_height()*0.1

        # The currently selected level
        self.level = 1
        self.level_box_height = self.digits[0].get_height() + 10
        self.level_box_width = self.digits[0].get_width() + 10

        # Score value
        self.score = 0


    def draw(self, mode):
        """
        Draw any required text to the screen. 
        In 'welcome' mode, we'll need to display the starting instructions as 
        well as the level selection menu. In 'game_over' mode, we'll need to
        display the game over text. 

        Arguments:
            mode (str): One of 'welcome', 'main', or 'game_over'
        """
        # In welcome mode, display the start instructions
        if mode == 'welcome':
            # Blit the welcome message
            self.surface.blit(self.msg_start, (0, 0))
            # Blit the green box highlighting the selected level
            pygame.draw.rect(self.surface, (0, 0, 0), 
                (self.x_level[self.level]-5, self.y_level-5, self.level_box_width, self.level_box_height), 5)
            # Blit the levels
            self.surface.blit(self.digits[0], (self.x_level[0], self.y_level))
            self.surface.blit(self.digits[1], (self.x_level[1], self.y_level))
            self.surface.blit(self.digits[2], (self.x_level[2], self.y_level))

        # In main mode, display the score
        if mode == 'main':
            self.draw_score()

        # In game_over mode, display the end text and score
        if mode == 'game_over':
            self.surface.blit(self.msg_end, (self.x_msg_end, self.y_msg_end))
            self.draw_score()


    def draw_score(self):
        """
        Draw the score to the game display.
        """
        # Extract a list of the individual digits in the score
        score_digits = [int(i) for i in list(str(self.score))]

        # Find the total width (in pixels) of the score
        score_width = sum([self.digits[i].get_width() for i in score_digits])

        # Blit the score digits onto the screen
        x = (self.surface.get_width() - score_width) / 2
        for i in score_digits:
            self.surface.blit(self.digits[i], (x, self.y_score))
            x += self.digits[i].get_width()


    def update_level(self, keys_pressed):
        """
        Update the selected level.

        Arguments:
            keys_pressed

        Returns:
            int: the selected level, where [0,1,2] corresponds to 
            ['easy', 'medium', 'hard'], respectively.
        """
        if 'right_arrow' in keys_pressed:
            if self.level == 2:
                return self.level
            self.level += 1

        if 'left_arrow' in keys_pressed:
            if self.level == 0:
                return self.level
            self.level -= 1

        return self.level


    def update_score(self):
        """
        Update the game score. 
        We call this function every time the bird makes it through a pair of 
        pipes, so we increment the score by 1.
        """
        self.score += 1
