import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A class the manage bullets fored from spaceship """

    def __init__(self, ai_game):
        """ Create bullet obj at ships current position """
        super().__init__()   # run __init__ from parent class and get all attributes & methods
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        self.color = self.settings.bullet_color

        # Create bullet rect at (0,0) which is top-left corner of rect and then set correct position
        self.rect = pygame.Rect(0,0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop  # align start of bullet from midtop of ship

        # store the bullet's position as a decimal value
        self.y = float(self.rect.y)


    def update(self):
        """ MOve the bullet up the screen  """    
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """ Draw the bullet to the screen """ 
        pygame.draw.rect(self.screen, self.color, self.rect)   