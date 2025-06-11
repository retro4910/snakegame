import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game with Power-Ups and Levels")

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
dark_blue = (0, 0, 139)
dark_purple = (48, 25, 52)

def get_background(level):
    if level == 1:
        return black
    elif level == 2:
        return dark_blue
    elif level == 3:
        return dark_purple
    return black

# Snake settings
snake_block = 10
snake_speed = 15
initial_speed = 15
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Sounds
hit_sound = pygame.mixer.Sound("hit.wav")
eat_sound = pygame.mixer.Sound("eat.wav")
level_up_sound = pygame.mixer.Sound("level_up.wav")

# Power-up duration in seconds
POWERUP_DURATION = 5

# Show score and lives
def show_score(score, lives, level):
    value = font.render(f"Score: {score}  Lives: {lives}  Level: {level}", True, white)
    win.blit(value, [10, 10])

# Draw snake
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], snake_block, snake_block])

# Message display
def message(msg, color):
    text = font.render(msg, True, color)
    win.blit(text, [width / 4, height / 3])

def flash_level_up(level):
    win.fill(white)
    msg = font.render(f"Level {level}!", True, red)
    win.blit(msg, [width // 3, height // 3])
    pygame.display.update()
    time.sleep(1)

def game_loop():
    global snake_speed
    game_over = False
    score = 0
    lives = 3
    level = 1
    snake_speed = initial_speed
    x = width / 2
    y = height / 2
    x_change = 0
    y_change = 0
    snake_list = []
    length = 1
    invincible = False
    invincible_timer = 0
    double_points = False
    double_points_timer = 0

    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    # Power-up
    powerup_active = False
    powerup_type = None
    powerup_x = powerup_y = 0

    # Obstacles
    obstacle_count = 5
    obstacles = [[
        round(random.randrange(0, width - snake_block) / 10.0) * 10.0,
        round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    ] for _ in range(obstacle_count)]

    while not game_over:
        if invincible and time.time() > invincible_timer:
            invincible = False
        if double_points and time.time() > double_points_timer:
            double_points = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = snake_block
                    x_change = 0

        x += x_change
        y += y_change

        if x >= width or x < 0 or y >= height or y < 0:
            if not invincible:
                hit_sound.play()
                lives -= 1
                if lives == 0:
                    game_over = True
                else:
                    x, y = width / 2, height / 2
                    x_change = y_change = 0
                    snake_list = []
                    length = 1

        win.fill(get_background(level))

        # Food
        pygame.draw.rect(win, red, [food_x, food_y, snake_block, snake_block])

        # Obstacles
        for obs in obstacles:
            pygame.draw.rect(win, white, [obs[0], obs[1], snake_block, snake_block])

        # Power-up
        if not powerup_active and random.randint(1, 100) == 1:
            powerup_type = random.choice(["speed", "invincible", "double"])
            powerup_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            powerup_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            powerup_active = True
        if powerup_active:
            color = (0, 255, 255) if powerup_type == "speed" else (255, 255, 0) if powerup_type == "invincible" else (255, 105, 180)
            pygame.draw.rect(win, color, [powerup_x, powerup_y, snake_block, snake_block])

        # Update snake
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        # Self collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                if not invincible:
                    hit_sound.play()
                    lives -= 1
                    if lives == 0:
                        game_over = True

        # Obstacle collision
        for obs in obstacles:
            if x == obs[0] and y == obs[1]:
                if not invincible:
                    hit_sound.play()
                    lives -= 1
                    if lives == 0:
                        game_over = True

        draw_snake(snake_list)
        show_score(score, lives, level)

        pygame.display.update()

        # Eat food
        if x == food_x and y == food_y:
            eat_sound.play()
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length += 1
            score += 20 if double_points else 10

            if score % 50 == 0:
                level += 1
                snake_speed += 2
                flash_level_up(level)
                level_up_sound.play()

        # Power-up collision
        if powerup_active and x == powerup_x and y == powerup_y:
            if powerup_type == "speed":
                snake_speed += 5
            elif powerup_type == "invincible":
                invincible = True
                invincible_timer = time.time() + POWERUP_DURATION
            elif powerup_type == "double":
                double_points = True
                double_points_timer = time.time() + POWERUP_DURATION
            powerup_active = False

        clock.tick(snake_speed)

    message("Game Over! Press Q to Quit", red)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

# Run the game
game_loop()
