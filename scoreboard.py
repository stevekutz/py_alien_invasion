import pygame.font

class Scoreboard:
    """ Score tracking class """

    def __init__(self, ai_game):
        """ Init scoring attributes """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scorring info   
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the intial score image
        self.prep_score()


    def prep_score(self):
        """  Render score values into screen images """    
        score_str = str(self.stats.score)    # convert to string for display
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display score in top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20  # offset 20 px from right edge
        self.score_rect.top =  20 # offset 20 from top edge

    def show_score(self):
        """ Draw score to the screen """    
        self.screen.blit(self.score_image, self.score_rect)