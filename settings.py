class Settings:
    def __init__(self):
        """Initialise the game's static settings"""
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0,0,0)
        self.ship_speed = 2
        self.ship_limit = 3

        #Bullet settings
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height =15
        self.bullet_color = (255,0,0)


        #Alien Settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 5
        #How quickly the game speeds up
        self.speedup_scale = 1.1

        self.difficulty_level = 'medium'

        self.initialize_dynamic_settings()
        #fleet direction 1 represents the movement to the right.


        self.fleet_direction = 1

    def initialize_dynamic_settings(self):
        """Initialize the settings that change throughout the game"""
        if self.difficulty_level == 'easy':
            self.ship_limit = 4
            self.ship_speed = 2
            self.bullet_speed = 1
            self.alien_speed = 1
            self.bullet_width = 2
        elif self.difficulty_level == 'medium':
            self.ship_limit = 3
            self.ship_speed = 4
            self.bullet_speed = 3
            self.alien_speed = 2
            self.bullet_width = 3
        elif self.difficulty_level == 'hard':
            self.ship_limit = 2
            self.ship_speed = 6
            self.bullet_speed = 4
            self.alien_speed = 5
            self.bullet_width = 4

        self.fleet_direction = 1

        #scoring
        self.alien_points = 10

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_width += 0.9
    def set_difficulty(self, diff_setting):
        if diff_setting == 'easy':
            print('easy')
        elif diff_setting == 'medium':
            pass
        elif diff_setting == 'hard':
            pass