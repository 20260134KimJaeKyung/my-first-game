import pygame
import sys

from core.gamestate import GameState
from core.game import Game

pygame.init()

WIDTH = 1280
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cube Survivor")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 70)

state = GameState.MENU

game = Game()

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == GameState.MENU:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    state = GameState.PLAYING

        elif state == GameState.PLAYING:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    state = GameState.MENU

    if state == GameState.MENU:

        screen.fill((20, 20, 30))

        title = font.render(
            "CUBE SURVIVOR",
            True,
            (255, 255, 255)
        )

        start = pygame.font.SysFont(
            None,
            40
        ).render(
            "Press ENTER To Start",
            True,
            (200, 200, 200)
        )

        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                250
            )
        )

        screen.blit(
            start,
            (
                WIDTH // 2 - start.get_width() // 2,
                360
            )
        )

    elif state == GameState.PLAYING:

        game.update()
        game.draw(screen)

    pygame.display.flip()
    clock.tick(60)