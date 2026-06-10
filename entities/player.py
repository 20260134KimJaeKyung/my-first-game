import pygame


class Player:

    def __init__(self):

        self.size = 40

        self.rect = pygame.Rect(
            640 - self.size // 2,
            360 - self.size // 2,
            self.size,
            self.size
        )

        self.speed = 5

    def update(self):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.rect.y -= self.speed

        if keys[pygame.K_s]:
            self.rect.y += self.speed

        if keys[pygame.K_a]:
            self.rect.x -= self.speed

        if keys[pygame.K_d]:
            self.rect.x += self.speed

        self.rect.x = max(0, min(self.rect.x, 1280 - self.size))
        self.rect.y = max(0, min(self.rect.y, 720 - self.size))

    def draw(self, screen):

        pygame.draw.rect(
            screen,
            (50, 200, 255),
            self.rect,
            border_radius=8
        )