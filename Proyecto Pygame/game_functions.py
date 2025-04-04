import pygame

def show_menu(screen):
    """Muestra el menú de inicio"""
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_text(screen, "Pixel Ninja - Shadows of the Dojo", 40, 180, 200)
        draw_text(screen, "Presiona ESPACIO para comenzar", 30, 220, 300)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False

def draw_text(screen, text, size, x, y, color=(255, 255, 255)):
    """Dibuja texto en pantalla"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def move_ninja(keys, x, y, speed, width, height):
    """Mueve al ninja con las teclas de flecha y evita que salga de la pantalla"""
    if keys[pygame.K_LEFT] and x > 0:
        x -= speed
    if keys[pygame.K_RIGHT] and x < width - 50:
        x += speed
    if keys[pygame.K_UP] and y > 0:
        y -= speed
    if keys[pygame.K_DOWN] and y < height - 50:
        y += speed
    return x, y

def check_collision(ninja_x, ninja_y, scrolls):
    """Verifica colisiones entre el ninja y los pergaminos"""
    ninja_rect = pygame.Rect(ninja_x, ninja_y, 50, 50)
    return [(sx, sy) for sx, sy in scrolls if not ninja_rect.colliderect(pygame.Rect(sx, sy, 40, 40))]

def move_enemies(enemies, ninja_x, ninja_y, speed):
    """Mueve los enemigos hacia el ninja"""
    new_positions = []
    for ex, ey in enemies:
        if ex < ninja_x:
            ex += speed
        elif ex > ninja_x:
            ex -= speed
        if ey < ninja_y:
            ey += speed
        elif ey > ninja_y:
            ey -= speed
        new_positions.append((ex, ey))
    return new_positions

def check_game_over(ninja_x, ninja_y, enemies):
    """Verifica si los enemigos alcanzan al ninja"""
    ninja_rect = pygame.Rect(ninja_x, ninja_y, 50, 50)
    for ex, ey in enemies:
        enemy_rect = pygame.Rect(ex, ey, 50, 50)
        if ninja_rect.colliderect(enemy_rect):  # Si hay colisión, termina el juego
            return True
    return False
