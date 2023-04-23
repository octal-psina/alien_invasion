import pygame


class Settings():
    """Класс для хранения настроек Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_hight = 800
        self.bg_color = (24, 24, 56)
        self.ship_speed = 0.5
        self.ship_lives = 3
        self.score = 0

        # Пармаетры снарядов
        self.bullet_speed = 1
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (250, 237, 39)

        # Настройки пришельцев
        self.alien_speed = 0.09
        self.fleet_drop_speed = 5
        self.fleet_direction = 1
        self.alien_laser_speed = -0.6

        # Настройки босс
        self.boss_lives = 300
        self.boss_speed = 0.4
        self.boss_drop_speed = 10
        self.boss_direction = 1
        self.boss_laser_speed = -0.5
        self.arc_speed = 1

    def updt_speed(self):
        """"Увеличение скорости пришельцев"""
        self.alien_speed += 0.01
        self.fleet_drop_speed += 0.1
        self.alien_laser_speed -= 0.02
