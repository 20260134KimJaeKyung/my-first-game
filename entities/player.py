import pygame
import math


class Player:

    def __init__(self):

        self.size = 64

        self.rect = pygame.Rect(
            640,
            360,
            self.size,
            self.size
        )

        self.speed = 5

        self.dash_speed = 15
        self.dash_cooldown = 0

        self.direction_x = 1
        self.direction_y = 0

        # 애니메이션

        self.frame_width = 120
        self.frame_height = 80

        self.idle_frames = self.load_sheet(
            "assets/images/player/_Idle.png"
        )

        self.run_frames = self.load_sheet(
            "assets/images/player/_Run.png"
        )

        self.current_frames = self.idle_frames

        self.frame_index = 0
        self.animation_timer = 0

        self.is_moving = False

    def load_sheet(self, path):

        sheet = pygame.image.load(
            path
        ).convert_alpha()

        frames = []

        frame_count = sheet.get_width() // self.frame_width

        for i in range(frame_count):

            frame = sheet.subsurface(
                (
                    i * self.frame_width,
                    0,
                    self.frame_width,
                    self.frame_height
                )
            )

            frame = pygame.transform.scale(
                frame,
                (64, 64)
            )

            frames.append(frame)

        return frames

    def update(self):

        current_speed = self.speed

        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1

        keys = pygame.key.get_pressed()

        move_x = 0
        move_y = 0

        if keys[pygame.K_w]:
            move_y -= 1

        if keys[pygame.K_s]:
            move_y += 1

        if keys[pygame.K_a]:
            move_x -= 1

        if keys[pygame.K_d]:
            move_x += 1

        self.is_moving = (
            move_x != 0 or move_y != 0
        )

        if keys[pygame.K_LSHIFT]:

            if self.dash_cooldown <= 0:

                current_speed = self.dash_speed
                self.dash_cooldown = 30

        self.rect.x += move_x * current_speed
        self.rect.y += move_y * current_speed

        self.rect.x = max(
            0,
            min(self.rect.x, 1280 - self.size)
        )

        self.rect.y = max(
            0,
            min(self.rect.y, 720 - self.size)
        )

        mouse_x, mouse_y = pygame.mouse.get_pos()

        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery

        length = math.hypot(dx, dy)

        if length > 0:

            self.direction_x = dx / length
            self.direction_y = dy / length

        # 애니메이션 선택

        if self.is_moving:
            self.current_frames = self.run_frames
        else:
            self.current_frames = self.idle_frames

        self.animation_timer += 1

        if self.animation_timer >= 6:

            self.frame_index += 1

            if self.frame_index >= len(
                    self.current_frames):
                self.frame_index = 0

            self.animation_timer = 0

    def draw(self, screen):

        image = self.current_frames[
            self.frame_index
        ]

        # 좌우 반전

        if self.direction_x < 0:

            image = pygame.transform.flip(
                image,
                True,
                False
            )

        screen.blit(
            image,
            (
                self.rect.centerx - 32,
                self.rect.centery - 32
            )
        )