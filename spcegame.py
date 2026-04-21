import pygame
import sys
import time
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Blogger - Final Edition")
clock = pygame.time.Clock()

# Colors & Glow
WHITE, RED, NEON_RED = (255, 255, 255), (255, 50, 50), (255, 0, 100)
BRIGHT_SILVER, ORANGE, ROCK_COLOR = (220, 220, 220), (255, 165, 0), (120, 100, 80)
glow_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.circle(glow_surf, (255, 100, 0, 150), (50, 50), 30)

# Game variables
player_x, player_y = 400, 500
bullets, asteroids = [], []
planet_x, black_hole_angle = -100, 0
game_active, last_shot = True, 0
font = pygame.font.Font(None, 74)


def draw_rocket(x, y):
    # Wings
    pygame.draw.polygon(screen, (100, 100, 100), [(x + 5, y + 50), (x + 25, y + 30), (x + 5, y + 60)])
    pygame.draw.polygon(screen, (100, 100, 100), [(x + 45, y + 50), (x + 25, y + 30), (x + 45, y + 60)])
    # Body
    pygame.draw.polygon(screen, BRIGHT_SILVER, [(x + 25, y + 5), (x + 10, y + 50), (x + 40, y + 50)])
    # Cockpit
    pygame.draw.ellipse(screen, (0, 200, 255), (x + 20, y + 15, 10, 15))
    # Engine Flame
    pygame.draw.polygon(screen, ORANGE, [(x + 15, y + 50), (x + 35, y + 50), (x + 25, y + 50 + random.randint(15, 30))])
    screen.blit(glow_surf, (x - 20, y + 25))


while True:
    # 1. Background (Gradient + Planet + Black Hole)
    for i in range(HEIGHT):
        pygame.draw.line(screen, (0, 0, int((HEIGHT - i) * (20 / HEIGHT))), (0, i), (WIDTH, i))

    planet_x += 0.5
    if planet_x > 900: planet_x = -100
    pygame.draw.circle(screen, (50, 100, 200), (int(planet_x), 100), 40)
    pygame.draw.circle(screen, (10, 10, 30), (400, 0), 60)

    # 2. Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        if game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if time.time() - last_shot > 0.3:
                bullets.append([player_x + 22, player_y])
                last_shot = time.time()
        if not game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_active, bullets, asteroids = True, [], []

    # 3. Game Logic
    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0: player_x -= 8
        if keys[pygame.K_RIGHT] and player_x < 760: player_x += 8

        if random.randint(1, 20) == 1:
            asteroids.append([random.randint(0, 750), -50, random.uniform(2, 5)])

        draw_rocket(player_x, player_y)

        for a in asteroids[:]:
            a[1] += a[2]
            pygame.draw.circle(screen, ROCK_COLOR, (int(a[0] + 20), int(a[1] + 20)), 20)
            if pygame.Rect(player_x, player_y, 40, 50).colliderect(pygame.Rect(a[0], a[1], 40, 40)): game_active = False
            if a[1] > 600: asteroids.remove(a)

        for b in bullets[:]:
            b[1] -= 15
            pygame.draw.line(screen, (255, 255, 255), (b[0], b[1]), (b[0], b[1] + 10), 3)
            for a in asteroids[:]:
                if pygame.Rect(b[0], b[1], 5, 10).colliderect(pygame.Rect(a[0], a[1], 40, 40)):
                    asteroids.remove(a)
                    if b in bullets: bullets.remove(b)
            if b[1] < 0: bullets.remove(b)
    else:
        screen.blit(font.render("YOU LOSE", True, NEON_RED), (280, 250))
        screen.blit(pygame.font.Font(None, 36).render("Press R to Restart", True, WHITE), (300, 320))

    pygame.display.update()
    clock.tick(60)