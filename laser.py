import pygame
from pygame.sprite import Sprite

class LaserBlast(Sprite):
    """ A powerful laster blast that takes time to recharge before firing again """
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.laser_color
        

        # Create laser
        self.rect = pygame.Rect(0,0, self.settings.laser_width, self.settings.laser_height)
        self.rect.midtop = ai_game.ship.rect.midtop  # align start of laser from midtop of ship
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.laser_speed   # change to new position value
        self.rect.y = self.y            # update new position value

    def draw_laser(self):
        # draw until at top of screen
        pygame.draw.rect(self.screen, self.color, self.rect)