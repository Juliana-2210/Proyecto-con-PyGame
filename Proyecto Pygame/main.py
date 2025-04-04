import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Ninja - Shadows of the Dojo")

background = pygame.image.load("assets/background.jpg")
ninja_img = pygame.image.load("assets/ninja.png")
enemy_img = pygame.image.load("assets/enemy.png")
scroll_img = pygame.image.load("assets/scroll.png")

pygame.mixer.music.load("assets/background_music.wav")
pygame.mixer.music.play(-1)

ninja_x, ninja_y = WIDTH // 2, HEIGHT - 100
ninja_speed = 7
level = 1
enemy_speed = 2
enemies = [(random.randint(50, 750), random.randint(50, 500))]
scrolls = [(random.randint(50, 750), random.randint(50, 500)) for _ in range(3)]
game_started = False

def move_ninja(keys, x, y):
    if keys[pygame.K_LEFT] and x > 0: x -= ninja_speed
    if keys[pygame.K_RIGHT] and x < WIDTH - 50: x += ninja_speed
    if keys[pygame.K_UP] and y > 0: y -= ninja_speed
    if keys[pygame.K_DOWN] and y < HEIGHT - 50: y += ninja_speed
    return x, y

def move_enemies(enemies, ninja_x, ninja_y):
    new_enemies = []
    for ex, ey in enemies:
        if ex < ninja_x: ex += min(enemy_speed, ninja_x - ex)
        elif ex > ninja_x: ex -= min(enemy_speed, ex - ninja_x)
        if ey < ninja_y: ey += min(enemy_speed, ninja_y - ey)
        elif ey > ninja_y: ey -= min(enemy_speed, ey - ninja_y)
        new_enemies.append((ex, ey))
    return new_enemies

def check_scroll_collision(ninja_x, ninja_y, scrolls):
    ninja_rect = pygame.Rect(ninja_x, ninja_y, 50, 50)
    new_scrolls = []
    for sx, sy in scrolls:
        scroll_rect = pygame.Rect(sx, sy, 30, 30)
        if not ninja_rect.colliderect(scroll_rect):
            new_scrolls.append((sx, sy))
    return new_scrolls

def check_enemy_collision(ninja_x, ninja_y, enemies):
    ninja_rect = pygame.Rect(ninja_x, ninja_y, 50, 50)
    for ex, ey in enemies:
        if ninja_rect.colliderect(pygame.Rect(ex, ey, 50, 50)):
            return True
    return False

def draw_text(text, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    screen.blit(font.render(text, True, color), (x, y))

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_started = True
    
    if not game_started:
        draw_text("🎴 Pixel Ninja - Shadows of the Dojo 🎮", 50, WIDTH // 2 - 250, HEIGHT // 2 - 50, (255, 255, 255))
        draw_text("Presiona ESPACIO para comenzar", 40, WIDTH // 2 - 200, HEIGHT // 2 + 20, (255, 255, 255))
        pygame.display.update()
        continue
    
    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()
    ninja_x, ninja_y = move_ninja(keys, ninja_x, ninja_y)
    
    screen.blit(ninja_img, (ninja_x, ninja_y))
    for ex, ey in enemies:
        screen.blit(enemy_img, (ex, ey))
    for sx, sy in scrolls:
        screen.blit(scroll_img, (sx, sy))
    
    scrolls = check_scroll_collision(ninja_x, ninja_y, scrolls)
    
    if check_enemy_collision(ninja_x, ninja_y, enemies):
        screen.fill((0, 0, 0))
        draw_text("GAME OVER", 60, WIDTH // 2 - 100, HEIGHT // 2, (255, 0, 0))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
        break
    
    if len(scrolls) == 0:
        level += 1
        scrolls = [(random.randint(50, 750), random.randint(50, 500)) for _ in range(3)]
        enemies.append((random.randint(50, 750), random.randint(50, 500)))
        enemy_speed += 0.2
    
    enemies = move_enemies(enemies, ninja_x, ninja_y)
    draw_text(f"Nivel: {level}", 30, 10, 10)
    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
