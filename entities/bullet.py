
import pygame
import math


class Bullet:
    """플레이어가 발사하는 파이어볼."""

    # 10장의 파이어볼 프레임을 한 번만 로드해서 공유한다.
    _raw_frames = None

    def __init__(self, x, y, dx, dy, size=24, damage=1, speed=10):

        self.size = size
        self.damage = damage
        self.speed = speed

        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (x, y)

        length = math.hypot(dx, dy)

        if length == 0:
            length = 1

        self.dx = dx / length
        self.dy = dy / length

        self.angle = math.degrees(math.atan2(-self.dy, self.dx))

        self.frames = [
            pygame.transform.scale(frame, (size, size))
            for frame in self._load_raw_frames()
        ]

        self.frame_index = 0
        self.animation_timer = 0

    @classmethod
    def _load_raw_frames(cls):

        if cls._raw_frames is None:

            cls._raw_frames = [
                pygame.image.load(
                    f"assets/images/bullets/fireball_{i}.png"
                ).convert_alpha()
                for i in range(10)
            ]

        return cls._raw_frames

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

        image = self.frames[self.frame_index]

        image = pygame.transform.rotate(image, self.angle)

        screen.blit(
            image,
            (
                self.rect.centerx - image.get_width() // 2,
                self.rect.centery - image.get_height() // 2,
            ),
        )
