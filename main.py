import pygame
import os
import sys
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running Ralph")

# Colors
SKY_BLUE = (135, 206, 235)
LIGHT_BROWN = (210, 180, 140)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load assets
ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

def load_image(name):
    return pygame.image.load(os.path.join(ASSETS_PATH, name)).convert_alpha()

def load_sound(name):
    return pygame.mixer.Sound(os.path.join(ASSETS_PATH, name))

DOG_IMG = load_image('dog.png')
COW_IMG = load_image('cow.png')
COW_MAD_IMG = load_image('cow_mad.png')
HORSESHOE_IMG = load_image('horseshoe.png')
JUMP_SOUND = load_sound('jump.wav')
KICK_SOUND = load_sound('kick.wav')

FONT = pygame.font.SysFont('arial', 28)
BIG_FONT = pygame.font.SysFont('arial', 48)
SMALL_FONT = pygame.font.SysFont('arial', 22)

clock = pygame.time.Clock()

# Game variables
gravity = 0.8
score = 0
high_score = 0
lives = 5

# Load or create highscore file
HS_FILE = "highscore.txt"
if not os.path.exists(HS_FILE):
    with open(HS_FILE, 'w') as f:
        f.write("0\n---")
with open(HS_FILE, 'r') as f:
    lines = f.read().splitlines()
    high_score = int(lines[0])
    high_score_initials = lines[1] if len(lines) > 1 else "---"

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(DOG_IMG, (50, 50))
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 40))
        self.pos = pygame.Vector2(self.rect.topleft)
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = True
        self.lives = lives

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.pos.x -= 5
        if keys[pygame.K_RIGHT]:
            self.pos.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = -15
            self.on_ground = False
            JUMP_SOUND.play()

    def apply_gravity(self):
        self.vel.y += gravity
        self.pos.y += self.vel.y
        if self.pos.y >= HEIGHT - 90:
            self.pos.y = HEIGHT - 90
            self.vel.y = 0
            self.on_ground = True

    def update(self):
        self.input()
        self.apply_gravity()
        self.rect.topleft = self.pos

