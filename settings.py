class Settings:
    """Class to store all settings for Alien Invasion"""
    def __init__(self):
        "Initialize game STATIC settings"
        "Screen"
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)    # defined as RGB colors
        
        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)       # (60,60,60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        # Game speedup
        self.speedup_scale = 1.2

        # Score increase scale
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize settings that change during gameplay """
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet direction   `1 is to the right` & `-1 is to the left`
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """ Increase speed settings """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)


# # Laser Blast settings
# self.laser_speed = 10.0
# self.laser_width = 5
# self.laser_height = 400
# self.laser_color = (10,210,50)
# self.laser_fire_allowed = True