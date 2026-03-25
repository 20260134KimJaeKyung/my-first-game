import pygame
import os

def load_sprite(name, size=None):
    base_path = os.path.dirname(__file__)  # 현재 파일 위치 기준
    path = os.path.join(base_path, "assets", f"{name}.png")

    print("👉 절대경로:", path)

    if not os.path.exists(path):
        print("❌ 파일 없음:", path)
        return pygame.Surface((50, 50))

    image = pygame.image.load(path).convert_alpha()

    if size:
        image = pygame.transform.scale(image, size)

    return image