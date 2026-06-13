
import pygame
import math


class XPOrb:
    """적이 죽으면 떨어지는 경험치 구슬. 플레이어가 가까우면 끌려온다."""

    def __init__(self, x, y, value=1):

        self.rect = pygame.Rect(0, 0, 12, 12)
        self.rect.center = (x, y)

        self.value = value
        self.pulse = 0

    def update(self, player):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = math.hypot(dx, dy)

        if 0 < distance < 140:

            dx /= distance
            dy /= distance

            # 가까울수록 빨리 끌려온다.
            pull = 4 + (140 - distance) / 20

            self.rect.x += dx * pull
            self.rect.y += dy * pull

        self.pulse += 0.2

    def draw(self, screen):

        radius = 6 + int(math.sin(self.pulse) * 1.5)

        # 바깥 글로우
        pygame.draw.circle(
            screen,
            (0, 120, 60),
            self.rect.center,
            radius + 3,
        )

        pygame.draw.circle(
            screen,
            (0, 255, 120),
            self.rect.center,
            radius,
        )
