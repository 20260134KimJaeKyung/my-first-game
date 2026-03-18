import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")

WHITE = (0, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE_CIRCLE = (255, 255, 255)

clock = pygame.time.Clock()
running = True

# 폰트 설정
font = pygame.font.SysFont(None, 30)

# 원 위치
x = 400
y = 300

# 기본 속도
speed = 5

# 원 반지름
radius = 50

# 🎨 색깔 리스트
colors = [BLUE, YELLOW, WHITE_CIRCLE]
color_index = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 🔥 F 키 누르면 색 변경
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                color_index += 1
                if color_index >= len(colors):
                    color_index = 0

    # 키 입력 상태 가져오기
    keys = pygame.key.get_pressed()

    # Shift 누르면 속도 2배
    current_speed = speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        current_speed = speed * 2

    # WASD 이동
    if keys[pygame.K_w]:
        y -= current_speed
    if keys[pygame.K_s]:
        y += current_speed
    if keys[pygame.K_a]:
        x -= current_speed
    if keys[pygame.K_d]:
        x += current_speed

    # 화면 제한
    if x < radius:
        x = radius
    if x > 800 - radius:
        x = 800 - radius
    if y < radius:
        y = radius
    if y > 600 - radius:
        y = 600 - radius

    screen.fill(WHITE)

    # 🎨 현재 색으로 원 그리기
    pygame.draw.circle(screen, colors[color_index], (x, y), radius)

    # FPS 표시
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, BLACK)
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()