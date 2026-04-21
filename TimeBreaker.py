import pygame
import sys
import random
import os
import math

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "applegothicmedium", "nanumgothic", "notosanscjk"]
    for name in candidates:
        try:
            font = pygame.font.SysFont(name, size)
            if font and font.get_ascent() > 0:
                return font
        except Exception:
            pass
    return pygame.font.SysFont(None, size)


BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def load_image(*parts, use_alpha=True):
    path = os.path.join(BASE_PATH, *parts)
    image = pygame.image.load(path)
    return image.convert_alpha() if use_alpha else image.convert()


def try_load_bgm():
    bgm_paths = [
        os.path.join(BASE_PATH, "mainbgm.wav"),
        os.path.join(BASE_PATH, "mainbgm.ogg"),
        os.path.join(BASE_PATH, "mainbgm.mp3"),
        os.path.join(BASE_PATH, "assets", "music", "mainbgm.wav"),
        os.path.join(BASE_PATH, "assets", "music", "mainbgm.ogg"),
        os.path.join(BASE_PATH, "assets", "music", "mainbgm.mp3"),
    ]

    print("BASE_PATH:", BASE_PATH)

    for path in bgm_paths:
        print("BGM 확인:", path, "존재:", os.path.exists(path))
        if os.path.exists(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
                print("BGM 재생 성공:", path)
                return True
            except Exception as e:
                print("BGM 재생 실패:", path)
                print("에러 내용:", e)

    print("재생 가능한 BGM 파일을 찾지 못함")
    return False


def try_load_hit_sound():
    hit_paths = [
        os.path.join(BASE_PATH, "hit.wav"),
        os.path.join(BASE_PATH, "assets", "music", "hit.wav"),
        os.path.join(BASE_PATH, "assets", "sounds", "hit.wav"),
    ]

    for path in hit_paths:
        print("히트 사운드 확인:", path, "존재:", os.path.exists(path))
        if os.path.exists(path):
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(0.6)
                print("히트 사운드 로드 성공:", path)
                return sound
            except Exception as e:
                print("히트 사운드 로드 실패:", path)
                print("에러 내용:", e)

    print("재생 가능한 히트 사운드 파일을 찾지 못함")
    return None


WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
RED = (220, 50, 50)
YELLOW = (240, 200, 0)
ORANGE = (240, 140, 0)
GREEN = (50, 200, 50)
BLUE = (50, 120, 220)
BLACK = (0, 0, 0)
CYAN = (60, 220, 220)
PURPLE = (180, 80, 220)

HP_BG = (15, 15, 15)
HP_BORDER = (255, 255, 255)

HUD_BG = (18, 18, 26)
HUD_PANEL = (28, 28, 38)
HUD_BORDER = (220, 220, 220)

UPGRADE_NAME_COLORS = {
    "pierce": (100, 220, 255),
    "explosion": (255, 150, 80),
    "shield": (120, 255, 140),
    "time_stop": (235, 120, 255),
}

BLOCK_SCORE = 100

BLOCK_TYPES = [
    {"color": RED, "score": BLOCK_SCORE, "image": "brick_05.png"},
    {"color": ORANGE, "score": BLOCK_SCORE, "image": "brick_04.png"},
    {"color": YELLOW, "score": BLOCK_SCORE, "image": "brick_03.png"},
    {"color": GREEN, "score": BLOCK_SCORE, "image": "brick_02.png"},
    {"color": BLUE, "score": BLOCK_SCORE, "image": "brick_01.png"},
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Defense Survivor")
clock = pygame.time.Clock()

font = get_korean_font(28)
font_small = get_korean_font(18)
font_big = get_korean_font(70)
font_mid = get_korean_font(22)
font_hp = get_korean_font(16)
font_upgrade_title = get_korean_font(16)
font_upgrade_value = get_korean_font(17)
font_upgrade_hint = get_korean_font(13)

font_levelup_title = get_korean_font(58)
font_levelup_guide = get_korean_font(22)
font_levelup_card_num = get_korean_font(48)
font_levelup_name = get_korean_font(24)
font_levelup_desc = get_korean_font(17)
font_levelup_lv = get_korean_font(18)
font_levelup_current = get_korean_font(18)

BASE_PAD_W, PAD_H = 120, 12
BALL_R = 8
BLOCK_W, BLOCK_H = 72, 22
BLOCK_COLS = 10
BLOCK_MARGIN = 5

TOP_HUD_HEIGHT = 105
BLOCK_TOP = TOP_HUD_HEIGHT + 12

DESCEND_STEP = BLOCK_H + BLOCK_MARGIN
BASE_DESCEND_INTERVAL = 5.5
MIN_DESCEND_INTERVAL = 1.8
SPEED_UP_EVERY = 18
SPEED_UP_AMOUNT = 0.25

DANGER_LINE_Y = HEIGHT - 70
PAD_Y = DANGER_LINE_Y - 28

XP_PER_BLOCK = 1
BASE_XP_TO_LEVEL = 5
XP_GROWTH = 1.35

TOUGH_BLOCK_START_SCORE = 1000
TOUGH_BLOCK_SCORE_STEP = 2000
MAX_TOUGH_HP = 5

UPGRADE_TEXT = {
    "pierce": "관통탄",
    "explosion": "폭발탄",
    "shield": "보호막",
    "time_stop": "시간정지",
}

UPGRADE_DESC = {
    "pierce": "패들 반사 후 제한 관통",
    "explosion": "주변 블럭 폭발 데미지",
    "shield": "데인저 라인 1회 방어",
    "time_stop": "F키로 하강 정지",
}

UPGRADE_MAX_LEVEL = {
    "pierce": 5,
    "explosion": 5,
    "shield": 5,
    "time_stop": 5,
}

PADDLE_IMAGE_ORIGINAL = load_image("assets", "images", "paddle_image.png")
BALL_IMAGE = load_image("assets", "images", "ball_image.png")
BALL_IMAGE = pygame.transform.scale(BALL_IMAGE, (BALL_R * 2, BALL_R * 2))


def get_paddle_surface(width):
    return pygame.transform.scale(PADDLE_IMAGE_ORIGINAL, (width, PAD_H))


def create_block(x, y, hp=1):
    t = random.choice(BLOCK_TYPES)
    rect = pygame.Rect(x, y, BLOCK_W, BLOCK_H)
    block_image = load_image("assets", "images", t["image"], use_alpha=False)
    block_image = pygame.transform.scale(block_image, (BLOCK_W, BLOCK_H))

    return {
        "rect": rect,
        "image": block_image,
        "score": t["score"] * hp,
        "hp": hp,
        "max_hp": hp,
    }


def get_tough_block_hp(score):
    if score < TOUGH_BLOCK_START_SCORE:
        return 1

    extra = (score - TOUGH_BLOCK_START_SCORE) // TOUGH_BLOCK_SCORE_STEP
    return min(2 + extra, MAX_TOUGH_HP)


def should_spawn_tough_block(score):
    return score >= TOUGH_BLOCK_START_SCORE


def make_blocks(rows):
    blocks = []
    for r in range(rows):
        for c in range(BLOCK_COLS):
            x = BLOCK_MARGIN + c * (BLOCK_W + BLOCK_MARGIN)
            y = BLOCK_TOP + r * (BLOCK_H + BLOCK_MARGIN)
            blocks.append(create_block(x, y, hp=1))
    return blocks


def add_new_top_row(blocks, score):
    for b in blocks:
        b["rect"].y += DESCEND_STEP

    empty_cols = random.sample(range(BLOCK_COLS), k=2)
    spawn_cols = [c for c in range(BLOCK_COLS) if c not in empty_cols]

    tough_col = None
    if should_spawn_tough_block(score) and spawn_cols:
        tough_col = random.choice(spawn_cols)

    for c in range(BLOCK_COLS):
        if c in empty_cols:
            continue

        x = BLOCK_MARGIN + c * (BLOCK_W + BLOCK_MARGIN)
        y = BLOCK_TOP

        if c == tough_col:
            hp = get_tough_block_hp(score)
            blocks.append(create_block(x, y, hp=hp))
        else:
            blocks.append(create_block(x, y, hp=1))


def get_available_upgrade_choices(upgrade_levels):
    available = [
        key for key in UPGRADE_TEXT.keys()
        if upgrade_levels[key] < UPGRADE_MAX_LEVEL[key]
    ]

    if not available:
        return []

    count = min(3, len(available))
    return random.sample(available, count)


def get_xp_reward(destroyed_count):
    return destroyed_count * XP_PER_BLOCK


def draw_text_with_shadow(text, font_obj, color, x, y, shadow_color=BLACK, shadow_offset=1):
    shadow = font_obj.render(text, True, shadow_color)
    main = font_obj.render(text, True, color)
    screen.blit(shadow, (x + shadow_offset, y + shadow_offset))
    screen.blit(main, (x, y))


def wrap_text(text, font_obj, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = word if current == "" else current + " " + word
        if font_obj.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def draw_centered_multiline(text_lines, font_obj, color, center_x, start_y, line_gap=3, shadow=True):
    y = start_y
    for line in text_lines:
        surf = font_obj.render(line, True, color)
        x = center_x - surf.get_width() // 2
        if shadow:
            draw_text_with_shadow(line, font_obj, color, x, y, BLACK, 1)
        else:
            screen.blit(surf, (x, y))
        y += surf.get_height() + line_gap


def draw_xp_bar(xp, xp_to_next, level):
    bar_x = 170
    bar_y = HEIGHT - 28
    bar_w = WIDTH - 340
    bar_h = 16

    pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_w, bar_h), border_radius=8)
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=8)

    fill_ratio = 0
    if xp_to_next > 0:
        fill_ratio = max(0, min(1, xp / xp_to_next))

    fill_w = int(bar_w * fill_ratio)
    pygame.draw.rect(screen, CYAN, (bar_x, bar_y, fill_w, bar_h), border_radius=8)

    draw_text_with_shadow(f"Lv {level}", font_small, WHITE, 95, HEIGHT - 32)
    draw_text_with_shadow(f"XP {xp}/{xp_to_next}", font_small, WHITE, WIDTH - 180, HEIGHT - 32)


