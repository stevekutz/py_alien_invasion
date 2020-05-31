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

- NOTE: The game can be run from virtual environment via `python3 alien_invasion.py`

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
                # updates entire display
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
            """ Initialize ship to self and instance of current AlienInvasion class  """
            self.screen = ai_game.screen
            self.screen_rect = ai_game.screen.get_rect()

            # Load ship image and get its rect
            self.image = pygame.image.load('images/ship2.bmp')
            self.rect = self.image.get_rect()

            # start each new ship at bottom center of surface (e.g. display screen)
            self.rect.midbottom = self.screen_rect.midbottom

        def blitme(self):
            """ Draw the ship at its current location """
            # blit() draws one image onto another
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

    # the self.ship instance is assigned to give Ship access to all game resourses via self parameter
    self.ship = Ship(self)
    ...

    ...
    self.screen.fill(self.settings.bg_color)
    self.ship.blitme()
    ...
    ~~~

5) Refactor the `run_game` method
- `_check_events` and `_update_screen` methods are used to simplify `run_game`
    ~~~ py
        def run_game(self):
            """Start main loop in game"""
            while True:
                self._check_events()  # check event listener
                self._update_screen() # refresh screen

        def _check_events(self):
            # create event listener to watch keyboard or mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # detects is any key is pressed
                    if event.key == pygame.K_RIGHT:


        def _update_screen(self):
            """ Update images """
            # Redraw screen during each pass through the loop
            # a surface obj is created via self.screen
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # Redraw screen during each pass through the loop
            # a surface obj is created via self.screen
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            
            # make most recent screen drawn visible
            # updates entire display
            pygame.display.flip()
    ~~~

6) Implement ability to move ship

- modify the `run_game` module to include `self.ship.update()` in `alien_invasion.py`

    ~~~ py
        def run_game(self):
            """Start main loop in game"""
            while True:
                self._check_events()  # check event listener
                self.ship.update()  # update position
                self._update_screen() # refresh screen
    ~~~

- update the `_check_events` of `alien_invasion`

~~~ py
    def _check_events(self):
        # create event listener to watch keyboard or mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True  # move ship to the right
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True   # move ship to the left

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False   # moving right key released, stop moving
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False   # moving left key released, stop moving  
~~~

- add moving left & right functionality to the `update` method of `ship.py`

~~~ py
    def update(self):
        """ Update the ship position based on the movement flag  """    
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1    

    def blitme(self):
~~~

7) Adjust ship speed to use float values

- add `self.settings` to `ship.py`
    ~~~ py
    def __init__(self,ai_game):
            """ Initialize ship to self and instance of current AlienInvasion class  """
            self.screen = ai_game.screen
            self.settings = ai_game.settings
            self.screen_rect = ai_game.screen.get_rect()
    ~~~

-  at bottom of `__init__` add `self.x`  

~~~ py
     # store ship position as float
     self.x = float(self.rect.x)
~~~

- improve the `update` method to keep ship on screen in `ship.py`

    ~~~ py
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
    ~~~

8) Refactor `_check_events` and add helper methods in `alein_invasion.py`  

    ~~~ py
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
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = True  # move ship to the right
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True   # move ship to the left
            elif event.key == pygame.K_q:      # quit is Q is pressed
                sys.exit()    

        def _check_keyup_events(self, event):
            """ respond to changes in direction """
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False   # moving right key released, stop moving
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False   # moving left key released, stop moving

    ~~~
