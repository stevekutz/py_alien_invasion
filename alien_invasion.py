import sys

import pygame
# from pygame.locals import *

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    
    def __init__(self):
        """Initialize game & resources"""
        pygame.init()   # intializes background settings
        self.settings = Settings()

        # the self.screen obj creates a `surface` that represents game screen where elements can be drawn
        ###  run in 1200 x 800 mode
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) 
        
        ### run in fullscreen mode
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien_Invasion")

        # the self.ship instance is assigned to give Ship access to all game resourses via self parameter
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # similar to a list with extra features

        # create instance of alien
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start main loop in game"""
        while True:
            self._check_events()  # check event listener
            self.ship.update()  # update position
            self.bullets.update()  # will update each sprite in the group
            self._update_bullets()    

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
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """  Update position of bullets to get rid of bullets that have exited screen """
        # Remove bullets that have reached top of screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            print(len(self.bullets)) 

    def _create_fleet(self):
        """ Create a fleet of aliens """
        alien = Alien(self)  # used for calculations, NOT part of fleet
        
        # Get dimensions for ship & alien
        ship_height = self.ship.rect.height
        alien_width, alien_height = alien.rect.size
        
        # find available space for aliens to fit on screen
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        available_space_x = self.settings.screen_width - ( 2 * alien_width )
        
        # detemine total number of aliens per row & total number of rows 
        number_aliens_x = available_space_x // ( 2 * alien_width )
        number_rows = available_space_y // ( 2 * alien_height )

        # Create rows of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
            # Fill row with aliens
                self._create_alien(alien_number, row_number )

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        # Each alien row starts below at twice the height of an alien ship
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number 
        self.aliens.add(alien)

    def _update_screen(self):
        """ Update images """
        # Redraw screen during each pass through the loop
        # a surface obj is created via self.screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # call draw method to render alien
        self.aliens.draw(self.screen)

        # make most recent screen drawn visible
        # updates entire display
        pygame.display.flip()

if __name__ == '__main__':    
    # make a game instance & run game
    print("__name__ is", __name__)
    print("pygame.__name__ is", pygame.__name__)
    ai = AlienInvasion()
    ai.run_game()                