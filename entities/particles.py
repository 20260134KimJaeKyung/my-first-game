import pygame
import math
import random


class Particle:
    __slots__ = ("x", "y", "color", "vx", "vy", "size", "lifetime", "max_lifetime")

    def __init__(self, x, y, color, vx, vy, size, lifetime):
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.vx = vx
        self.vy = vy
        self.size = float(size)
        self.lifetime = lifetime
        self.max_lifetime = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.18
        self.vx *= 0.93
        self.size *= 0.96
        self.lifetime -= 1

    def draw(self, surface):
        s = max(1, int(self.size))
        alpha = int(220 * self.lifetime / self.max_lifetime)
        buf = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        pygame.draw.circle(buf, (*self.color, alpha), (s, s), s)
        surface.blit(buf, (int(self.x) - s, int(self.y) - s))

    @property
    def alive(self):
        return self.lifetime > 0 and self.size >= 0.8


class DamageNumber:
    _font = None

    def __init__(self, x, y, value, color=(255, 230, 60)):
        if DamageNumber._font is None:
            DamageNumber._font = pygame.font.SysFont(None, 24)
        self.x = float(x) + random.uniform(-8, 8)
        self.y = float(y) - 10
        self.value = value
        self.color = color
        self.vy = -1.8
        self.lifetime = 50
        self.max_lifetime = 50

    def update(self):
        self.y += self.vy
        self.vy = min(self.vy + 0.07, 0)
        self.lifetime -= 1

    def draw(self, surface):
        alpha = min(255, int(280 * self.lifetime / self.max_lifetime))
        text = self._font.render(f"-{self.value}", True, self.color)
        text.set_alpha(alpha)
        surface.blit(text, (int(self.x) - text.get_width() // 2, int(self.y)))

    @property
    def alive(self):
        return self.lifetime > 0


def spawn_death(cx, cy, count=14, color=(100, 220, 80)):
    particles = []
    for _ in range(count):
        a = random.uniform(0, math.tau)
        speed = random.uniform(1.5, 5.5)
        particles.append(Particle(
            cx, cy, color,
            math.cos(a) * speed,
            math.sin(a) * speed,
            random.uniform(3, 8),
            random.randint(20, 38),
        ))
    return particles


def spawn_hit(cx, cy, count=4):
    particles = []
    for _ in range(count):
        a = random.uniform(0, math.tau)
        speed = random.uniform(1, 3)
        particles.append(Particle(
            cx, cy, (255, 240, 150),
            math.cos(a) * speed,
            math.sin(a) * speed,
            random.uniform(2, 4),
            random.randint(8, 18),
        ))
    return particles
