import pygame
from settings import Settings


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        self.settings = Settings()
        self.image = pygame.image.load('images/laser.bmp').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.height_y_constraint = screen_height
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def destroy(self):
        """Уничтожение при пересечении границ"""
        if self.y <= -50 or self.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        """Обновление Laser"""
        self.y -= self.speed
        self.rect.y = self.y
        self.destroy()
