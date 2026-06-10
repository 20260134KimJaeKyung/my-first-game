
import pygame
import random

from entities.player import Player
from entities.enemy import Enemy
from entities.tank_enemy import TankEnemy
from entities.bullet import Bullet
from entities.xp_orb import XPOrb


class Game:

    def __init__(self):

        self.background_color = (25, 25, 35)

        self.player = Player()

        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 60)

        self.max_hp = 100
        self.hp = 100

        self.level = 1
        self.xp = 0
        self.xp_needed = 5

        self.attack_cooldown = 10
        self.bullet_size_bonus = 0

        self.enemies = []
        self.bullets = []
        self.xp_orbs = []

        self.spawn_timer = 0
        self.attack_timer = 0

        self.level_up_active = False
        self.upgrade_choices = []

        self.survival_time = 0
        self.wave = 1

    def generate_upgrades(self):

        pool = [
            "Attack Speed Up",
            "Bullet Size Up",
            "Heal 30 HP"
        ]

        self.upgrade_choices = random.sample(pool, 3)

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

        # Wave 3부터 탱크 적 등장

        if self.wave >= 3 and random.random() < 0.2:

            self.enemies.append(
                TankEnemy(x, y)
            )

        else:

            self.enemies.append(
                Enemy(x, y)
            )

    def update(self):

        if self.level_up_active:
            return

        self.survival_time += 1 / 60

        self.wave = int(
            self.survival_time // 30
        ) + 1

        self.player.update()

        self.spawn_timer += 1
        self.attack_timer += 1

        spawn_rate = max(
            15,
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

            bullet.size += self.bullet_size_bonus

            self.bullets.append(
                bullet
            )

            self.attack_timer = 0

        for orb in self.xp_orbs[:]:

            orb.update(self.player)

            if orb.rect.colliderect(
                    self.player.rect):

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
                    self.player.rect):

                self.hp -= 0.2

            for bullet in self.bullets[:]:

                if bullet.rect.colliderect(
                        enemy.rect):

                    enemy.hp -= 1

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    if enemy.hp <= 0:

                        self.xp_orbs.append(
                            XPOrb(
                                enemy.rect.centerx,
                                enemy.rect.centery
                            )
                        )

                        self.enemies.remove(enemy)

                    break

        if self.hp < 0:
            self.hp = 0

    def draw(self, screen):

        screen.fill(self.background_color)

        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        for orb in self.xp_orbs:
            orb.draw(screen)

        level_text = self.font.render(
            f"LV {self.level}",
            True,
            (255, 255, 0)
        )

        wave_text = self.font.render(
            f"Wave {self.wave}",
            True,
            (255, 255, 255)
        )

        time_text = self.font.render(
            f"Time {int(self.survival_time)}",
            True,
            (255, 255, 255)
        )

        screen.blit(level_text, (20, 20))
        screen.blit(wave_text, (20, 60))
        screen.blit(time_text, (20, 100))

        if self.level_up_active:

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                (250, 150, 780, 400)
            )

            title = self.big_font.render(
                "LEVEL UP",
                True,
                (255, 255, 0)
            )

            screen.blit(
                title,
                (
                    640 - title.get_width() // 2,
                    180
                )
            )

            for i, choice in enumerate(
                    self.upgrade_choices):

                text = self.font.render(
                    f"{i+1}. {choice}",
                    True,
                    (255, 255, 255)
                )

                screen.blit(
                    text,
                    (
                        320,
                        280 + i * 80
                    )
                )
```
