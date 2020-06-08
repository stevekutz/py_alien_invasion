### Alien Invastion

#### Project Setup
1) Create virtual environment

~~~ bash 
python3 -m venv v_env
~~~

2) Activate virtual environment

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
- pygame allows `FULLSCREEN` mode
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
        ###  run in 1200 x 800 mode
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) 
        
        ### run in fullscreen mode
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
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
            
            # make most recent screen drawn visible
            # updates entire display
            pygame.display.flip()
    ~~~

1) Implement ability to move ship

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

9) Add attributes for bullets in `settings.py`

    ~~~ py
    # Bullet settings
    self.bullet_speed = 1.0
    self.bullet_width = 3
    self.bullet_height = 15
    self.bullet_color = (60,60,60)
    ~~~

10) Create `Bullet` class

    ~~~ py
    import pygame
    from pygame.sprite import Sprite

    class Bullet(Sprite):
        """ A class the manage bullets fored from spaceship """

        def __init__(self, ai_game):
            """ Create bullet obj at ships current position """
            super().__init__()   # run __init__ from parent class and get all attributes & methods
            self.screen = ai_game.screen
            self.settings = ai_game.settings 
            self.color = self.settings.bullet_color

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
    ~~~

#### Add Aliens

1) Create `alien` class

    ~~~ py
    import pygame
    from pygame.sprite import Sprite


    class Alien(Sprite):
        """ Class for single alien in fleet """

        def __init__(self, ai_game):
            """ Initialize alien and start position """
            super().__init__()
            self.screen = ai_game.screen

            # Load alien image and set rect attribute
            self.image = pygame.image.load('images/alien.bmp')
            self.rect = self.image.get_rect()

            # Start each new alien at top of screen
            self.rect.x = self.rect.width
            self.rect.y = self.rect.height

            # Store alien's horizontal position as float
            self.x = float(self.rect.x)
    ~~~

2) Update `alien_invaion.py` to render alien

- add import for `Alien` class

    ~~~ py
    from bullet import Bullet
    from alien import Alien
    ~~~

- update  `__init__`

    ~~~ py
    # create instance of alien
    self.aliens = pygame.sprite.Group()
    self._create_fleet()
    ~~~

- create `_create_fleet` method

    ~~~ py
    def _create_fleet(self):
        """ Create a fleet of aliens """
        alien = Alien(self)
        self.aliens.add(alien)
    ~~~

- add to `_update_screen` to draw alien

    ~~~ py
    for bullet in self.bullets.sprites():
        bullet.draw_bullet()

    # call draw method to render aliens
    self.aliens.draw(self.screen)
    ~~~

3) Refactor `alien_invasion.py` to render fleet of aliens

- `_create_fleet` calls upon a helper function `_create_alien`
- the number of rows and aliens per row is calculated based on whether 800 x 1200 OR FULLSCREEN mode is used
- debug code is added to see how fleet is rendered
    ~~~ py
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

        # detemine total number of aliens per row & total number of rows 
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
    ~~~

4) Add alien settings to `settings.py`

    ~~~ py
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction   `1 is to the right` & `-1 is to the left`
        self.fleet_direction = 1
    ~~~

5) add `_update_aliens` method to `alien_invasion`

    ~~~ py
        def _update_aliens(self):
            """ Verify if fleet at edges. if so, change position of fleet """
            self._check_fleet_edges()

            self.aliens.update()
    ~~~

6) Add `check_edges` and `update` to `alien.py`    
- this helps set up how to change direction when alien fleet detects edges of screen
- `alien.rect` returns `rect = <rect(x, y, width, height)> `
- 1200 x 800 screen size, the fleet will change direction as follow from debug code
    ~~~ bash
            NOW self.rect.right  1200
            NOW screen_rect.right  1200
            NOW self.rect.left  1140
    alien.rect BEFORE <rect(1140, 58, 60, 58)>
    direction BEFORE  1
    direction AFTER  -1
    Change in y is  68
            NOW self.rect.right  60
            NOW screen_rect.right  1200
            NOW self.rect.left  0
    alien.rect BEFORE <rect(0, 68, 60, 58)>
    direction BEFORE  -1
    direction AFTER  1
    Change in y is  78
            NOW self.rect.right  1200
            NOW screen_rect.right  1200
            NOW self.rect.left  1140
    alien.rect BEFORE <re
    ~~~


    ~~~ py
        def _check_fleet_edges(self):
            """ Determine if fleet hits edge of screen and respond  """
            for alien in self.aliens.sprites():
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
    ~~~

