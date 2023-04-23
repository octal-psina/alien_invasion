import sys
from time import sleep

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from boss import Boss
from random import choice
from random import randint
from laser import Laser
from stars import Stars
from arc import Arc


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()

        # pygame.mixer.init() #инициаллизирует проигрыватель

        # Установки игры, экрана
        self.settings = Settings()
        # присвоин атриьуту чтобы использовать во всех методах игры
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_hight))
        pygame.display.set_caption("Alien Invasion")  # self.modul.parametr

        # Корабль игрока
        player = Ship(self)
        # создание спрайта корабля игрока!!
        self.ship = pygame.sprite.GroupSingle(player)
        # группа для хранения всех летящих снарядов
        self.bullets = pygame.sprite.Group()

        # Флот инопланетян
        self.aliens = pygame.sprite.Group()  # группа для хранения отрисованых пришельцев
        self.alien_lasers = pygame.sprite.Group()
        self._create_fleet()  # Создание флота пришельцев

        # Boss
        boss_ship = Boss(self)
        self.boss = pygame.sprite.GroupSingle(boss_ship)
        self.arc = pygame.sprite.Group()

        # Звезды
        self.stars = pygame.sprite.Group()
        self.star_setup(rows=15, cols=20)  # rows = 37, cols = 15

        # Шрифт
        self.font = pygame.font.Font('font/Righteous-Regular.ttf', 30)
        self.font_1 = pygame.font.Font('font/Righteous-Regular.ttf', 60)

        # Жизни
        self.live_surf = pygame.image.load('images/tool.bmp').convert_alpha()
        self.live_x_start_pos = self.settings.screen_width - \
            (self.live_surf.get_size()[0] * 2 + 90)

        # Музыка/звуки
        # загружает музыкальную композицию
        music = pygame.mixer.music.load("music/main.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)  # Запускает музакальный трек

        self.laser_sound = pygame.mixer.Sound("music/laser3.wav")
        self.laser_sound.set_volume(0.2)

        self.explosion_sound = pygame.mixer.Sound("music/epl1.wav")
        self.explosion_sound.set_volume(1.0)

    def run_game(self):  # управление основным процессом игры
        """Запуск основного цикла игры."""
        while True:
            self._check_events()  # Вспомогательный метод для управления событиями
            self.ship.update()  # Обновление позиции корабля
            self._update_boss()  # Обновлениее Boss
            self._update_aliens()  # Обновление aliens
            self.alien_lasers.update()  # Обновление alien_laser
            self.arc.update()  # Обновление arc(дуга босса)
            self.collision_checks()  # Проверка коллизий
            self.stars.update()  # Движение звезд
            self._update_sreen()  # Вспомогательный метод для обновлы экран

    # Звезды
    def star_setup(self, rows, cols, x_distance=1200, y_distance=80, x_offset=150, y_offset=30):
        """Установки звезд"""
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = randint(-1200, (row_index * x_distance)) + x_offset
                y = randint(-100, (col_index * y_distance)) + y_offset
                stars = (Stars('perpl', x, y, self.settings.screen_hight), Stars(
                    'white', x, y, self.settings.screen_hight), Stars('yellow', x, y, self.settings.screen_hight))
                stars_sprite = choice(stars)
                self.stars.add(stars_sprite)

    # Флот пришельцев
    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца
        # Пришелец не входит во флот просто шаблон для расчета рядов и поз. пришельца
        alien = Alien(self, "blue")
        alien_width, alien_height = alien.rect.size

        # Вычисление доступн пространства на оси X = ширина экрана - (2 * ширину_пришельца)
        #(для сохранения пустых интервалов по краям экрана)
        avaliable_space_space_x = self.settings.screen_width - alien_width

        # Количество пришельцев в ряду = доступн_пространство // (2 * ширину_пришельца)
        number_aliens_x = avaliable_space_space_x // (alien_width) - 8
        # print(number_aliens_x) вывод количества пришельцев в терминал

        # доступное пространство по оси Y  = высота экрана - (3 * высоту пришельца) - высота корабля
        available_space_y = (self.settings.screen_hight - (2 * alien_height))
        # количество рядов = доступное пространсто Y // (2* высоту_пришельца)
        number_rows = available_space_y // (2 * alien_height)
        #print(list(range(0, number_rows))[-1])
        # Создание флота пришельцев.
        # от нуля до номера последнего ряда
        for row_number in range(number_rows):
            # создание одного ряда пришельцев
            for alien_number in range(number_aliens_x):
                # Создание пришельца и размещение в ряду
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        if row_number == 0:
            alien = Alien(self, "blue")
        elif 1 <= row_number <= 2:
            alien = Alien(self, "red")
        else:
            alien = Alien(self, "green")
        alien_width, alien_height = alien.rect.size  # кортеж с парметрами пришельца
        alien_width = alien.rect.width  # определение ширины пришельца
        alien.x = alien_width * 0.3 + 2 * alien_width * \
            alien_number  # создается координата x для размещения
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height * 1 + 1.2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцами края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_directions()
                break

    def _change_fleet_directions(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """Обновление спрайта aliens с учетом условий"""
        self._check_fleet_edges()
        self.aliens.update()
        if self.settings.score <= 112000 and not self.aliens and self.settings.ship_lives > 0:
            # Уничтожение существующих снарядов и создание нового флота увеличение скорости его движения
            self.bullets.empty()
            self.settings.updt_speed()
            self._create_fleet()

    def alien_shoot(self):
        # Инопланетяне стрельба
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(
                random_alien.rect.center, self.settings.alien_laser_speed, self.settings.screen_hight)
            #laser_sprite1 = Laser(random_alien.rect.midleft,self.settings.alien_laser_speed,self.settings.screen_hight)
            self.alien_lasers.add(laser_sprite)  # ,laser_sprite1)
            self.laser_sound.play()
        # print(len(self.alien_lasers))

    # Boss
    def boss_shoot(self):
        """Стрельба лазером Boss"""
        if self.boss.sprites():
            for bos in self.boss.sprites():
                laser_1 = Laser(
                    bos.rect.midright, self.settings.alien_laser_speed, self.settings.screen_hight)
                laser_2 = Laser(
                    bos.rect.midleft, self.settings.alien_laser_speed, self.settings.screen_hight)
                laser_3 = Laser(
                    bos.rect.center, self.settings.alien_laser_speed, self.settings.screen_hight)
            self.alien_lasers.add(laser_1, laser_2, laser_3)
            self.laser_sound.play()

    def boss_arc(self):
        """Стрельба энергодугой Boss"""
        if self.boss.sprites():
            for bos in self.boss.sprites():
                arc = Arc(bos.rect.center)
            self.arc.add(arc)
            self.laser_sound.play()

    def _boss_check_fleet_edges(self):
        """Реагирует на достижение босса края экрана"""
        for bos in self.boss.sprites():
            if bos.check_edges():
                self._change_boss_directions()
                break

    def _change_boss_directions(self):
        """Снижение Boss и меняет направление флота"""
        for bos in self.boss.sprites():
            bos.rect.y += self.settings.boss_drop_speed
        self.settings.boss_direction *= -1

    def boss_destroyed(self):
        """Условия уничтожения Boss"""
        if self.settings.boss_lives <= 0:
            self.boss.empty()
            self.bullets.empty()
            self.alien_lasers.empty()

    def _update_boss(self):
        """Обновление Boss и условия для обновления"""
        if self.settings.score >= 112000 and not self.aliens:
            self._boss_check_fleet_edges()
            self.boss_destroyed()
            self.boss.update()

    # Проверка условий ивента
    def _check_events(self):
        """Обрабатывает нажатие клавиши и использ. мыши"""
        for event in pygame.event.get():  # получения доступа к событиям, обнаруженным Pygame
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
            if event.type == ALIENLASER:
                self.alien_shoot()
            if event.type == BOSSLASER:
                self.boss_shoot()
            if event.type == BOSSARC:
                self.boss_arc()

    def collision_checks(self):
        """Проверка коллизий"""
        # bullets
        for bullet in self.ship.sprite.bullets:
            aliens_hit = pygame.sprite.spritecollide(bullet, self.aliens, True)
            boss_hit = pygame.sprite.spritecollide(bullet, self.boss, False)
            if aliens_hit:
                for alien in aliens_hit:
                    self.settings.score += alien.value
                    #print(f'score = {self.settings.score}')
                bullet.kill()
                self.explosion_sound.play()

            if boss_hit:
                bullet.kill()
                self.settings.boss_lives -= 1
                print(f"bosslives = {self.settings.boss_lives}")
                self.explosion_sound.play()

        # aliens
        screen_rect = self.screen.get_rect()
        if self.aliens:
            for alien in self.aliens.sprites():
                if pygame.sprite.spritecollide(alien, self.ship, False):
                    alien.kill()
                    self._ship_hit()
                    self.explosion_sound.play()
                    sleep(0.3)

                if alien.rect.bottom >= screen_rect.bottom:
                    self._ship_hit()
                    sleep(0.05)
                    break

        # alien_lassers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.ship, False):
                    laser.kill()
                    self._ship_hit()
                    self.explosion_sound.play()
                    sleep(0.3)

        # boss
        if self.boss:
            for bos in self.boss.sprites():
                if pygame.sprite.spritecollide(bos, self.ship, False):
                    self.settings.boss_lives -= 1
                    print(f"bosslives = {self.settings.boss_lives}")
                    self.explosion_sound.play()
                    sleep(0.3)
                    self._ship_hit()

                if bos.rect.bottom >= screen_rect.bottom:
                    self.settings.ship_lives -= 3
        # arc
        if self.arc:
            for ar in self.arc:
                if pygame.sprite.spritecollide(ar, self.ship, False):
                    ar.kill()
                    self._ship_hit()
                    self.explosion_sound.play()
                    sleep(0.3)

    def _ship_hit(self):
        """Нанесении урона игроку"""
        self.settings.ship_lives -= 1
        #print(f'live = {self.settings.ship_lives}')
        for s in self.ship:
            s.hit = True
        if self.settings.score < 112000:
            self.aliens.empty()
            self.bullets.empty()
            self.alien_lasers.empty()
            self._create_fleet()

    def display_score(self):
        """Отображение очков игрока"""
        score_surf = self.font.render(
            f'score: {self.settings.score}', True, 'white')
        score_rect = score_surf.get_rect(topleft=(10, 0))
        self.screen.blit(score_surf, score_rect)

    def display_lives(self):
        """Отображение жизний игрока"""
        for live in range(self.settings.ship_lives):
            x = self.live_x_start_pos + \
                (live * (self.live_surf.get_size()[0] + 15))
            self.screen.blit(self.live_surf, (x, 8))

    def game_over_message(self):
        """В случае не выполнения условий для победы"""
        if self.settings.ship_lives <= 0:
            game_over_surf = self.font_1.render("GAME OVER", True, "white")
            game_over_surf_1 = self.font.render(
                "press 'q' to quit", True, 'white')
            game_over_rect = game_over_surf.get_rect(
                center=(self.settings.screen_width / 2, self.settings.screen_hight / 2))
            game_over_rect_1 = game_over_surf_1.get_rect(
                center=(self.settings.screen_width / 2, self.settings.screen_hight / 2 + 100))
            self.screen.blit(game_over_surf, game_over_rect)
            self.screen.blit(game_over_surf_1, game_over_rect_1)
            pygame.time.wait(500)

    def win_game_message(self):
        if self.settings.score >= 112000 and not self.boss:
            game_win_surf = self.font_1.render(
                "You saved the world!", True, "white")
            game_win_surf_1 = self.font.render(
                "press 'q' to quit", True, 'white')
            game_caption_surf = self.font.render(
                "shitty code: Alex,  designer: @mirmariiaa", True, 'white')
            game_caption_surf_1 = self.font.render(
                "music: Dance With the Dead - The Man Who Made a Monster", True, 'white')
            game_win_rect = game_win_surf.get_rect(
                center=(self.settings.screen_width / 2, self.settings.screen_hight / 2))
            game_win_rect_1 = game_win_surf_1.get_rect(
                center=(self.settings.screen_width / 2, self.settings.screen_hight / 2 + 100))
            game_caption_rect = game_caption_surf.get_rect(
                center=(self.settings.screen_width / 2, self.settings.screen_hight / 2 + 200))
            game_caption_rect_1 = game_caption_surf_1.get_rect(
                center=(self.settings.screen_width / 2, self.settings.screen_hight / 2 + 300))

            self.screen.blit(game_win_surf, game_win_rect)
            self.screen.blit(game_win_surf_1, game_win_rect_1)
            self.screen.blit(game_caption_surf, game_caption_rect)
            self.screen.blit(game_caption_surf_1, game_caption_rect_1)

            # pygame.time.wait(500)

    # Обновления экрана
    def _update_sreen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        # при каждом проходе цикла перерисовываеn цвет экрана
        # используется обращение к имопртир. модулю
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.draw(self.screen)
        self.ship.sprite.bullets.draw(self.screen)
        self.aliens.draw(self.screen)  # Отображение пришельца на экране
        self.alien_lasers.draw(self.screen)
        if self.settings.score >= 112000 and not self.aliens:
            self.boss.draw(self.screen)
        self.arc.draw(self.screen)
        self.display_score()
        self.display_lives()
        self.game_over_message()
        self.win_game_message()

        # отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == "__main__":
    # создание экземпляра и запуск игры.
    pygame.init()
    clock = pygame.time.Clock()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 500)

    BOSSLASER = pygame.USEREVENT + 2
    pygame.time.set_timer(BOSSLASER, 900)

    BOSSARC = pygame.USEREVENT + 3
    pygame.time.set_timer(BOSSARC, 3050)

    ai = AlienInvasion()
    ai.run_game()
