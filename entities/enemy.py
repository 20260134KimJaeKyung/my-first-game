
import pygame
import math


class Enemy:

    def __init__(self, x, y):

        self.size = 40

        self.rect = pygame.Rect(
            x,
            y,
            self.size,
            self.size
        )

        self.speed = 2
        self.hp = 3

        self.run_frames = self.load_sheet(
            "assets/images/enemies/plant1/Run.png"
        )

        self.current_frames = self.run_frames

        self.frame_index = 0
        self.animation_timer = 0

    def load_sheet(self, path):

        sheet = pygame.image.load(
            path
        ).convert_alpha()

        frames = []

        cols = 8
        rows = 4

        frame_width = sheet.get_width() // cols
        frame_height = sheet.get_height() // rows

        # 첫 번째 줄만 사용
        row = 0

        for col in range(cols):

            frame = sheet.subsurface(
                (
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height
                )
            )

            frame = pygame.transform.scale(
                frame,
                (40, 40)
            )

            frames.append(frame)

        return frames

    def update(self, player):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = math.hypot(dx, dy)

        if distance > 0:

            dx /= distance
            dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        self.animation_timer += 1

        if self.animation_timer >= 8:

            self.frame_index += 1

            if self.frame_index >= len(self.current_frames):
                self.frame_index = 0

            self.animation_timer = 0

    def draw(self, screen):

        image = self.current_frames[
            self.frame_index
        ]

        screen.blit(
            image,
            (
                self.rect.x,
                self.rect.y
            )
        )

        pygame.draw.rect(
            screen,
            (60, 60, 60),
            (
                self.rect.x,
                self.rect.y - 6,
                30,
                4
            )
        )

        pygame.draw.rect(
            screen,
            (255, 60, 60),
            (
                self.rect.x,
                self.rect.y - 6,
                30 * (self.hp / 3),
                4
            )
        )

