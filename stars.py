import pygame
from settings import Settings
from pygame.sprite import Sprite


class Stars(Sprite):

    def __init__(self, color, x, y, screen_height):
        """Инициализирует пришельца и задает его начальную позицию"""
        super().__init__()

        # загрузка изображения звезды назнач атрибута rect
        file_path = "images/" + color + ".bmp"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.height_y_constraint = screen_height
        self.y = float(self.rect.y)

    def update(self):
        """обновление Stars"""
        self.y += 0.3
        self.rect.y = self.y
        self.destroy()

    def destroy(self):
        """уничтожение при пересечении граници"""
        if self.y <= -50 or self.y >= self.height_y_constraint + 50:
            self.y = 0
