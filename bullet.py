import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #create a bullet rect at(0,0) and the correct the position.
        self.rect =pygame.Rect(0,0, self.settings.bullet_width,
                               self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """MOve the bullets up the screen"""
        #update the decimal value position of the screen
        self.y -= self.settings.bullet_speed
        #update rect position
        self.rect.y = self.y

    def draw_bullets(self):
        """Draw the bullets on the screen"""
        pygame.draw.rect(self.screen, self.color,self.rect)