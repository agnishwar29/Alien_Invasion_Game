import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import ALien
from game_stats import Gamestats
from buttons import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """Initialize the game, and create game resorces"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.stats = Gamestats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()



        self._create_fleet()

        #Make the play button
        self.play_button = Button(self, "PLay")

        #Make difficulty buttons
        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """Make buttons that allow player to select their difficulty"""
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self,"Medium")
        self.hard_button = Button(self, "Hard")

        #Position buttons
        self.easy_button.rect.top = (
            self.play_button.rect.top + 2.5*self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (
                self.easy_button.rect.top + 1.5 * self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = (
                self.medium_button.rect.top + 1.5 * self.medium_button.rect.height)
        self.hard_button._update_msg_position()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.update_aliens()
                self.ship.update()
                self._update_screen()
                self._update_bullets()


            self._update_screen()
    def _update_bullets(self):
            #get rid of bullets that have disappeared.
            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            self._check_bullet_alien_collision()



    def _check_bullet_alien_collision(self):
        # Check for any bullets that have hit aliens.
        # if so get rid of the bullets
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()


            #increase level
            self.stats.level += 1
            self.sb.prep_level()
    def _ship_hit(self):
        """Respond to the ship being hit by an alien """
        #decrement ship's left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            #self.sb.prep_ships()

            #Get rid of any remaining ullets and aliens
            self.aliens.empty()
            self.bullets.empty()

            #Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship( )

            #pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_aliens_bottom(self):
        """Check if any alien reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
    def update_aliens(self):
        """Update the positions of the aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #look for alien hitting the bottom of the screen
        self.check_aliens_bottom()


            #watch for keyboard and mouse events.
    def _check_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
                    self._check_difficulty_buttons(mouse_pos)
    def _check_play_button(self, mouse_pos):
        """Start a new game when player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self.start_game()
    def _check_difficulty_buttons(self, mouse_pos):
        """Set the appropriate difficulty level"""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if easy_button_clicked:
            self.settings.difficulty_level = 'easy'
        elif medium_button_clicked:
            self.settings.difficulty_level = 'medium'
        elif hard_button_clicked:
            self.settings.difficulty_level = 'hard'

    def start_game(self):
        """Start the game"""
        # reset the game settings
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        #self.sb.prep_ships()
        # Get rid of any bullets or aliens
        self.aliens.empty()
        self.bullets.empty()

        # Create new fleet
        self._create_fleet()
        self.ship.center_ship()

        # Hide the mouse courser
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right =True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left =True
            self.ship.rect.x += 1
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
            self.ship.rect.y += 1
        elif event.key == pygame.K_p:
            self.stats.reset_stats()
            self.stats.game_active = True


        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
           self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False


    def _fire_bullet(self):
        """Create a new bullet and it to the groups"""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create the fleet of Aliens"""
        #Create an  alien and find the numbers in a row

        alien = ALien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - alien_width
        number_aliens_x = available_space_x // (2* alien_width)

        #Detremine the number of rows of aliens that fit the screen
        ship_height = self.ship.rect.height

        available_space_y = (self.settings.screen_height -
                             ( 2 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens:
        for row_number in range(number_rows):
            #create the first row of aliens
            for alien_number in range(number_aliens_x):
                #create an alien and place it in the row
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        alien = ALien(self)
        alien_width, alien_height = alien.rect.size

        alien.x = alien_width + 2 * alien_width * alien_number

        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond the entire fleet when it reaches the edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the direction of the fleet"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
            self.screen.fill(self.settings.bg_color)
            self.ship.blitime()
            #make the most recently drawin screen visible

            for bullet in self.bullets.sprites():
                bullet.draw_bullets()

            self.aliens.draw(self.screen)
            self.sb.show_score()
            #Draw the play button if the game is imactive
            if not self.stats.game_active:
                self.play_button.draw_button()
                self.easy_button.draw_button()
                self.medium_button.draw_button()
                self.hard_button.draw_button()


            pygame.display.flip()

    """def _close_game(self):
        Save high score and exit.
        saved_high_score = self.stats.get_saved_high_score()
        if self.stats.high_score > saved_high_score:
            with open('high_score.json', 'w') as f:
                json.dump(self.stats.high_score, f)
        sys.exit()"""

if __name__ == '__main__':
    #make a game instance,and run the game.
    ai =AlienInvasion()
    ai.run_game()
