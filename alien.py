import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Class for single alien in fleet """

    def __init__(self, ai_game):
        """ Initialize alien and start position """
        super().__init__()
        self.screen = ai_game.screen    # <Surface(1200x800x32 SW)>
        self.settings = ai_game.settings    # 

        # Load alien image and set rect attribute
        self.image = pygame.image.load('images/alien.bmp')   # <Surface(60x58x24 SW)>
        self.rect = self.image.get_rect()   # = <rect(0, 0, 60, 58)

        # Start each new alien at top of screen
        # rect looks at (x,y) coordinate of top left corner
        self.rect.x = self.rect.width   # 60
        self.rect.y = self.rect.height  # 0
            # now self.rect = <rect(60, 0, 60, 58)

        # Store alien's horizontal position as float
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """ Move alien to the right """
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

