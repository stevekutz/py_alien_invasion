import sys

import pygame
# from pygame.locals import *

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    
    def __init__(self):
        """Initialize game & resources"""
        pygame.init()   # intializes background settings
        self.settings = Settings()

        # the self.screen obj creates a `surface` that represents game screen where elements can be drawn
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) 
        pygame.display.set_caption("Alien_Invasion")

        # the self.ship instance is assigned to give Ship access to all game resourses via self parameter
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # similar to a list with extra features

        # set background color
        # self.bg_color = (230, 230, 230)

    def run_game(self):
        """Start main loop in game"""
        while True:
            self._check_events()  # check event listener
            self.ship.update()  # update position
            self.bullets.update()  # will update each sprite in the group
            self._update_screen() # refresh screen

    def _check_events(self):
        # create event listener to watch keyboard or mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
   
    def _check_keydown_events(self, event):
        """ Set directions for current movements """
        print('key pressed was ', (event))
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True  # move ship to the right
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True   # move ship to the left
        elif event.key == pygame.K_q:      # quit is Q is pressed
            sys.exit()    
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()    

    def _check_keyup_events(self, event):
        """ respond to changes in direction """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False   # moving right key released, stop moving
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False   # moving left key released, stop moving

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group """
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
        """ Update images """
        # Redraw screen during each pass through the loop
        # a surface obj is created via self.screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # make most recent screen drawn visible
        # updates entire display
        pygame.display.flip()

if __name__ == '__main__':    
    # make a game instance & run game
    print("__name__ is", __name__)
    print("pygame.__name__ is", pygame.__name__)
    ai = AlienInvasion()
    ai.run_game()                