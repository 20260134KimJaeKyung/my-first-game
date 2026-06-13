
import pygame
import math


class Enemy:
    """plant1 스프라이트를 사용하는 기본 추적형 적."""

    # 스프라이트 시트(Run.png)를 클래스 단위로 캐싱해서
    # 적이 생성될 때마다 디스크에서 다시 읽지 않도록 한다.
    _sheet_cache = {}

    def __init__(
        self,
        x,
        y,
        size=40,
        speed=2,
        hp=3,
        xp_value=1,
        touch_damage=0.2,
        tint=None,
        sprite="assets/images/enemies/plant1/Run.png",
    ):

        self.size = size

        self.rect = pygame.Rect(x, y, size, size)

        self.speed = speed

        self.max_hp = hp
        self.hp = hp

        self.xp_value = xp_value
        self.touch_damage = touch_damage

        self.facing_left = False
        self.hurt_timer = 0

        self.run_frames = self.load_sheet(sprite, size, tint)
        self.current_frames = self.run_frames

        self.frame_index = 0
        self.animation_timer = 0

    def load_sheet(self, path, size, tint):

        cache_key = (path, size, tint)

        if cache_key in Enemy._sheet_cache:
            return Enemy._sheet_cache[cache_key]

        sheet = pygame.image.load(path).convert_alpha()

        cols = 8
        rows = 4

        frame_width = sheet.get_width() // cols
        frame_height = sheet.get_height() // rows

        frames = []

        # 첫 번째 줄만 걷기 애니메이션으로 사용한다.
        row = 0

        for col in range(cols):

            frame = sheet.subsurface(
                (
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height,
                )
            )

            frame = pygame.transform.scale(frame, (size, size))

            if tint is not None:
                frame = frame.copy()
                frame.fill(tint, special_flags=pygame.BLEND_RGB_MULT)

            frames.append(frame)

        Enemy._sheet_cache[cache_key] = frames
        return frames

    def take_damage(self, amount):

        self.hp -= amount
        self.hurt_timer = 6

    def update(self, player):

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = math.hypot(dx, dy)

        if distance > 0:

            dx /= distance
            dy /= distance

            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            self.facing_left = dx < 0

        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        self.animation_timer += 1

        if self.animation_timer >= 8:

            self.frame_index += 1

            if self.frame_index >= len(self.current_frames):
                self.frame_index = 0

            self.animation_timer = 0

    def draw(self, screen):

        image = self.current_frames[self.frame_index]

        if self.facing_left:
            image = pygame.transform.flip(image, True, False)

        # 피격 시 흰색으로 번쩍이게 한다.
        if self.hurt_timer > 0:
            image = image.copy()
            image.fill(
                (255, 255, 255, 0),
                special_flags=pygame.BLEND_RGB_ADD,
            )

        screen.blit(image, (self.rect.x, self.rect.y))

        # 체력바 (가득 찬 경우엔 생략)
        if self.hp < self.max_hp:

            bar_w = self.size

            pygame.draw.rect(
                screen,
                (60, 60, 60),
                (self.rect.x, self.rect.y - 6, bar_w, 4),
            )

            pygame.draw.rect(
                screen,
                (255, 60, 60),
                (
                    self.rect.x,
                    self.rect.y - 6,
                    bar_w * max(0, self.hp) / self.max_hp,
                    4,
                ),
            )
