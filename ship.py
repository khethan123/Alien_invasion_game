import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize the Ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the ship image and let's get its rect.
        self.image = pygame.image.load("ship.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom centre of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store decimal value for the ship's center as centerx takes only int values
        self.center_x = float(self.rect.centerx)
        self.center_y = float(self.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_center = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center_x += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center_x -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.center_y -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center_y += self.ai_settings.ship_speed_factor

        # Move ship to center if 'c' key is pressed
        if self.moving_center:
            self.center_x = self.screen_rect.centerx
            self.center_y = self.screen_rect.centery
            self.moving_center = False

        # Update the rect object from self values
        self.rect.centerx = self.center_x
        self.rect.y = self.center_y

    def blitme(self):
        """Draw the ship at it's current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.center_x = self.screen_rect.centerx
        self.center_y = self.screen_rect.bottom - 110