def draw_upgrade_levels(upgrade_levels, shield_count, stop_charges):
    hud_rect = pygame.Rect(0, 42, WIDTH, TOP_HUD_HEIGHT - 42)
    pygame.draw.rect(screen, HUD_BG, hud_rect)

    card_margin_x = 10
    card_gap = 8
    card_w = (WIDTH - card_margin_x * 2 - card_gap * 3) // 4
    card_h = 46
    card_y = 52

    cards = [
        ("pierce", f"Lv {upgrade_levels['pierce']}/{UPGRADE_MAX_LEVEL['pierce']}", UPGRADE_DESC["pierce"]),
        ("explosion", f"Lv {upgrade_levels['explosion']}/{UPGRADE_MAX_LEVEL['explosion']}", UPGRADE_DESC["explosion"]),
        ("shield", f"{shield_count}개", UPGRADE_DESC["shield"]),
        ("time_stop", f"{stop_charges}개", "F키 사용"),
    ]

    for i, (key, value, desc) in enumerate(cards):
        x = card_margin_x + i * (card_w + card_gap)
        rect = pygame.Rect(x, card_y, card_w, card_h)

        pygame.draw.rect(screen, HUD_PANEL, rect, border_radius=10)
        pygame.draw.rect(screen, HUD_BORDER, rect, 2, border_radius=10)

        name_color = UPGRADE_NAME_COLORS[key]

        draw_text_with_shadow(UPGRADE_TEXT[key], font_upgrade_title, name_color, x + 9, card_y + 6)
        value_x = x + card_w - font_upgrade_value.size(value)[0] - 10
        draw_text_with_shadow(value, font_upgrade_value, WHITE, value_x, card_y + 6)
        draw_text_with_shadow(desc, font_upgrade_hint, (190, 190, 190), x + 9, card_y + 27)