7) Update `update_bullets` in `alien_invasion.py` to detect if bullets hit an alien and add new method `_check_bullet_alien_collisions`
- the sprite positions are checked for overlap
- aliens and bullet will dissappear if collision occurs

    ~~~ py
        def _update_bullets(self):
            """  Update position of bullets to get rid of bullets that have exited screen """
            # Remove bullets that have reached top of screen
            self.bullets.update()    ## MOVED HERE !!!!!!
            
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
                # print(len(self.bullets)) 

            self._check_bullet_alien_collisions()
    ~~~

    ~~~ py
        def _check_bullet_alien_collisions(self):
            """ Handles hits to fleet """
            collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
            
            # # print out collisions dictionary
            # for item in collisions:
            #     print("key = {}, value = {}".format(item, collisions[item]))

            if not self.aliens:
                # Destroy bullets and create new fleet
                self.bullets.empty()
                self._create_fleet() 
    ~~~

#### Set up game scoring

1) Add the following to `_update_aliens` to check for alien-ship collisions

    ~~~ py
    class GameStats:
        """ Track statistics for alien invasion  """

        def __init__(self, ai_game):
            self.settings = ai_game.settings 
            self.reset_stats()
            self.game_active = True

        def reset_stats(self):
            self.ships_left = self.settings.ship_limit
    ~~~

2) Create a new file `game_stats.py`
    ~~~ py
    class GameStats:
        """ Track statistics for alien invasion  """

        def __init__(self, ai_game):
            self.settings = ai_game.settings 
            self.reset_stats()
        
        def reset_stats(self):
            self.ships_left = self.settings.ship_limit
    ~~~

3) In `settings.py` add  3 ship limit
    ~~~ py
        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3
    ~~~

4) Update `alien_invasion.py`
- import `GameStats` & `sleep`
- create instance with in `__init__`
  
    ~~~ py
    ...
    from game_stats import GameStats
    from time import slee
    ...
        pygame.display.set_caption("Alien_Invasion")

        # Create instance of game statistics
        self.stats = GameStats(self)
    ...
    ~~~

1) Create `_ship_hit` method

    ~~~ py
    def _ship_hit(self):
        """ Respond to ship being hit by alien """
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1

            # Remove remaining aliens & bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and ship at start location
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False  
    ~~~

2) Add `_ship_hit` method to `update_aliens`

    ~~~ py
    def _update_aliens(self):
    """ Verify if fleet at edges. if so, change position of fleet """
    self._check_fleet_edges()

    self.aliens.update()
    if pygame.sprite.spritecollideany(self.ship, self.aliens) != None :
        print("SHIP Hit !")
        self._ship_hit()
    ~~~

3) Add `center_ship` method to `ship.py`

    ~~~ py
        def center_ship(self):
            """ Center ship on screen """
            self.rect.midbottom = self.screen_rect.midbottom
            self.x = float(self.rect.x)
    ~~~

4) Add `_check_aliens_bottom` to `alien_invasion`

    ~~~ py
        def _check_aliens_bottom(self):
            """ Verify if aliends reach bottom od screen """
            screen_rect = self.screen.get_rect()
            for alien in self.aliens.sprites():
                if alien.rect.bottom >= screen_rect.bottom:
                    self._ship_hit()
                    break
    ~~~

5) Add call to `_check_aliens_bottom` to `update_aliens` method

    ~~~ py
        def _update_aliens(self):
            """ Verify if fleet at edges. if so, change position of fleet """
            self._check_fleet_edges()

            self.aliens.update()
            if pygame.sprite.spritecollideany(self.ship, self.aliens) != None :
                print("SHIP Hit !")
                self._ship_hit()

            # Verify if aliens reach the bottom of the screen
            self._check_aliens_bottom() 
    ~~~

6)  Add flag to `__init__ `    