import pygame

from ui.button import Button


class MenuScreen:

    def __init__(self, font):

        self.font = font

        self.title_font = pygame.font.SysFont(
            None,
            90
        )

        self.start_button = Button(
            490,
            280,
            300,
            60,
            "Start Game",
            font
        )

        self.settings_button = Button(
            490,
            370,
            300,
            60,
            "Settings",
            font
        )

        self.exit_button = Button(
            490,
            460,
            300,
            60,
            "Exit",
            font
        )

    def draw(self, screen, width, height):

        screen.fill((20, 20, 30))

        title = self.title_font.render(
            "Breakout Defense DX",
            True,
            (255, 255, 255)
        )

        screen.blit(
            title,
            (
                width // 2 - title.get_width() // 2,
                120
            )
        )

        self.start_button.draw(screen)
        self.settings_button.draw(screen)
        self.exit_button.draw(screen)