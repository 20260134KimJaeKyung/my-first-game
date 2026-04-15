import pygame
import sys
import random

pygame.init()


def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)


WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
BLUE = (50, 120, 220)
RED = (220, 50, 50)
YELLOW = (240, 200, 0)
ORANGE = (240, 140, 0)
GREEN = (50, 200, 50)
BLACK = (0, 0, 0)

BLOCK_TYPES = [
    {"color": RED, "score": 50, "image": "assets/images/brick_05.png", "broken_image": "assets/images/brick_broken05.png", "threshold": 30},
    {"color": ORANGE, "score": 40, "image": "assets/images/brick_04.png", "broken_image": "assets/images/brick_broken04.png", "threshold": 30},
    {"color": YELLOW, "score": 30, "image": "assets/images/brick_03.png", "broken_image": "assets/images/brick_broken03.png", "threshold": 20},
    {"color": GREEN, "score": 20, "image": "assets/images/brick_02.png", "broken_image": "assets/images/brick_broken02.png", "threshold": 10},
    {"color": BLUE, "score": 10, "image": "assets/images/brick_01.png", "broken_image": "assets/images/brick_broken01.png", "threshold": 5},
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

font = get_korean_font(36)
font_small = get_korean_font(18)
font_big = get_korean_font(100)

LEVELS = [
    {"rows": 3, "ball_speed": 5, "label": "Lv.1", "goal": 500},
    {"rows": 5, "ball_speed": 6, "label": "Lv.2", "goal": 900},
    {"rows": 7, "ball_speed": 8, "label": "Lv.3", "goal": 1400},
]

PAD_W, PAD_H = 100, 12
BALL_R = 8
BLOCK_W, BLOCK_H = 72, 22  # 블록의 크기
BLOCK_COLS = 10
BLOCK_MARGIN = 5
BLOCK_TOP = 140
BALL_DAMAGE = 10  # 공의 데미지


# 패들 이미지 추가
PADDLE_IMAGE = pygame.image.load("assets/images/paddle_image.png").convert_alpha()  # 패들 이미지 로드
PADDLE_IMAGE = pygame.transform.scale(PADDLE_IMAGE, (PAD_W, PAD_H))  # 패들 크기 맞추기

# 공 이미지 추가
BALL_IMAGE = pygame.image.load("assets/images/ball_image.png").convert_alpha()  # 공 이미지 로드
BALL_IMAGE = pygame.transform.scale(BALL_IMAGE, (BALL_R * 2, BALL_R * 2))  # 공 크기 맞추기

# 별 아이템 클래스 추가
class Star:
    def __init__(self, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.image = pygame.image.load("assets/images/star.png").convert_alpha()  # 별 이미지 로드
        self.image = pygame.transform.scale(self.image, (30, 30))  # 별 크기 조정
        self.rect = self.image.get_rect(center=(x, y))
    
    def draw(self):
        screen.blit(self.image, self.rect)  # 별 그리기


def make_blocks(rows):
    blocks = []
    positions = []

    for r in range(rows):
        for c in range(BLOCK_COLS):
            x = BLOCK_MARGIN + c * (BLOCK_W + BLOCK_MARGIN)
            y = BLOCK_TOP + r * (BLOCK_H + BLOCK_MARGIN)
            positions.append((x, y))

    random.shuffle(positions)

    for pos in positions:
        t = random.choice(BLOCK_TYPES)
        rect = pygame.Rect(pos[0], pos[1], BLOCK_W, BLOCK_H)

        # 블록의 색상과 이미지 설정
        block_image = pygame.image.load(t["image"]).convert()
        block_image = pygame.transform.scale(block_image, (BLOCK_W, BLOCK_H))  # 이미지 크기 맞추기

        blocks.append({
            "rect": rect,
            "image": block_image,  # 블록 이미지
            "score": t["score"],  # 블록의 점수
            "broken_image": t["broken_image"],  # 깨진 이미지
            "threshold": t["threshold"],  # 점수 감소 임계값
            "initial_score": t["score"],  # 초기 점수를 저장하여 깨지는지 확인
        })

    return blocks


def draw_hud(score, time_left, level_cfg):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Time: {int(time_left)}", True, RED), (WIDTH - 180, 10))

    level_text = font.render(level_cfg["label"], True, YELLOW)
    screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, 10))

    goal_text = font.render(f"GOAL {level_cfg['goal']}", True, GREEN)
    screen.blit(goal_text, (WIDTH // 2 - goal_text.get_width() // 2, 50))


def message_screen(title, color, score):
    screen.fill(GRAY)
    screen.blit(font_big.render(title, True, color), (WIDTH // 2 - 200, 220))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (350, 330))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (270, 380))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    level_idx = 0
    level_cfg = LEVELS[level_idx]

    pad = pygame.Rect(WIDTH // 2 - PAD_W // 2, HEIGHT - 40, PAD_W, PAD_H)

    ball = pygame.Rect(0, 0, BALL_R * 2, BALL_R * 2)
    ball.center = (pad.centerx, pad.top - BALL_R - 2)

    bx, by = level_cfg["ball_speed"], -level_cfg["ball_speed"]
    blocks = make_blocks(level_cfg["rows"])

    score = 0
    time_left = 60
    launched = False
    respawn_timer = 0

    stars = []  # 별 아이템 리스트 추가

    while True:
        dt = clock.tick(FPS) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if respawn_timer <= 0:
                    launched = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and pad.left > 0:
            pad.x -= 7
        if keys[pygame.K_RIGHT] and pad.right < WIDTH:
            pad.x += 7

        # 🎯 목표 달성 → 다음 레벨
        if score >= level_cfg["goal"]:
            level_idx += 1
            if level_idx >= len(LEVELS):
                if message_screen("CLEAR!", YELLOW, score):
                    main()
                return

            level_cfg = LEVELS[level_idx]
            blocks = make_blocks(level_cfg["rows"])
            score = 0
            time_left = 60
            launched = False
            ball.center = (pad.centerx, pad.top - BALL_R - 2)
            bx, by = level_cfg["ball_speed"], -level_cfg["ball_speed"]

        # ⏱ 시간 감소
        if launched:
            time_left -= dt
            if time_left <= 0:
                if message_screen("FAILED!", RED, score):
                    main()
                return

        # ⏳ 리스폰 연출
        if respawn_timer > 0:
            respawn_timer -= dt
            ball.centerx = pad.centerx

            screen.fill(GRAY)
            for b in blocks:
                screen.blit(b["image"], b["rect"])  # 블록 이미지 그리기
                text = font_small.render(str(b["score"]), True, WHITE)
                screen.blit(text, (b["rect"].centerx - 10, b["rect"].centery - 10))

            screen.blit(PADDLE_IMAGE, pad)  # 패들 이미지 그리기
            screen.blit(BALL_IMAGE, ball)  # 공 이미지 그리기

            # 별 아이템 그리기
            for star in stars:
                star.draw()

            draw_hud(score, time_left, level_cfg)

            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            count = str(int(respawn_timer) + 1)
            txt = font_big.render(count, True, WHITE)
            screen.blit(
                txt,
                (WIDTH // 2 - txt.get_width() // 2,
                 HEIGHT // 2 - txt.get_height() // 2)
            )

            pygame.display.flip()
            continue

        if not launched:
            ball.centerx = pad.centerx
        else:
            ball.x += bx
            ball.y += by

            if ball.left <= 0 or ball.right >= WIDTH:
                bx = -bx
            if ball.top <= 0:
                by = -by

            if ball.colliderect(pad) and by > 0:
                offset = (ball.centerx - pad.centerx) / (PAD_W / 2)
                bx = int(offset * level_cfg["ball_speed"]) or bx
                by = -abs(by)

            hit_block = None
            for b in blocks:
                if ball.colliderect(b["rect"]):
                    hit_block = b
                    break

            if hit_block:
                # 공이 블록에 부딪혔을 때 점수 감소
                hit_block["score"] -= BALL_DAMAGE
                if hit_block["score"] <= hit_block["threshold"]:  # 점수가 임계값 이하로 떨어지면 깨진 이미지로 변경
                    hit_block["image"] = pygame.image.load(hit_block["broken_image"]).convert()
                    hit_block["image"] = pygame.transform.scale(hit_block["image"], (BLOCK_W, BLOCK_H))

                # 별 아이템 생성
                if hit_block["score"] <= 0:  # 블록이 파괴되었을 때
                    score += hit_block["initial_score"]  # 블록 점수 추가
                    blocks.remove(hit_block)  # 블록 제거
                    # 별 아이템 생성
                    stars.append(Star(hit_block["rect"].centerx, hit_block["rect"].centery, hit_block["initial_score"]))
                
                by = -by

            # 별 아이템과 공 충돌 확인
            for star in stars:
                if ball.colliderect(star.rect):  # 공이 별을 맞혔을 때
                    score += star.score  # 별의 점수 추가
                    stars.remove(star)  # 별 제거

            if ball.bottom >= HEIGHT:
                launched = False
                respawn_timer = 3
                ball.center = (pad.centerx, pad.top - BALL_R - 2)

        # 🎨 렌더링
        screen.fill(GRAY)

        for b in blocks:
            screen.blit(b["image"], b["rect"])  # 블록 이미지 그리기
            text = font_small.render(str(b["score"]), True, WHITE)
            screen.blit(
                text,
                (
                    b["rect"].centerx - text.get_width() // 2,
                    b["rect"].centery - text.get_height() // 2
                )
            )

        screen.blit(PADDLE_IMAGE, pad)  # 패들 이미지 그리기
        screen.blit(BALL_IMAGE, ball)  # 공 이미지 그리기

        # 별 아이템 그리기
        for star in stars:
            star.draw()

        draw_hud(score, time_left, level_cfg)

        pygame.display.flip()


main()