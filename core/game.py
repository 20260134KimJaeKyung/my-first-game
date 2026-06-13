import pygame
import math
import random

from entities.player import Player
from entities.enemy import Enemy
from entities.tank_enemy import TankEnemy
from entities.bullet import Bullet
from entities.xp_orb import XPOrb


WIDTH = 1280
HEIGHT = 720


# (라벨, 설명) 형태의 업그레이드 풀
UPGRADE_POOL = [
    ("Attack Speed", "Fire faster"),
    ("Bullet Size", "Bigger fireballs"),
    ("Damage Up", "+1 damage per hit"),
    ("Multishot", "+1 extra fireball"),
    ("Move Speed", "Move faster"),
    ("Max HP +20", "Raise & heal HP"),
    ("Heal 40 HP", "Restore health"),
]


class Game:

    def __init__(self):

        self.player = Player()

        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 80)

        self.max_hp = 100
        self.hp = 100

        self.level = 1
        self.xp = 0
        self.xp_needed = 5

        self.wave = 1
        self.survival_time = 0
        self.kills = 0

        # 공격 스탯
        self.attack_cooldown = 12
        self.bullet_size = 24
        self.bullet_damage = 1
        self.shots = 1

        self.enemies = []
        self.bullets = []
        self.xp_orbs = []

        self.spawn_timer = 0
        self.attack_timer = 0

        self.level_up_active = False
        self.upgrade_choices = []

        self.game_over = False

        # 타일 로드 (tile0 ~ tile6)
        self.tiles = []

        for i in range(7):

            tile = pygame.image.load(
                f"assets/images/tiles/tile{i}.png"
            ).convert_alpha()

            tile = pygame.transform.scale(tile, (64, 64))

            self.tiles.append(tile)

        # 맵 생성 (12행 x 20열, 64px = 1280 x 768)
        self.map_data = [
            [random.randint(0, len(self.tiles) - 1) for _ in range(20)]
            for _ in range(12)
        ]

    # ------------------------------------------------------------------ #
    # 업그레이드
    # ------------------------------------------------------------------ #

    def generate_upgrades(self):

        self.upgrade_choices = random.sample(UPGRADE_POOL, 3)

    def apply_upgrade(self, choice):

        label = choice[0] if isinstance(choice, tuple) else choice

        if label == "Attack Speed":
            self.attack_cooldown = max(3, self.attack_cooldown - 2)

        elif label == "Bullet Size":
            self.bullet_size += 8

        elif label == "Damage Up":
            self.bullet_damage += 1

        elif label == "Multishot":
            self.shots += 1

        elif label == "Move Speed":
            self.player.speed += 1

        elif label == "Max HP +20":
            self.max_hp += 20
            self.hp += 20

        elif label == "Heal 40 HP":
            self.hp = min(self.max_hp, self.hp + 40)

        self.level_up_active = False

    # ------------------------------------------------------------------ #
    # 스폰 / 발사
    # ------------------------------------------------------------------ #

    def spawn_enemy(self):

        side = random.randint(0, 3)

        if side == 0:
            x, y = random.randint(0, WIDTH), -50
        elif side == 1:
            x, y = random.randint(0, WIDTH), HEIGHT + 50
        elif side == 2:
            x, y = -50, random.randint(0, HEIGHT)
        else:
            x, y = WIDTH + 50, random.randint(0, HEIGHT)

        # Wave 3부터 탱크 적이 섞여 나온다.
        if self.wave >= 3 and random.random() < 0.18 + self.wave * 0.01:
            self.enemies.append(TankEnemy(x, y))
        else:
            enemy = Enemy(x, y)
            # 웨이브가 오를수록 일반 적도 조금씩 단단해진다.
            bonus = (self.wave - 1) // 2
            enemy.max_hp += bonus
            enemy.hp += bonus
            self.enemies.append(enemy)

    def fire(self):

        cx = self.player.rect.centerx
        cy = self.player.rect.centery

        base_x = self.player.direction_x
        base_y = self.player.direction_y

        # 멀티샷이면 부채꼴로 퍼뜨린다.
        spread = 12
        start = -spread * (self.shots - 1) / 2

        for i in range(self.shots):

            angle = math.radians(start + spread * i)

            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            dx = base_x * cos_a - base_y * sin_a
            dy = base_x * sin_a + base_y * cos_a

            self.bullets.append(
                Bullet(
                    cx,
                    cy,
                    dx,
                    dy,
                    size=self.bullet_size,
                    damage=self.bullet_damage,
                )
            )

    # ------------------------------------------------------------------ #
    # 업데이트
    # ------------------------------------------------------------------ #

    def update(self):

        if self.level_up_active or self.game_over:
            return

        self.survival_time += 1 / 60
        self.wave = int(self.survival_time // 30) + 1

        self.player.update()

        self.spawn_timer += 1
        self.attack_timer += 1

        spawn_rate = max(15, 60 - self.wave * 3)

        if self.spawn_timer >= spawn_rate:
            self.spawn_enemy()
            self.spawn_timer = 0

        if self.attack_timer >= self.attack_cooldown:
            self.fire()
            self.attack_timer = 0

        # 경험치 구슬
        for orb in self.xp_orbs[:]:

            orb.update(self.player)

            if orb.rect.colliderect(self.player.rect):
                self.xp += orb.value
                self.xp_orbs.remove(orb)

        # 레벨업 체크
        if self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.level += 1
            self.xp_needed += 3
            self.level_up_active = True
            self.generate_upgrades()

        # 총알 이동 / 화면 밖 제거
        for bullet in self.bullets[:]:

            bullet.update()

            if (
                bullet.rect.right < -100
                or bullet.rect.left > WIDTH + 100
                or bullet.rect.bottom < -100
                or bullet.rect.top > HEIGHT + 100
            ):
                self.bullets.remove(bullet)

        # 적 이동 / 충돌
        for enemy in self.enemies[:]:

            enemy.update(self.player)

            if enemy.rect.colliderect(self.player.rect):
                self.hp -= enemy.touch_damage
                self.player.hit()

            for bullet in self.bullets[:]:

                if bullet.rect.colliderect(enemy.rect):

                    enemy.take_damage(bullet.damage)

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    if enemy.hp <= 0:

                        self.xp_orbs.append(
                            XPOrb(
                                enemy.rect.centerx,
                                enemy.rect.centery,
                                value=enemy.xp_value,
                            )
                        )

                        self.enemies.remove(enemy)
                        self.kills += 1

                    break

        if self.hp <= 0:
            self.hp = 0
            self.game_over = True

    # ------------------------------------------------------------------ #
    # 그리기
    # ------------------------------------------------------------------ #

    def draw(self, screen):

        self.draw_world(screen)
        self.draw_hud(screen)

        if self.level_up_active:
            self.draw_level_up(screen)

        if self.game_over:
            self.draw_game_over(screen)

    def draw_world(self, screen):

        for row in range(len(self.map_data)):
            for col in range(len(self.map_data[row])):
                tile_index = self.map_data[row][col]
                screen.blit(self.tiles[tile_index], (col * 64, row * 64))

        for orb in self.xp_orbs:
            orb.draw(screen)

        self.player.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen)

        # 체력이 낮으면 화면 가장자리를 붉게.
        if self.hp / self.max_hp < 0.3:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(
                overlay,
                (180, 0, 0, 70),
                (0, 0, WIDTH, HEIGHT),
                width=40,
            )
            screen.blit(overlay, (0, 0))

    def draw_hud(self, screen):

        screen.blit(
            self.font.render(f"LV {self.level}", True, (255, 255, 0)),
            (20, 18),
        )
        screen.blit(
            self.small_font.render(f"Wave {self.wave}", True, (255, 255, 255)),
            (20, 58),
        )
        screen.blit(
            self.small_font.render(
                f"Time {int(self.survival_time)}s", True, (200, 200, 200)
            ),
            (20, 84),
        )
        screen.blit(
            self.small_font.render(f"Kills {self.kills}", True, (200, 200, 200)),
            (20, 110),
        )

        # HP 바
        bar_x, bar_y, bar_w = 20, 142, 320

        pygame.draw.rect(screen, (70, 70, 70), (bar_x, bar_y, bar_w, 22))
        pygame.draw.rect(
            screen,
            (50, 220, 80),
            (bar_x, bar_y, bar_w * max(0, self.hp) / self.max_hp, 22),
        )
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_w, 22), 2)
        screen.blit(
            self.small_font.render(
                f"{int(self.hp)}/{self.max_hp}", True, (255, 255, 255)
            ),
            (bar_x + 8, bar_y - 1),
        )

        # XP 바
        xp_y = bar_y + 28
        pygame.draw.rect(screen, (40, 40, 60), (bar_x, xp_y, bar_w, 12))
        pygame.draw.rect(
            screen,
            (90, 160, 255),
            (bar_x, xp_y, bar_w * min(1, self.xp / self.xp_needed), 12),
        )

    def draw_level_up(self, screen):

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 280, 150, 560, 420)
        pygame.draw.rect(screen, (25, 25, 35), panel, border_radius=16)
        pygame.draw.rect(screen, (255, 255, 0), panel, 3, border_radius=16)

        title = self.big_font.render("LEVEL UP!", True, (255, 255, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 175))

        hint = self.small_font.render(
            "Press 1 / 2 / 3 to choose", True, (180, 180, 180)
        )
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 250))

        for i, (label, desc) in enumerate(self.upgrade_choices):

            box = pygame.Rect(WIDTH // 2 - 240, 290 + i * 90, 480, 76)
            pygame.draw.rect(screen, (45, 45, 60), box, border_radius=10)
            pygame.draw.rect(screen, (120, 120, 140), box, 2, border_radius=10)

            line = self.font.render(f"{i + 1}.  {label}", True, (255, 255, 255))
            screen.blit(line, (box.x + 20, box.y + 12))

            sub = self.small_font.render(desc, True, (170, 200, 255))
            screen.blit(sub, (box.x + 24, box.y + 44))

    def draw_game_over(self, screen):

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        title = self.big_font.render("GAME OVER", True, (255, 70, 70))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))

        stats = [
            f"Reached Level {self.level}",
            f"Survived {int(self.survival_time)} seconds  -  Wave {self.wave}",
            f"Kills: {self.kills}",
        ]

        for i, line in enumerate(stats):
            text = self.font.render(line, True, (230, 230, 230))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 320 + i * 44))

        prompt = self.font.render(
            "Press R to Restart    -    ESC for Menu", True, (255, 255, 0)
        )
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 480))
