import pygame


class Button:

    def __init__(self, x, y, width, height, text, font):

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text
        self.font = font

    def draw(self, screen):

        mouse_pos = pygame.mouse.get_pos()

        color = (70, 70, 70)

        if self.rect.collidepoint(mouse_pos):
            color = (110, 110, 110)

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.rect,
            2,
            border_radius=12
        )

        text_surface = self.font.render(
            self.text,
            True,
            (255, 255, 255)
        )

        screen.blit(
            text_surface,
            (
                self.rect.centerx - text_surface.get_width() // 2,
                self.rect.centery - text_surface.get_height() // 2
            )
        )

    def is_clicked(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                return self.rect.collidepoint(event.pos)

        return False