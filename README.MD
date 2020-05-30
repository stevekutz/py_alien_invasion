### Alien Invastion

#### Project Setup
1) Create virutal environment

~~~ bash 
python3 -m venv v_env
~~~

2) Activate virutal environment

~~~ bash
source v_env/bin/activate
~~~

3) Install `pygame` from virtual environment

~~~ bash
python3 -m pip install -U pygame==2.0.0.dev6 --user
~~~



#### Build Classes

1) Create `alien_invasion.py` 

- import `sys` (allows exiting of game) & `pygame` (contains game functionality) 

    ~~~ py
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
    ~~~

2) Create a `Settings` class in `settings.py` 

    ~~~ py
    class Settings:
        "Class to store all settings for Alien Invasion"
        def __init__(self):
            "Initialize game settings"
            "Screen"
            self.screen_width = 1200
            self.screen_height = 800
            self.bg_color = (230, 230, 230)    # defined as RGB colors
    ~~~

3) Create `Ship` class

    ~~~ py
    import pygame

    class Ship:
        """A class to manage the ship """

        # 
        def __init__(self,ai_game):
            self.screen = ai_game.screen
            self.screen_rect = ai_game.screen.get_rect()

            # Load ship image and get its rect
            self.image = pygame.image.load('images/ship2.bmp')
            self.rect = self.image.get_rect()

            # start each new ship at bottom center of surface (e.g. display screen)
            self.rect.midbottom = self.screen_rect.midbottom

        def blitme(self):
            """ Draw the ship at its current location """
            self.screen.blit(self.image, self.rect)
    ~~~

4) Add `Ship` to `alien_invasion.py`

    ~~~ py
    ...
    from settings import Settings
    from ship import Ship
    ...

    ...
    pygame.display.set_caption("Alien_Invasion")

    self.ship = Ship(self)
    ...

    ...
    self.screen.fill(self.settings.bg_color)
    self.ship.blitme()
    ...
    ~~~
