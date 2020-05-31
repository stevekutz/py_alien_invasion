import pygame

class Ship:
    """A class to manage the ship """

    # 
    def __init__(self,ai_game):
        """ Initialize ship to self and instance of current AlienInvasion class  """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Movement flag
        self.moving_right = False
        self.moving_left = False

        # Load ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # start each new ship at bottom center of surface (e.g. display screen)
        self.rect.midbottom = self.screen_rect.midbottom

        # store ship position as float
        self.x = float(self.rect.x)

    def update(self):
        """ Update the ship position based on the movement flag  """    
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.x += 1
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            # self.rect.x -= 1   
            self.x -= self.settings.ship_speed      

        # update the rect obj
        self.rect.x = self.x    

    def blitme(self):
        """ Draw the ship at its current location """
        # blit() draws one image onto another
        self.screen.blit(self.image, self.rect)
