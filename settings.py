class Settings:
    """Class to store all settings for Alien Invasion"""
    def __init__(self):
        "Initialize game settings"
        "Screen"
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)    # defined as RGB colors
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet direction   `1 is to the right` & `-1 is to the left`
        self.fleet_direction = 1
