import pygame


class Ball(pygame.sprite.Sprite):
    """
    Class to keep track of a ball's location and vector.
    """

    def __init__(self):
        super().__init__()

        # Set up the image and rect attributes for Sprite
        self.image = pygame.Surface([25, 25])  # Adjust the size as needed
        self.image.fill((255, 255, 255))  # Default colour: white
        self.rect = self.image.get_rect()

        self.change_x = 0
        self.change_y = 0

    def update(self):
        """
        Update the position of the ball based on its velocity properties.
        """
        self.rect.x += self.change_x
        self.rect.y += self.change_y