def draw_hud(score, survive_time, descend_interval, xp, xp_to_next, level,
             freeze_timer, upgrade_levels, shield_count, stop_charges):
    top_bar = pygame.Rect(0, 0, WIDTH, 42)
    pygame.draw.rect(screen, HUD_BG, top_bar)

    draw_text_with_shadow(f"Score: {score}", font, WHITE, 10, 10)
    draw_text_with_shadow(f"Time: {int(survive_time)}", font, YELLOW, WIDTH - 135, 10)

    if freeze_timer > 0:
        speed_text = f"Drop: STOP {freeze_timer:.1f}s"
        speed_color = CYAN
    else:
        speed_text = f"Drop: {descend_interval:.1f}s"
        speed_color = GREEN

    center_x = WIDTH // 2 - font_small.size(speed_text)[0] // 2
    draw_text_with_shadow(speed_text, font_small, speed_color, center_x, 14)

    draw_upgrade_levels(upgrade_levels, shield_count, stop_charges)

    draw_text_with_shadow("DANGER LINE", font_small, RED, 10, DANGER_LINE_Y - 24)
    pygame.draw.line(screen, RED, (0, DANGER_LINE_Y), (WIDTH, DANGER_LINE_Y), 2)

    draw_xp_bar(xp, xp_to_next, level)


