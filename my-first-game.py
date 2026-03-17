import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fancy Particle Playground V2")

clock = pygame.time.Clock()

particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 7)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(50, 100)
        self.max_life = self.life

        self.size = random.randint(4, 8)

        # 네온 느낌 색상
        self.color = pygame.Color(0)
        self.color.hsva = (
            random.randint(0, 360),  # 색상
            80,                      # 채도
            100,                     # 밝기
            100
        )

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vy += 0.1  # 중력

        # 공기 저항 느낌
        self.vx *= 0.98
        self.vy *= 0.98

        self.life -= 1

    def draw(self, surf):
        if self.life > 0:
            # 페이드 아웃
            alpha = int(255 * (self.life / self.max_life))

            glow_surface = pygame.Surface((self.size*4, self.size*4), pygame.SRCALPHA)

            pygame.draw.circle(
                glow_surface,
                (*self.color[:3], alpha),
                (self.size*2, self.size*2),
                self.size
            )

            surf.blit(glow_surface, (self.x - self.size*2, self.y - self.size*2))

    def alive(self):
        return self.life > 0


def draw_background(surface, t):
    for y in range(HEIGHT):
        c = int(50 + 40 * math.sin(y * 0.01 + t))
        color = (20, c, 80 + c//2)
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))


running = True
time = 0

# 잔상용 투명 레이어
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.set_alpha(40)
fade_surface.fill((0, 0, 0))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

  
    if buttons[0]:
        for _ in range(15):
            particles.append(Particle(mouse[0], mouse[1]))

    time += 0.03

    draw_background(screen, time)

    # 잔상 효과
    screen.blit(fade_surface, (0, 0))

    for p in particles:
        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.alive()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()