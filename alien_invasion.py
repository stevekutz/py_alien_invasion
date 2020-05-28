import sys

import pygame

class AlienInvasion:
    
    def __init__(self):
        "Initialize game & resources"
        pygame.init()

        self.screen = pygame.display.set_mode(1200, 800)
        pygame.display.set_caption("Alien_Invasion")

        # set background color
        self.bg_color = (230, 230, 230)

    def run_game(self):
        "Start main loop in game"
        while True:
            # watch keyboard or events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw screen during each pass through the loop
            self.screen.fill(self.bg_color)

            # make most recent screen drawn visible
            pygame.display.flip()

    if __name__ == '__main__':
        # make a game instance & run game
        ai = AlienInvasion()
        ai.run_game()                