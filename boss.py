import pygame
from settings import Settings


class Boss(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.ships = ai_game.ship

        self.image = pygame.image.load('images/boss.bmp').convert_alpha()

        self.rect = self.image.get_rect(midtop=(600, -650))

        self.x = float(self.rect.x)  # ось X
        self.y = float(self.rect.y)  # ось Y

    def check_edges(self):
        """Возвращает True, если пришелец находится у края экрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def boss_flys_away(self):
        """Если игрок пытается облететь флот ряд кораблей стремительно улетает игрок получает -1 НР"""
        for ship in self.ships:
            if ship.rect.bottom < self.rect.bottom:
                self.rect.y += 1

    def update(self):
        if self.rect.y < 50:
            self.y += 0.2
            self.rect.y = self.y
        else:
            self.x += (self.settings.boss_speed *
                       self.settings.boss_direction)
            self.rect.x = self.x
        self.boss_flys_away()
        # self.boss_movement()
