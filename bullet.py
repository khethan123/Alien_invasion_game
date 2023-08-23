import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage all the bullets fired fromthe ship."""

    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the current ship's position."""
        super(Bullet, self).__init__()
        self.screen = screen

        # Let's crete a bullet at top left corner initially since we dont have a image ref.
        # i.e., (0, 0) and then set it to the correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Now let's store the bullet's y-co-ordinate as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet on the screen.
        self.y -= self.speed_factor
        # Now we must also update the rectangle position on the screen.
        self.rect.y = self.y

    def draw_bullets(self):
        """Draw the bullets on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
