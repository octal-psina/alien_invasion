import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс, представляющий одного пришельца."""

    def __init__(self, ai_game, color):
        """Инициализирует пришельца и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ships = ai_game.ship

        file_path = "images/" + color + ".bmp"
        # Загрузка изображения пришельца и назнач атрибута rect.
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение горизонтальной позиции в вещественном числе по коорд (X)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # цвет пришельцев
        if color == 'green':
            self.value = 100
        elif color == 'red':
            self.value = 200
        elif color == 'blue':
            self.value = 300

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def destroy(self):
        """Уничтожение при пересечение границ экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.y <= -50 or self.rect.y >= screen_rect.bottom:
            self.kill()

    def row_flys_away(self):
        """Если игрок пытается облететь флот ряд кораблей стремительно улетает игрок получает -1 НР"""
        for ship in self.ships:
            if ship.rect.bottom < self.rect.bottom:
                self.rect.y += 1

    def update(self):
        """Обновление Alien"""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
        self.destroy()
        self.row_flys_away()
