import sys

from game_stats import GameStats
from time import sleep

import pygame
# from pygame.locals import *

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
# from laser import LaserBlast

from game_stats import GameStats
from button import Button

from scoreboard import Scoreboard

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

        # Create instance of game statistics & scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # the self.ship instance is assigned to give Ship access to all game resourses via self parameter
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # similar to a list with extra features

        # create instance of alien
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Create a Play button
        self.play_button = Button(self, "Play !")

# # create instance of laser_blast
# self.laser = pygame.sprite.Group()

    def run_game(self):
        """Start main loop in game"""
        while True:
            self._check_events()  # check event listener
           
            if self.stats.game_active:
                self.ship.update()  # update position
                # self.bullets.update()  # will update each sprite in the group
                self._update_bullets()    
                self._update_aliens()

#            self.laser.update()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """ Start a new game when player clicks Play """ 
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game settings
            self.settings.initialize_dynamic_settings()

            # Reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # Remove any remaining aliends and bullets
            self.aliens.empty()       
            self.bullets.empty()

            # Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()   

            # Hide the mouse cursor when inside of game window
            pygame.mouse.set_visible(False) 
   
    def _check_keydown_events(self, event):
        """ Set directions for current movements """
        # print('key pressed was ', (event))
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True  # move ship to the right
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True   # move ship to the left
        elif event.key == pygame.K_q:      # quit is Q is pressed
            sys.exit()    
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
# elif event.key == pygame.K_l:
#     self._fire_laser()        

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

    def _fire_laser(self):
        print("LASER FIRED")
# print(self.settings.laser_fire_allowed)
# if self.settings.laser_fire_allowed:
#     #laser_blast = LaserBlast(self)
#     laser_blast = Bullet(self)

#     laser_blast.color = self.settings.laser_color
#     self.bullets.add(laser_blast)

    def _update_bullets(self):
        """  Update position of bullets to get rid of bullets that have exited screen """
        # Remove bullets that have reached top of screen
        self.bullets.update()    ## MOVED HERE !!!!!!
        
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # print(len(self.bullets)) 

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Handles hits to fleet """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                print(f' Collision values() is {aliens}')
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # # print out collisions dictionary
        # for item in collisions:
        #     print("key = {}, value = {}".format(item, collisions[item]))

        if not self.aliens:
            # Destroy bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()    
            self.settings.increase_speed()

    def _update_aliens(self):
        """ Verify if fleet at edges. if so, change position of fleet """
        self._check_fleet_edges()

        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens) != None :
            print("SHIP Hit !")
            self._ship_hit()

        # Verify if aliens reach the bottom of the screen
        self._check_aliens_bottom()    

    def _ship_hit(self):
        """ Respond to ship being hit by alien """
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1

            # Remove remianing aliens & bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and ship at start location
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False   
            pygame.mouse.set_visible(True) 

    def _create_fleet(self):
        """ Create a fleet of aliens """
        alien = Alien(self)  # used for calculations, NOT part of fleet
            # <Alien sprite(in 0 groups)>

        # Get dimensions for ship & alien
        ship_height = self.ship.rect.height
        alien_width, alien_height = alien.rect.size   # (60, 58)
        
        # find available space for aliens to fit on screen
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        available_space_x = self.settings.screen_width - ( 2 * alien_width )
            # available_space_y = (800) - (3 * 58) - 48    = 578
            # available_space_x = 1200 - (2 * 60)    = 1080

        # determine total number of aliens per row & total number of rows 
        number_aliens_x = available_space_x // ( 2 * alien_width )
        number_rows = available_space_y // ( 2 * alien_height )
            # number_aliens_x = 1080 // (2 * 60)   = 9
            # number_rows = 578 // (2 * 58)  = 4

        # Create rows of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
            # Fill row with aliens
                self._create_alien(alien_number, row_number )

        # rect = <rect(x, y, width, height)>       <rect(180, 58, 60, 58)>
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
            # alien.x = 60 + (2 * 60 * 0..9)   alien.x = 60.0, 180.0, 300.0, 420.0, ...
        alien.rect.x = alien.x
        # Each alien row starts below at twice the height of an alien ship
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number 
            # alien.rect.y =   58 + (2 * 58 * 0..4)                     58, 174, 290 
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """ Determine if fleet hits edge of screen and respond  """
        for alien in self.aliens.sprites():
            #  if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            if alien.check_edges():
                print("alien.rect BEFORE", alien.rect) # rect = <rect(x, y, width, height)> 
                print("direction BEFORE ", self.settings.fleet_direction)
                self._change_fleet_direction()
                print("direction AFTER ", self.settings.fleet_direction)
                print("Change in y is ", alien.rect.y)
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change direction """  
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1          

    def _check_aliens_bottom(self):
        """ Verify if aliends reach bottom od screen """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


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

        # Draw scoreboard info
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

# for blast in self.laser.sprites():
#     blast.draw_laser()

        # make most recent screen drawn visible
        # updates entire display
        pygame.display.flip()

if __name__ == '__main__':    
    # make a game instance & run game
    print("__name__ is", __name__)
    print("pygame.__name__ is", pygame.__name__)
    ai = AlienInvasion()
    ai.run_game()                