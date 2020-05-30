import sys

import pygame
# from pygame.locals import *

from settings import Settings

class AlienInvasion:
    
    def __init__(self):
        "Initialize game & resources"
        pygame.init()   # intializes background settings
        self.settings = Settings()

        # the self.screen obj creates a `surface` that represents game screen where elements can be drawn
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) 
        pygame.display.set_caption("Alien_Invasion")

        # set background color
        self.bg_color = (230, 230, 230)

    def run_game(self):
        "Start main loop in game"
        while True:
            # create event listener to watch keyboard or mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw screen during each pass through the loop
            # a surface obj is created via self.screen
            self.screen.fill(self.settings.bg_color)

            # make most recent screen drawn visible
            pygame.display.flip()

if __name__ == '__main__':    
    # make a game instance & run game
    ai = AlienInvasion()
    ai.run_game()                