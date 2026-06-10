
import pygame
import math


class Bullet:

    def __init__(self, x, y, dx, dy):

        self.size = 24

        self.rect = pygame.Rect(
            x,
            y,
            self.size,
            self.size
        )

        self.speed = 10

        length = math.hypot(dx, dy)

        if length == 0:
            length = 1

        self.dx = dx / length
        self.dy = dy / length

        self.frames = []

        for i in range(10):

            image = pygame.image.load(
                f"assets/images/bullets/fireball_{i}.png"
            ).convert_alpha()

            image = pygame.transform.scale(
                image,
                (24, 24)
            )

            self.frames.append(image)

        self.frame_index = 0
        self.animation_timer = 0

    def update(self):

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        self.animation_timer += 1

        if self.animation_timer >= 3:

            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.animation_timer = 0

    def draw(self, screen):

        image = self.frames[
            self.frame_index
        ]

        angle = math.degrees(
            math.atan2(
                -self.dy,
                self.dx
            )
        )

        image = pygame.transform.rotate(
            image,
            angle
        )

        screen.blit(
            image,
            (
                self.rect.centerx - image.get_width() // 2,
                self.rect.centery - image.get_height() // 2
            )
        )

