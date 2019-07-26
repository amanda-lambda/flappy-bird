import pygame


class GameText():

    def __init__(self):
        """
        Initialize a new text instance. 
        This handles any global game text, game scores, as well as menu text.
        """
        # Game screen
        self.screen = pygame.display.get_surface() 

        # Sprites
        self.msg_start = pygame.image.load('assets/start_msg.png').convert_alpha()
        self.msg_end = pygame.image.load('assets/end_msg.png').convert_alpha()
        self.digits = []
        for i in range(10):
            self.digits.append(pygame.image.load('assets/%i.png' % i).convert_alpha())

        # Locations of sprites
        self.x_msg_end = (self.screen.get_width() - self.msg_end.get_width()) / 2
        self.y_msg_end = 0.3 * self.screen.get_height()

        digit_gap = 50
        self.x_level_1 = (self.screen.get_width() - self.digits[0].get_width()) / 2
        self.x_level_0 = self.x_level_1 - digit_gap - self.digits[1].get_width()
        self.x_level_2 = self.x_level_1 + digit_gap + self.digits[1].get_width()
        self.y_level = 0.7 * self.screen.get_height()

        self.y_score = self.screen.get_height()*0.1

        # The currently selected level
        self.selected_level = 1

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
            self.screen.blit(self.msg_start, (0,0))
            self.screen.blit(self.digits[0], (self.x_level_0, self.y_level))
            self.screen.blit(self.digits[1], (self.x_level_1, self.y_level))
            self.screen.blit(self.digits[2], (self.x_level_2, self.y_level))

        # In main mode, display the score
        if mode == 'main':
            self.draw_score()

        # In game_over mode, display the end text and score
        if mode == 'game_over':
            self.screen.blit(self.msg_end, (self.x_msg_end, self.y_msg_end))
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
        x = (self.screen.get_width() - score_width) / 2
        for i in score_digits:
            self.screen.blit(self.digits[i], (x, self.y_score))
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
            if self.selected_level == 2:
                return self.selected_level
            self.selected_level += 1

        if 'left_arrow' in keys_pressed:
            if self.selected_level == 0:
                return self.selected_level
            self.selected_level -= 1

        return self.selected_level


    def update_score(self):
        """
        Update the game score. 
        We call this function every time the bird makes it through a pair of 
        pipes, so we increment the score by 1.
        """
        self.score += 1