def draw_levelup_overlay(level, choices, upgrade_levels):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(215)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    title_text = "LEVEL UP!"
    guide_text = "1 / 2 / 3 키로 업그레이드를 선택하세요"
    current_text = f"현재 레벨: {level}"

    title_x = WIDTH // 2 - font_levelup_title.size(title_text)[0] // 2
    guide_x = WIDTH // 2 - font_levelup_guide.size(guide_text)[0] // 2
    current_x = WIDTH // 2 - font_levelup_current.size(current_text)[0] // 2

    draw_text_with_shadow(title_text, font_levelup_title, YELLOW, title_x, 40, BLACK, 2)
    draw_text_with_shadow(guide_text, font_levelup_guide, WHITE, guide_x, 108, BLACK, 1)
    draw_text_with_shadow(current_text, font_levelup_current, WHITE, current_x, 140, BLACK, 1)

    if not choices:
        done_txt = "모든 업그레이드가 최대 레벨입니다"
        done_x = WIDTH // 2 - font_mid.size(done_txt)[0] // 2
        draw_text_with_shadow(done_txt, font_mid, WHITE, done_x, 300)
        return

    card_w = 220
    card_h = 250
    gap = 20
    total_w = card_w * len(choices) + gap * (len(choices) - 1)
    start_x = WIDTH // 2 - total_w // 2
    y = 195

    card_colors = [
        (55, 165, 95),
        (55, 145, 180),
        (130, 75, 170),
    ]

    for i, choice in enumerate(choices):
        x = start_x + i * (card_w + gap)
        rect = pygame.Rect(x, y, card_w, card_h)

        pygame.draw.rect(screen, card_colors[i % len(card_colors)], rect, border_radius=18)
        pygame.draw.rect(screen, WHITE, rect, 3, border_radius=18)

        center_x = rect.centerx

        number = str(i + 1)
        number_x = center_x - font_levelup_card_num.size(number)[0] // 2
        draw_text_with_shadow(number, font_levelup_card_num, WHITE, number_x, rect.y + 12, BLACK, 2)

        name = UPGRADE_TEXT[choice]
        name_x = center_x - font_levelup_name.size(name)[0] // 2
        draw_text_with_shadow(name, font_levelup_name, WHITE, name_x, rect.y + 78, BLACK, 1)

        desc_lines = wrap_text(UPGRADE_DESC[choice], font_levelup_desc, card_w - 24)
        draw_centered_multiline(desc_lines, font_levelup_desc, BLACK, center_x, rect.y + 118, line_gap=3, shadow=False)

        now_lv = upgrade_levels[choice]
        max_lv = UPGRADE_MAX_LEVEL[choice]
        lv_text = f"Lv {now_lv} -> {now_lv + 1} / {max_lv}"
        lv_x = center_x - font_levelup_lv.size(lv_text)[0] // 2
        draw_text_with_shadow(lv_text, font_levelup_lv, BLACK, lv_x, rect.y + card_h - 38, WHITE, 1)


