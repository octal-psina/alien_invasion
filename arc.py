import pygame
from settings import Settings


class Arc(pygame.sprite.Sprite):
    def __init__(self, pos,):
        super().__init__()
        self.settings = Settings()

        self.image = pygame.image.load('images/arc.bmp').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        self.speed = self.settings.arc_speed
        self.height_y_constraint = self.settings.screen_hight
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def destroy(self):
        """Уничтожение при пересечении границ"""
        if self.y <= -50 or self.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        """Обновление Laser"""
        self.y += self.speed
        self.rect.y = self.y
        # self.laser_sound.play()
        self.destroy()
