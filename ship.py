import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    """A class to manage the ship"""
    def __init__(self,ai_game):
        """Initialize the ship ans set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship image and get its rect
        self.image = pygame.image.load(
            'E:\ALien Invasion\Screenshot 2021-04-12 152908.jpg')
        self.rect = self.image.get_rect()

        #start the ship at the center bottom of the screen

        self.rect.midbottom = self.screen_rect.midbottom
        #self.rect.centery = self.screen_rect.centery



        #store a decimal value for the ships horixontal movement
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        #update rect object from self.x
        self.rect.x = self.x
        self.rect.y = self.y


    def blitime(self):
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.bottom = self.screen_rect.bottom
        self.x = float(self.rect.x)
