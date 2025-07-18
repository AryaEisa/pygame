# Importera nödvändiga bibliotek
import pygame
import random
import sys
# Lägg till högst upp efter import
# anime_bg will be loaded after W and H are defined
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # När det körs som .exe
    except Exception:
        base_path = os.path.abspath(".")  # När det körs som .py
    return os.path.join(base_path, relative_path)

# Initiera Pygame
pygame.init()

# Definiera skärmstorlek (bredd och höjd)
W, H = 600, 600

# Skapa fönstret med angiven storlek
screen = pygame.display.set_mode((W, H))

# Skapa fönstret med angiven storlek
screen = pygame.display.set_mode((W, H))

# Ladda och skala bakgrundsbilden nu när W och H är definierade
anime_bg = pygame.image.load(resource_path("anime.png"))
# Skala bakgrundsbilden till skärmstorleken
anime_bg = pygame.transform.scale(anime_bg, (W, H))

# Definiera färger (RGB-format)
WHT, BLU, RED, BLK = (255, 255, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0)

# Skapa en klocka för att kontrollera FPS
clock = pygame.time.Clock()

# Definiera fonten som ska användas (standardfont, storlek 36)
font = pygame.font.SysFont(None, 36)

# Skapa spelarens plattform (rektangel: x, y, bredd, höjd)
paddle = pygame.Rect(W // 2 - 60, H - 20, 30, 10)

# Skapa blocket som faller (rektangel: slumpad x, startar på y=0, bredd och höjd = 20)
block = pygame.Rect(random.randint(0, W - 10), 0, 10, 10)

# Startfart för blocket
b_speed = 30

# Startpoäng
score = 0

# Variabel för att hålla spelloopen igång
run = True

def game_loop():
    # Skapa spelarens plattform (rektangel: x, y, bredd, höjd)
    paddle = pygame.Rect(W // 2 - 60, H - 20, 120, 10)
    # Skapa blocket som faller (rektangel: slumpad x, startar på y=0, bredd och höjd = 20)
    block = pygame.Rect(random.randint(0, W - 20), 0, 20, 20)
    # Startfart för blocket
    b_speed = 5
    # Startpoäng
    score = 0
    # Variabel för att hålla spelloopen igång
    run = True

    while run:
        # Rita bakgrundsbilden
        screen.blit(anime_bg, (0, 0))
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))  # Halvtransparent svart överlägg
        screen.blit(overlay, (0, 0))

        # Hantera händelser (t.ex. fönsterstängning)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Hämta vilka tangenter som trycks ned
        keys = pygame.key.get_pressed()

        # Flytta plattformen åt vänster om vänsterpil trycks ned
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-20, 0)

        # Flytta plattformen åt höger om högerpil trycks ned
        if keys[pygame.K_RIGHT] and paddle.right < W:
            paddle.move_ip(20, 0)

        # Flytta blocket nedåt med aktuell hastighet
        block.y += b_speed

        # Om blocket träffar plattformen
        if block.colliderect(paddle):
            # Starta om blockets position högst upp med ny slumpmässig x
            block.y = 0
            block.x = random.randint(0, W - 20)
            # Öka poängen
            score += 1
            # Gör spelet svårare genom att öka blockets hastighet
            b_speed += 0.5

        # Om blocket når botten utan att bli fångat
        if block.y > H:
            # Visa "Game Over"-text med slutpoängen
            game_over = font.render(f"Game Over! Final Score: {score}", True, RED)
            screen.blit(game_over, (W // 2 - 150, H // 2))
            restart_text = font.render("Press SPACE to restart, ESC to quit", True, WHT)
            screen.blit(restart_text, (W // 2 - 150, H // 2 + 40))
            # Uppdatera skärmen
            pygame.display.flip()
            # Vänta 2 sekunder innan spelet avslutas
            pygame.time.wait(2000)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            waiting = False
                            return True  # Restart
                        if event.key == pygame.K_ESCAPE:
                            waiting = False
                            return False  # Quit
            run = False

        # Rita plattformen på skärmen
        pygame.draw.rect(screen, WHT, paddle)

        # Rita blocket på skärmen
        pygame.draw.rect(screen, BLU, block)

        # Skapa text för poängen och visa den i övre vänstra hörnet
        score_text = font.render(f"Score: {score}", True, WHT)
        screen.blit(score_text, (10, 10))

        # Uppdatera hela fönstret
        pygame.display.flip()

        # Vänta så att spelet körs i 60 FPS
        clock.tick(60)

# Main loop to allow replay
while True:
    play_again = game_loop()
    if not play_again:
        break
pygame.quit()
sys.exit()
# ...existing code...