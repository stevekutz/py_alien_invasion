import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Class for single alien in fleet """

    def __init__(self, ai_game):
        """ Initialize alien and start position """
        super().__init__()
        self.screen = ai_game.screen

        # Load alien image and set rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien at top of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's horizontal position as float
        self.x = float(self.rect.x)

