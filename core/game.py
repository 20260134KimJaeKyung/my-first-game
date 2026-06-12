import pygame
import random

from entities.player import Player
from entities.enemy  import Enemy
from entities.bullet import Bullet
from entities.xp_orb import XPOrb


class Game:

    def __init__(self):

        self.player = Player()

        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 60)

        self.max_hp = 100
        self.hp = 100

        self.level = 1
        self.xp = 0
        self.xp_needed = 5

        self.wave = 1
        self.survival_time = 0

        self.attack_cooldown = 10
        self.bullet_size_bonus = 0

        self.enemies = []
        self.bullets = []
        self.xp_orbs = []

        self.spawn_timer = 0
        self.attack_timer = 0

        self.level_up_active = False
        self.upgrade_choices = []

        self.game_over = False

        # 타일 로드
        self.tiles = []

        for i in range(1, 7):

            tile = pygame.image.load(
                f"assets/images/tiles/tile{i}.png"
            ).convert_alpha()

            tile = pygame.transform.scale(
                tile,
                (64, 64)
            )

            self.tiles.append(tile)

        # 맵 생성
        self.map_data = []

        for row in range(12):

            row_data = []

            for col in range(20):

                row_data.append(
                    random.randint(0, 5)
                )

            self.map_data.append(row_data)

    def generate_upgrades(self):

        pool = [
            "Attack Speed Up",
            "Bullet Size Up",
            "Heal 30 HP"
        ]

        self.upgrade_choices = random.sample(
            pool,
            3
        )

    def apply_upgrade(self, choice):

        if choice == "Attack Speed Up":

            self.attack_cooldown = max(
                3,
                self.attack_cooldown - 2
            )

        elif choice == "Bullet Size Up":

            self.bullet_size_bonus += 2

        elif choice == "Heal 30 HP":

            self.hp = min(
                self.max_hp,
                self.hp + 30
            )

        self.level_up_active = False

    def spawn_enemy(self):

        side = random.randint(0, 3)

        if side == 0:
            x = random.randint(0, 1280)
            y = -50

        elif side == 1:
            x = random.randint(0, 1280)
            y = 770

        elif side == 2:
            x = -50
            y = random.randint(0, 720)

        else:
            x = 1330
            y = random.randint(0, 720)

        self.enemies.append(
            Enemy(x, y)
        )

    def update(self):

        if self.level_up_active:
            return

        if self.game_over:
            return

        self.survival_time += 1 / 60

        self.wave = int(
            self.survival_time // 30
        ) + 1

        self.player.update()

        self.spawn_timer += 1
        self.attack_timer += 1

        spawn_rate = max(
            20,
            60 - self.wave * 3
        )

        if self.spawn_timer >= spawn_rate:

            self.spawn_enemy()
            self.spawn_timer = 0

        if self.attack_timer >= self.attack_cooldown:

            bullet = Bullet(
                self.player.rect.centerx,
                self.player.rect.centery,
                self.player.direction_x,
                self.player.direction_y
            )

            self.bullets.append(
                bullet
            )

            self.attack_timer = 0

        for orb in self.xp_orbs[:]:

            orb.update(self.player)

            if orb.rect.colliderect(
                self.player.rect
            ):

                self.xp += orb.value

                self.xp_orbs.remove(orb)

        if self.xp >= self.xp_needed:

            self.xp -= self.xp_needed

            self.level += 1

            self.xp_needed += 3

            self.level_up_active = True

            self.generate_upgrades()

        for bullet in self.bullets[:]:

            bullet.update()

            if (
                bullet.rect.x < -100
                or bullet.rect.x > 1400
                or bullet.rect.y < -100
                or bullet.rect.y > 900
            ):

                self.bullets.remove(bullet)

        for enemy in self.enemies[:]:

            enemy.update(self.player)

            if enemy.rect.colliderect(
                self.player.rect
            ):

                self.hp -= 0.2

            for bullet in self.bullets[:]:

                if bullet.rect.colliderect(
                    enemy.rect
                ):

                    enemy.hp -= 1

                    if bullet in self.bullets:
                        self.bullets.remove(
                            bullet
                        )

                    if enemy.hp <= 0:

                        self.xp_orbs.append(
                            XPOrb(
                                enemy.rect.centerx,
                                enemy.rect.centery
                            )
                        )

                        self.enemies.remove(
                            enemy
                        )

                    break

        if self.hp <= 0:

            self.hp = 0
            self.game_over = True

    def draw(self, screen):

        # 타일맵
        for row in range(
            len(self.map_data)
        ):

            for col in range(
                len(self.map_data[row])
            ):

                tile_index = self.map_data[row][col]

                screen.blit(
                    self.tiles[tile_index],
                    (
                        col * 64,
                        row * 64
                    )
                )

        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        for orb in self.xp_orbs:
            orb.draw(screen)

        screen.blit(
            self.font.render(
                f"LV {self.level}",
                True,
                (255, 255, 0)
            ),
            (20, 20)
        )

        screen.blit(
            self.font.render(
                f"Wave {self.wave}",
                True,
                (255, 255, 255)
            ),
            (20, 60)
        )

        pygame.draw.rect(
            screen,
            (70, 70, 70),
            (20, 100, 300, 24)
        )

        pygame.draw.rect(
            screen,
            (50, 220, 80),
            (
                20,
                100,
                300 * (
                    self.hp / self.max_hp
                ),
                24
            )
        )