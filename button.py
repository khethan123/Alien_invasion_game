import pygame.font

class Button():

    def __init__(self, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and the properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (133,19, 169)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont('Arail', 48)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center # screen center

        # The button message needs to be prepped only once.
        self.prep_msg(msg)
    
    def prep_msg(self, msg):
        """Turn msg into a rendered image & center the text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                         self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center # button center

    def draw_button(self):
        # Draw a blank button and then draw message.
        self.screen.fill(self.button_color, self.rect) # a colored rectangle.
        self.screen.blit(self.msg_image, self.msg_image_rect) # upon which image is placed.