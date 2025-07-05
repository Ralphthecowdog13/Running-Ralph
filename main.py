import pygame
import random
import os
import sys
import time

WIDTH, HEIGHT = 800, 400
FPS = 60

SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (210, 180, 140)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

def load_image(path, size=None):
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

class Player:
    def __init__(self):
        self.image = load_image(os.path.join('assets', 'dog.png'), (40, 40))
        self.rect = self.image.get_rect(midbottom=(100, HEIGHT - 20))
        self.vel_y = 0
        self.jump = False
        self.lives = 5
        self.on_ground = True

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if not self.jump and keys[pygame.K_SPACE] and self.on_ground:
            self.jump = True
            self.vel_y = -14
            self.on_ground = False
            if jump_sound:
                jump_sound.play()
        if self.jump:
            self.rect.y += self.vel_y
            self.vel_y += 0.8
            if self.rect.bottom >= HEIGHT - 20:
                self.rect.bottom = HEIGHT - 20
                self.jump = False
                self.on_ground = True

    def draw(self, win):
        win.blit(self.image, self.rect)

class Cow:
    def __init__(self):
        self.normal_img = load_image(os.path.join('assets', 'cow.png'), (60, 40))
        self.chase_img = load_image(os.path.join('assets', 'cow_mad.png'), (60, 40))
        self.image = self.normal_img
        self.rect = self.image.get_rect(midbottom=(300, HEIGHT - 20))
        self.normal_speed = 2
        self.chase_speed = 4
        self.chasing = False
        self.chase_start_time = 0
        self.chase_duration = 3
        self.chase_cooldown = 5
        self.last_chase_end = 0

    def update(self, player_rect):
        dist = player_rect.x - self.rect.x
        now = time.time()
        if abs(dist) > 150 and not self.chasing and (now - self.last_chase_end) > self.chase_cooldown:
            self.chasing = True
            self.chase_start_time = now
            self.image = self.chase_img
        if self.chasing and (now - self.chase_start_time) > self.chase_duration:
            self.chasing = False
            self.last_chase_end = now
            self.image = self.normal_img
        if abs(dist) < 40:
            return "kick"
        if self.chasing:
            if dist > 0:
                self.rect.x += self.chase_speed
            else:
                self.rect.x -= self.chase_speed
        else:
            self.rect.x += self.normal_speed
            return "moving"
        return None

    def draw(self, win):
        win.blit(self.image, self.rect)

class Obstacle:
    def __init__(self, x):
        self.image = load_image(os.path.join('assets', 'horseshoe.png'), (20, 20))
        self.rect = self.image.get_rect(midbottom=(x, HEIGHT - 20))

    def update(self):
        self.rect.x -= 3

    def draw(self, win):
        win.blit(self.image, self.rect)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Running Ralph")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

try:
    jump_sound = load_sound(os.path.join('assets', 'jump.wav'))
    kick_sound = load_sound(os.path.join('assets', 'kick.wav'))
except:
    jump_sound, kick_sound = None, None

def save_score(initials, score):
    usb_path = os.path.join(os.path.dirname(sys.argv[0]), "scores")
    os.makedirs(usb_path, exist_ok=True)
    with open(os.path.join(usb_path, "high_scores.txt"), "a") as file:
        file.write(f"{initials} {score}\\n")

def game_over_screen(score):
    WIN.fill(SKY_BLUE)
    text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))

    initials = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and initials:
                    save_score(initials, score)
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]
                elif len(initials) < 3 and event.unicode.isalpha():
                    initials += event.unicode.upper()

        WIN.fill(SKY_BLUE)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))
        prompt = font.render("Enter initials: " + initials, True, BLACK)
        WIN.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        clock.tick(30)

def main_menu():
    WIN.fill(SKY_BLUE)
    title = font.render("Running Ralph", True, BLACK)
    prompt = font.render("Press Enter to Start", True, BLACK)
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
    WIN.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
        clock.tick(30)

def pause_screen():
    pause_text = font.render("Paused. Press P to resume.", True, BLACK)
    WIN.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2))
    pygame.display.update()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False
        clock.tick(15)

def main():
    player = Player()
    cow = Cow()
    obstacles = []
    score = 0
    last_score_time = time.time()
    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause_screen()
        player.update(keys)
        cow_state = cow.update(player.rect)
        now = time.time()
        if cow_state == "moving" and now - last_score_time >= 1:
            score += 1
            last_score_time = now
        if cow_state == "kick":
            player.lives -= 1
            if kick_sound:
                kick_sound.play()
            pygame.time.delay(500)
        for obs in obstacles[:]:
            obs.update()
            if player.rect.colliderect(obs.rect):
                player.lives -= 1
                if kick_sound:
                    kick_sound.play()
                obstacles.remove(obs)
            elif obs.rect.right < 0:
                obstacles.remove(obs)
        if random.randint(1, 100) < 2:
            obstacles.append(Obstacle(WIDTH + 20))
        WIN.fill(SKY_BLUE)
        pygame.draw.rect(WIN, GROUND_BROWN, (0, HEIGHT - 20, WIDTH, 20))
        player.draw(WIN)
        cow.draw(WIN)
        for obs in obstacles:
            obs.draw(WIN)
        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
        WIN.blit(score_text, (10, 10))
        WIN.blit(lives_text, (10, 40))
        pygame.display.update()
        if player.lives <= 0:
            running = False
    game_over_screen(score)

if __name__ == "__main__":
    main_menu()
    main()
    pygame.quit()