def get_hp_text_color(hp):
    if hp >= 5:
        return RED
    if hp == 4:
        return ORANGE
    if hp == 3:
        return YELLOW
    if hp == 2:
        return CYAN
    return WHITE


def draw_blocks(blocks):
    for b in blocks:
        screen.blit(b["image"], b["rect"])

        if b["max_hp"] > 1:
            if b["hp"] >= 4:
                border_color = RED
            elif b["hp"] == 3:
                border_color = ORANGE
            else:
                border_color = CYAN

            pygame.draw.rect(screen, border_color, b["rect"], 3, border_radius=5)

            hp_str = str(b["hp"])
            hp_text = font_hp.render(hp_str, True, get_hp_text_color(b["hp"]))
            hp_shadow = font_hp.render(hp_str, True, BLACK)

            badge_w = max(22, hp_text.get_width() + 10)
            badge_h = 18
            badge_x = b["rect"].right - badge_w - 3
            badge_y = b["rect"].y + 2

            badge_rect = pygame.Rect(badge_x, badge_y, badge_w, badge_h)

            pygame.draw.rect(screen, HP_BG, badge_rect, border_radius=6)
            pygame.draw.rect(screen, HP_BORDER, badge_rect, 2, border_radius=6)

            text_x = badge_rect.centerx - hp_text.get_width() // 2
            text_y = badge_rect.centery - hp_text.get_height() // 2 - 1

            screen.blit(hp_shadow, (text_x + 1, text_y + 1))
            screen.blit(hp_text, (text_x, text_y))


