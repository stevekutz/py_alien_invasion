import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Class for single alien in fleet """

    def __init__(self, ai_game):
        """ Initialize alien and start position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image and set rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien at top of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

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

