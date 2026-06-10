import pygame

from entities.player import Player


class Game:

    def __init__(self):

        self.background_color = (25, 25, 35)

        self.player = Player()

        self.font = pygame.font.SysFont(None, 40)

    def update(self):

        self.player.update()

    def draw(self, screen):

        screen.fill(self.background_color)

        self.player.draw(screen)

        text = self.font.render(
            "WASD TO MOVE",
            True,
            (255, 255, 255)
        )

        screen.blit(text, (20, 20))