def message_screen(title, color, score, survive_time, level):
    screen.fill(GRAY)

    title_surface = font_big.render(title, True, color)
    score_surface = font.render(f"Score: {score}", True, WHITE)
    time_surface = font.render(f"Time: {int(survive_time)} sec", True, WHITE)
    level_surface = font.render(f"Level: {level}", True, WHITE)
    guide_surface = font.render("R: Restart   Q: Quit", True, WHITE)

    screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 150))
    screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, 255))
    screen.blit(time_surface, (WIDTH // 2 - time_surface.get_width() // 2, 305))
    screen.blit(level_surface, (WIDTH // 2 - level_surface.get_width() // 2, 355))
    screen.blit(guide_surface, (WIDTH // 2 - guide_surface.get_width() // 2, 420))
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


def apply_upgrade(choice, state):
    if state["upgrade_levels"][choice] >= UPGRADE_MAX_LEVEL[choice]:
        return

    state["upgrade_levels"][choice] += 1

    if choice == "shield":
        state["shield_count"] += 1
    elif choice == "time_stop":
        state["stop_charges"] += 1


def get_explosion_radius(level):
    if level <= 0:
        return 0
    return 35 + (level - 1) * 15


def get_pierce_charges(level):
    if level <= 1:
        return 0
    elif level <= 3:
        return 1
    else:
        return 2


def destroy_blocks(blocks, target_block, explosion_level):
    hit_targets = []

    if target_block in blocks:
        hit_targets.append(target_block)

    if explosion_level > 0:
        radius = get_explosion_radius(explosion_level)
        cx, cy = target_block["rect"].center

        for b in blocks:
            if b == target_block:
                continue
            bx2, by2 = b["rect"].center
            dist = math.hypot(bx2 - cx, by2 - cy)
            if dist <= radius:
                hit_targets.append(b)

    unique_targets = []
    seen_ids = set()
    for b in hit_targets:
        if id(b) not in seen_ids:
            unique_targets.append(b)
            seen_ids.add(id(b))

    destroyed_blocks = []
    destroyed_rects = []

    for b in unique_targets:
        b["hp"] -= 1
        if b["hp"] <= 0:
            destroyed_blocks.append(b)
            destroyed_rects.append(b["rect"].copy())

    for b in destroyed_blocks:
        if b in blocks:
            blocks.remove(b)

    return destroyed_blocks, destroyed_rects


def clamp_nonzero_speed(value, fallback):
    iv = int(value)
    if iv == 0:
        return fallback
    return iv


def main():
    try_load_bgm()
    hit_sound = try_load_hit_sound()

    base_pad_w = BASE_PAD_W
    pad = pygame.Rect(WIDTH // 2 - base_pad_w // 2, PAD_Y, base_pad_w, PAD_H)

    ball = pygame.Rect(0, 0, BALL_R * 2, BALL_R * 2)
    ball.center = (pad.centerx, pad.top - BALL_R - 2)

    ball_speed = 5
    bx, by = ball_speed, -ball_speed

    blocks = make_blocks(2)

    score = 0
    survive_time = 0
    launched = False
    respawn_timer = 0

    descend_timer = 0
    descend_interval = BASE_DESCEND_INTERVAL
    freeze_timer = 0

    xp = 0
    level = 1
    xp_to_next = BASE_XP_TO_LEVEL
    level_up = False
    upgrade_choices = []

    upgrade_levels = {
        "pierce": 0,
        "explosion": 0,
        "shield": 0,
        "time_stop": 0,
    }

    shield_count = 0
    stop_charges = 0
    pierce_hits_left = 0

    while True:
        dt = clock.tick(FPS) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if level_up:
                if e.type == pygame.KEYDOWN:
                    selected_index = None

                    if e.key == pygame.K_1:
                        selected_index = 0
                    elif e.key == pygame.K_2:
                        selected_index = 1
                    elif e.key == pygame.K_3:
                        selected_index = 2

                    if selected_index is not None and selected_index < len(upgrade_choices):
                        state = {
                            "upgrade_levels": upgrade_levels,
                            "shield_count": shield_count,
                            "stop_charges": stop_charges,
                        }

                        apply_upgrade(upgrade_choices[selected_index], state)

                        upgrade_levels = state["upgrade_levels"]
                        shield_count = state["shield_count"]
                        stop_charges = state["stop_charges"]

                        level_up = False

                    elif len(upgrade_choices) == 0:
                        level_up = False
                continue

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if not launched and respawn_timer <= 0:
                        launched = True
                        pierce_hits_left = get_pierce_charges(upgrade_levels["pierce"])

                if e.key == pygame.K_f:
                    if stop_charges > 0 and freeze_timer <= 0 and not level_up:
                        stop_charges -= 1
                        freeze_timer = 2.0 + upgrade_levels["time_stop"] * 0.8

        keys = pygame.key.get_pressed()
        if not level_up:
            if keys[pygame.K_LEFT] and pad.left > 0:
                pad.x -= 7
            if keys[pygame.K_RIGHT] and pad.right < WIDTH:
                pad.x += 7

        is_game_running = (launched or respawn_timer > 0) and not level_up

        if is_game_running:
            survive_time += dt

            if freeze_timer > 0:
                freeze_timer -= dt
                if freeze_timer < 0:
                    freeze_timer = 0
            else:
                descend_timer += dt
                target_interval = BASE_DESCEND_INTERVAL - (int(survive_time // SPEED_UP_EVERY) * SPEED_UP_AMOUNT)
                descend_interval = max(MIN_DESCEND_INTERVAL, target_interval)

                while descend_timer >= descend_interval:
                    descend_timer -= descend_interval
                    add_new_top_row(blocks, score)

        if respawn_timer > 0 and not level_up:
            respawn_timer -= dt
            if respawn_timer <= 0:
                respawn_timer = 0
                launched = True
                bx = random.choice([-ball_speed, ball_speed])
                by = -ball_speed
                pierce_hits_left = get_pierce_charges(upgrade_levels["pierce"])

            ball.center = (pad.centerx, pad.top - BALL_R - 2)

            danger_blocks = [b for b in blocks if b["rect"].bottom >= DANGER_LINE_Y]
            if danger_blocks:
                if shield_count > 0:
                    shield_count -= 1
                    for b in danger_blocks:
                        if b in blocks:
                            blocks.remove(b)
                else:
                    if message_screen("GAME OVER!", RED, score, survive_time, level):
                        main()
                    return

            screen.fill(GRAY)
            draw_blocks(blocks)

            paddle_surface = get_paddle_surface(pad.width)
            screen.blit(paddle_surface, pad)
            screen.blit(BALL_IMAGE, ball)

            draw_hud(
                score, survive_time, descend_interval, xp, xp_to_next, level,
                freeze_timer, upgrade_levels, shield_count, stop_charges
            )

            if respawn_timer > 0:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(150)
                overlay.fill(BLACK)
                screen.blit(overlay, (0, 0))

                count = str(int(respawn_timer) + 1)
                txt = font_big.render(count, True, WHITE)
                screen.blit(
                    txt,
                    (
                        WIDTH // 2 - txt.get_width() // 2,
                        HEIGHT // 2 - txt.get_height() // 2
                    )
                )

            pygame.display.flip()
            continue

        danger_blocks = [b for b in blocks if b["rect"].bottom >= DANGER_LINE_Y]
        if danger_blocks:
            if shield_count > 0:
                shield_count -= 1
                for b in danger_blocks:
                    if b in blocks:
                        blocks.remove(b)
            else:
                if message_screen("GAME OVER!", RED, score, survive_time, level):
                    main()
                return

        if not launched:
            ball.center = (pad.centerx, pad.top - BALL_R - 2)

        elif not level_up:
            ball.x += bx
            ball.y += by

            if ball.left <= 0 or ball.right >= WIDTH:
                bx = -bx
            if ball.top <= 0:
                by = -by

            if ball.colliderect(pad) and by > 0:
                offset = (ball.centerx - pad.centerx) / (pad.width / 2)
                bx = int(offset * ball_speed)

                if bx == 0:
                    bx = 1 if ball.centerx >= pad.centerx else -1

                if bx > ball_speed:
                    bx = ball_speed
                if bx < -ball_speed:
                    bx = -ball_speed

                by = -abs(ball_speed)
                pierce_hits_left = get_pierce_charges(upgrade_levels["pierce"])

            hit_block = None
            for b in blocks:
                if ball.colliderect(b["rect"]):
                    hit_block = b
                    break

            if hit_block:
                if hit_sound is not None:
                    hit_sound.play()

                explosion_level = upgrade_levels["explosion"]

                if pierce_hits_left > 0:
                    explosion_level = 0

                destroyed_blocks, _ = destroy_blocks(blocks, hit_block, explosion_level)

                gained_score = sum(b["score"] for b in destroyed_blocks)
                destroyed_count = len(destroyed_blocks)

                score += gained_score
                xp += get_xp_reward(destroyed_count)

                while xp >= xp_to_next:
                    xp -= xp_to_next
                    level += 1
                    xp_to_next = max(1, int(xp_to_next * XP_GROWTH))
                    level_up = True
                    upgrade_choices = get_available_upgrade_choices(upgrade_levels)
                    break

                if pierce_hits_left > 0:
                    pierce_hits_left -= 1
                    bx = clamp_nonzero_speed(bx * 0.9, 1 if bx >= 0 else -1)
                    by = clamp_nonzero_speed(by * 0.9, -1 if by < 0 else 1)
                else:
                    by = -by

            if ball.bottom >= HEIGHT:
                launched = False
                respawn_timer = 2.5
                ball.center = (pad.centerx, pad.top - BALL_R - 2)

        screen.fill(GRAY)
        draw_blocks(blocks)

        paddle_surface = get_paddle_surface(pad.width)
        screen.blit(paddle_surface, pad)
        screen.blit(BALL_IMAGE, ball)

        draw_hud(
            score, survive_time, descend_interval, xp, xp_to_next, level,
            freeze_timer, upgrade_levels, shield_count, stop_charges
        )

        if level_up:
            draw_levelup_overlay(level, upgrade_choices, upgrade_levels)

        pygame.display.flip()


main()