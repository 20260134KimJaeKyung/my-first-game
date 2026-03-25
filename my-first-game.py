import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Collision Comparison")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# 색상
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

rect_size = 80
speed = 5
radius = rect_size // 2

# 플레이어
player_rect = pygame.Rect(100, 100, rect_size, rect_size)

# 회전 오브젝트
center_surface = pygame.Surface((rect_size, rect_size), pygame.SRCALPHA)
center_surface.fill(GRAY)
center_pos = (400, 300)

angle = 0
rotation_speed = 1

# ---------- OBB 함수 ----------

def get_corners(pos, angle, size):
    cx, cy = pos
    w = size / 2
    h = size / 2

    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    corners = [(-w, -h), (w, -h), (w, h), (-w, h)]

    result = []
    for x, y in corners:
        rx = x * cos_a - y * sin_a + cx
        ry = x * sin_a + y * cos_a + cy
        result.append((rx, ry))

    return result

def get_axes(corners):
    axes = []
    for i in range(4):
        p1 = corners[i]
        p2 = corners[(i + 1) % 4]

        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])

        length = math.hypot(normal[0], normal[1])
        if length != 0:
            normal = (normal[0] / length, normal[1] / length)

        axes.append(normal)
    return axes

def project(corners, axis):
    dots = [corner[0]*axis[0] + corner[1]*axis[1] for corner in corners]
    return min(dots), max(dots)

def sat_collision(c1, c2):
    axes = get_axes(c1) + get_axes(c2)

    for axis in axes:
        min1, max1 = project(c1, axis)
        min2, max2 = project(c2, axis)

        if max1 < min2 or max2 < min1:
            return False
    return True

# -----------------------------

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 이동
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    # 회전 속도
    if keys[pygame.K_z]:
        rotation_speed = 3
    else:
        rotation_speed = 1

    player_rect.clamp_ip(screen.get_rect())

    angle += rotation_speed

    rotated_surface = pygame.transform.rotate(center_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=center_pos)

    # ---------- 충돌 계산 ----------

    # 1️⃣ AABB
    aabb_hit = player_rect.colliderect(rotated_rect)

    # 2️⃣ Circle
    dx = player_rect.centerx - rotated_rect.centerx
    dy = player_rect.centery - rotated_rect.centery
    circle_hit = (dx*dx + dy*dy) < (radius*2)**2

    # 3️⃣ OBB (SAT)
    player_corners = get_corners(player_rect.center, 0, rect_size)
    center_corners = get_corners(center_pos, angle, rect_size)
    obb_hit = sat_collision(player_corners, center_corners)

    # 배경
    screen.fill(WHITE)

    # ---------- 그리기 ----------

    # 사각형
    pygame.draw.rect(screen, GRAY, player_rect)
    screen.blit(rotated_surface, rotated_rect)

    # AABB (빨강)
    pygame.draw.rect(screen, RED, player_rect, 2)
    pygame.draw.rect(screen, RED, rotated_rect, 2)

    # Circle (파랑)
    pygame.draw.circle(screen, BLUE, player_rect.center, radius, 2)
    pygame.draw.circle(screen, BLUE, rotated_rect.center, radius, 2)

    # OBB (초록)
    pygame.draw.polygon(screen, GREEN, player_corners, 2)
    pygame.draw.polygon(screen, GREEN, center_corners, 2)

    # ---------- 텍스트 ----------

    screen.blit(font.render(f"Circle: {'HIT' if circle_hit else 'MISS'}", True, BLACK), (10, 10))
    screen.blit(font.render(f"AABB: {'HIT' if aabb_hit else 'MISS'}", True, BLACK), (10, 40))
    screen.blit(font.render(f"OBB: {'HIT' if obb_hit else 'MISS'}", True, BLACK), (10, 70))

    fps = int(clock.get_fps())
    screen.blit(font.render(f"FPS: {fps}", True, BLACK), (10, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()