class Cow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(COW_IMG, (60, 60))
        self.mad_image = pygame.transform.scale(COW_MAD_IMG, (60, 60))
        self.rect = self.image.get_rect(midbottom=(WIDTH - 100, HEIGHT - 40))
        self.pos = pygame.Vector2(self.rect.topleft)
        self.speed = 2
        self.kicking = False
        self.kick_timer = 0

    def update(self, player_pos):
        dist = abs(player_pos.x - self.pos.x)
        if dist < 50:
            # kick Ralph
            if not self.kicking:
                self.kicking = True
                self.kick_timer = pygame.time.get_ticks()
                KICK_SOUND.play()
        elif dist > 150:
            # chase Ralph
            if player_pos.x < self.pos.x:
                self.pos.x -= self.speed
            else:
                self.pos.x += self.speed
            self.kicking = False
        else:
            self.kicking = False

        # Reset kick animation after 1 second
        if self.kicking and pygame.time.get_ticks() - self.kick_timer > 1000:
            self.kicking = False

        self.rect.topleft = self.pos

    def draw(self, surface):
        if self.kicking:
            surface.blit(self.mad_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

class Horseshoe(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.transform.scale(HORSESHOE_IMG, (30, 20))
        self.rect = self.image.get_rect(midbottom=(x, HEIGHT - 40))

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

# Functions for splash, game over, etc.
def draw_text_center(surface, text, font, color, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    surface.blit(render, rect)

def splash_screen():
    SCREEN.fill(SKY_BLUE)
    draw_text_center(SCREEN, "🐶 RUNNING RALPH 🐮", BIG_FONT, BLACK, HEIGHT // 2 - 50)
    draw_text_center(SCREEN, "Press SPACE to start", FONT, BLACK, HEIGHT // 2 + 30)
    pygame.display.flip()

    barking_sound = JUMP_SOUND  # reuse jump sound as bark placeholder
    barking_sound.play()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
        clock.tick(60)

def game_over_screen(final_score):
    global high_score, high_score_initials
    SCREEN.fill(SKY_BLUE)

    # Update high score
    if final_score > high_score:
        high_score = final_score
        # Ask for initials
        initials = ""
        entering = True
        while entering:
            SCREEN.fill(SKY_BLUE)
            draw_text_center(SCREEN, f"New High Score: {final_score}", BIG_FONT, BLACK, HEIGHT//4)
            draw_text_center(SCREEN, "Enter your initials:", FONT, BLACK, HEIGHT//2 - 30)
            draw_text_center(SCREEN, initials, BIG_FONT, BLACK, HEIGHT//2 + 30)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        initials = initials[:-1]
                    elif event.key == pygame.K_RETURN and len(initials) > 0:
                        entering = False
                    elif len(initials) < 3 and event.unicode.isalpha():
                        initials += event.unicode.upper()

            clock.tick(30)

        high_score_initials = initials
        with open(HS_FILE, 'w') as f:
            f.write(f"{high_score}\n{high_score_initials}")

    else:
        draw_text_center(SCREEN, f"Score: {final_score}", BIG_FONT, BLACK, HEIGHT // 4)
        draw_text_center(SCREEN, f"High Score: {high_score} ({high_score_initials})", FONT, BLACK, HEIGHT // 4 + 60)

    # Credits scroll
    credits = [
        "Lead Developer: Dennis Hendrix",
        "Artistic Inspiration: Ralph Hendrix",
        "Logistical Support: Lee Ann Short",
        "Game Tester: Bernie Short",
        "",
        "Press Enter to Restart or Esc to Quit"
    ]

    y_offset = HEIGHT
    scrolling = True
    while scrolling:
        SCREEN.fill(SKY_BLUE)
        # Draw score and high score on top
        draw_text_center(SCREEN, f"Score: {final_score}", BIG_FONT, BLACK, 50)
        draw_text_center(SCREEN, f"High Score: {high_score} ({high_score_initials})", FONT, BLACK, 100)

        # Scroll credits
        y_offset -= 1
        for i, line in enumerate(credits):
            text_surface = FONT.render(line, True, BLACK)
            SCREEN.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, y_offset + i*30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    scrolling = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if y_offset + len(credits)*30 < 0:
            scrolling = False

        clock.tick(60)

def main():
    global score

    splash_screen()

    player = Player()
    cow = Cow()
    horseshoes = pygame.sprite.Group()

    running = True
    game_speed = 5
    spawn_timer = 0
    score = 0
    lives_left = player.lives

    while running:
        dt = clock.tick(60) / 1000
        SCREEN.fill(SKY_BLUE)
        pygame.draw.rect(SCREEN, LIGHT_BROWN, (0, HEIGHT - 40, WIDTH, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update()
        cow.update(player.pos)

        # Spawn horseshoes randomly
        spawn_timer += dt
        if spawn_timer > 2:
            spawn_timer = 0
            horseshoe = Horseshoe(WIDTH + 30)
            horseshoes.add(horseshoe)

        # Update horseshoes
        for h in horseshoes:
            h.update(game_speed)
            if player.rect.colliderect(h.rect):
                # Jump sound played on jump, no penalty here
                pass
            if h.rect.right < 0:
                horseshoes.remove(h)

        # Check collision between player and cow
        if player.rect.colliderect(cow.rect):
            # Determine kick and damage timing
            if not cow.kicking:
                lives_left -= 1
                KICK_SOUND.play()
                cow.kicking = True
                cow.kick_timer = pygame.time.get_ticks()
                if lives_left <= 0:
                    running = False

        cow.draw(SCREEN)
        SCREEN.blit(player.image, player.rect)
        horseshoes.draw(SCREEN)

        # Update score only when cow moves (chasing)
        if abs(player.pos.x - cow.pos.x) > 150:
            score += dt

        # Increase difficulty over time
        if int(score) % 10 == 0 and int(score) > 0:
            game_speed = min(15, 5 + int(score) // 10)

        # Draw UI
        score_text = FONT.render(f"Score: {int(score)}", True, BLACK)
        lives_text = FONT.render(f"Lives: {lives_left}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(lives_text, (WIDTH - 110, 10))

        pygame.display.flip()

    game_over_screen(int(score))

if __name__ == "__main__":
    main()
