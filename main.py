import pygame
import sys

from core.gamestate import GameState
from core.game import Game
from ui.menu import MenuScreen


pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cube Survivor")

clock = pygame.time.Clock()

ui_font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

menu = MenuScreen(ui_font)

state = GameState.MENU
game = Game()

paused = False
show_controls = False


CONTROLS_LINES = [
    "WASD  -  Move",
    "Mouse  -  Aim (auto-fire toward cursor)",
    "Left Shift  -  Dash",
    "1 / 2 / 3  -  Pick upgrade on level up",
    "P  -  Pause      ESC  -  Back to menu",
    "",
    "Click anywhere to close",
]


def draw_overlay_box(lines, title):

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    screen.blit(overlay, (0, 0))

    head = ui_font.render(title, True, (255, 255, 0))
    screen.blit(head, (WIDTH // 2 - head.get_width() // 2, 170))

    for i, line in enumerate(lines):
        text = small_font.render(line, True, (230, 230, 230))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 250 + i * 42))


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ----------------------------- MENU ----------------------------- #
        if state == GameState.MENU:

            if show_controls:
                if event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN
                ):
                    show_controls = False
                continue

            if menu.start_button.is_clicked(event):
                game = Game()
                paused = False
                state = GameState.PLAYING

            elif menu.controls_button.is_clicked(event):
                show_controls = True

            elif menu.exit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game = Game()
                paused = False
                state = GameState.PLAYING

        # ---------------------------- PLAYING --------------------------- #
        elif state == GameState.PLAYING:

            if event.type == pygame.KEYDOWN:

                # 레벨업 선택
                if game.level_up_active:
                    if event.key == pygame.K_1:
                        game.apply_upgrade(game.upgrade_choices[0])
                    elif event.key == pygame.K_2:
                        game.apply_upgrade(game.upgrade_choices[1])
                    elif event.key == pygame.K_3:
                        game.apply_upgrade(game.upgrade_choices[2])

                # 게임오버 후 재시작
                if game.game_over and event.key == pygame.K_r:
                    game = Game()
                    paused = False

                # 일시정지 토글 (레벨업/게임오버 중에는 무시)
                if event.key == pygame.K_p and not (
                    game.level_up_active or game.game_over
                ):
                    paused = not paused

                if event.key == pygame.K_ESCAPE:
                    state = GameState.MENU
                    paused = False

    # ------------------------------- DRAW ------------------------------- #
    if state == GameState.MENU:

        menu.draw(screen, WIDTH, HEIGHT)

        hint = small_font.render(
            "Press ENTER or click Start Game", True, (150, 150, 160)
        )
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 560))

        if show_controls:
            draw_overlay_box(CONTROLS_LINES, "CONTROLS")

    elif state == GameState.PLAYING:

        if not paused:
            game.update()

        game.draw(screen)

        if paused:
            draw_overlay_box(
                ["Press P to resume", "ESC for menu"], "PAUSED"
            )

    pygame.display.flip()
    clock.tick(60)
