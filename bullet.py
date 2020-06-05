import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A class the manage bullets from spaceship """

    def __init__(self, ai_game):
        """ Create bullet obj at ships current position """
        super().__init__()   # run __init__ from parent class and get all attributes & methods
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        self.color = self.settings.bullet_color
        # self.reach = self.settings.bullet_height

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

# class LaserBlast(Bullet):
#     """ A powerful laster blast that takes time to recharge before firing again """
#     def __init__(self, ai_game, screen , settings, color):
#         super().__init__(ai_game, screen, settings, color)
#         self.screen = ai_game.screen
#         self.settings = ai_game.settings


#         self.color = self.settings.laser_color
        

#         # Create laser
#         self.rect = pygame.Rect(0,0, self.settings.laser_width, self.settings.laser_height)
#         self.rect.midtop = ai_game.ship.rect.midtop  # align start of laser from midtop of ship
#         self.y = float(self.rect.y)

#     def update(self):
#         self.y -= self.settings.laser_speed   # change to new position value
#         self.rect.y = self.y            # update new position value

#     def draw_laser(self):
#         # draw until at top of screen
#         pygame.draw.rect(self.screen, self.color, self.rect)        