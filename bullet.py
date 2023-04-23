import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Класс для управления снарядами выпущенными кораблем."""

    def __init__(self, ai_game, pos):
        """создает объект снарядов в текущей позиции корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/bullet.bmp').convert_alpha()
        self.pos = pos

        # Создание снаряда в позиции (0,0) и назначение правильной позиции.
        # bullet 1 # прямоугольник инициализ. в коорд (0,0)
        self.rect = self.image.get_rect()

        if self.pos == 'midleft':
            # в этой строке перемещается в середину прямоуг коробля
            self.rect.bottomleft = ai_game.rect.midleft
        elif self.pos == 'midright':
            self.rect.bottomright = ai_game.rect.midright
        # переменной присваевается веществ значение
        self.y_1 = float(self.rect.y)

    def update(self):
        """Перемещает снаряд вверх по экрану."""
        # Обновление позиции снарядов в вещественном формате.
        # движение вверх (уменьшение коорд по оси Y)
        self.y_1 -= self.settings.bullet_speed
        # Обновление позиции снарядов.
        self.rect.y = self.y_1
        self.destroy()

    def destroy(self):
        """уничтожение при пересечении граници"""
        screen_rect = self.screen.get_rect()
        if self.rect.y <= -50 or self.rect.y >= screen_rect.bottom:
            self.kill()

    def draw_bullet(self):
        #"""Вывод снаряда на экран"""
        pygame.draw.rect(
            self.screen, self.rect)  # рисует прямоугольник на экране
