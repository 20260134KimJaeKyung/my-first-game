import pygame
import math


class XPOrb:

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            12,
            12
        )

        self.value = 1

    def update(self, player):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = math.hypot(dx, dy)

        if distance < 120 and distance > 0:

            dx /= distance
            dy /= distance

            self.rect.x += dx * 4
            self.rect.y += dy * 4

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            (0, 255, 120),
            self.rect.center,
            6
        )