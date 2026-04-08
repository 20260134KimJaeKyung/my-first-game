import base64, io
import pygame

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  스프라이트 시트 Base64 데이터
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHEET_B64 = "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"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  설정
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCREEN_W, SCREEN_H = 480, 320
FRAME_W, FRAME_H   = 16, 16
COLS               = 4
FRAME_DELAY        = 150   # ms
DISPLAY_SCALE      = 4     # 화면 확대 배율

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Sprite Animation Demo")
clock = pygame.time.Clock()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  시트 로드 → 프레임 리스트
#  인덱스 0 ~ 27 (총 28개)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sheet_bytes = base64.b64decode(SHEET_B64)
player_sheet = pygame.image.load(io.BytesIO(sheet_bytes)).convert_alpha()

player_frames = []
for i in range(28):
    row, col = divmod(i, COLS)
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    player_frames.append(player_sheet.subsurface(rect))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  walk_frames: 선택한 프레임 순서
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
walk_frames = [player_frames[i] for i in [0, 4, 8, 12, 16, 20, 24]]

frame_index = 0
frame_timer = 0
x = SCREEN_W // 2 - (FRAME_W * DISPLAY_SCALE) // 2
y = SCREEN_H // 2 - (FRAME_H * DISPLAY_SCALE) // 2

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  게임 루프
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    frame_timer += dt
    if frame_timer >= FRAME_DELAY:
        frame_index = (frame_index + 1) % len(walk_frames)
        frame_timer = 0

    screen.fill((30, 30, 40))
    frame_img = pygame.transform.scale(
        walk_frames[frame_index],
        (FRAME_W * DISPLAY_SCALE, FRAME_H * DISPLAY_SCALE)
    )
    screen.blit(frame_img, (x, y))
    pygame.display.flip()

pygame.quit()
