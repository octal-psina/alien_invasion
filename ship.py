import pygame
from settings import Settings
from bullet import Bullet


class Ship(pygame.sprite.Sprite):
    """класс для управления кораблем"""

    def __init__(self, ai_game):  # ссылка на экхемпляр класса  AlienInvasion
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = Settings()

        # Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/ship_9.bmp').convert_alpha()
        self.rect = self.image.get_rect()
        self.bullets = pygame.sprite.Group()

        self.speed = [1, 1]  # для метода fly_ship()

        self.lasers = pygame.sprite.Group()
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 300
        self.hit = False
        #self.win = False

        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom
        # Сохранение вещесвенной координаты центра корабля
        self.x = float(self.rect.x)  # ось X
        self.y = float(self.rect.y)  # ось Y

        self.bullet_sound = pygame.mixer.Sound('music/laser1.wav')
        self.bullet_sound.set_volume(0.5)

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
                # print(current_time)

    def get_input(self):
        """Обновление позиции корабля"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.x += self.settings.ship_speed

        elif keys[pygame.K_LEFT]:
            self.x -= self.settings.ship_speed

        elif keys[pygame.K_UP] and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed

        elif keys[pygame.K_DOWN] and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        if keys[pygame.K_SPACE] and self.ready:
            self.fire_bullet()
            self.ready = False
            # print(self.ready)
            self.laser_time = pygame.time.get_ticks()

        # Обновление атрибута rect на основании self.x
        self.rect.x = self.x
        self.rect.y = self.y

        # Teleport ship to the other side
        if self.rect.left > self.screen_rect.right:  # Справа на лево
            self.x = 0

        elif self.rect.right < self.screen_rect.left:  # Cлева на право
            self.x = 1130

    def fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        new_bullet1 = Bullet(self, "midleft")
        new_bullet2 = Bullet(self, "midright")
        self.bullets.add(new_bullet1, new_bullet2)
        self.bullet_sound.play()
        # print(len(self.bullets))

    def fly_ship(self):
        """Корабль перемещается по экрану."""

        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.settings.screen_width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > self.settings.screen_hight:
            self.speed[1] = -self.speed[1]

        #self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """ Обновление Ship"""
        self.get_input()
        self.bullets.update()
        self.recharge()

        if self.hit == True:
            self.center_ship()
            self.hit = False

        # if self.win == True:
            # self.fly_ship()
