import pygame
import sys
import random
import os
import tkinter as tk
from tkinter import messagebox

# Initializing the pygame
pygame.init()

# Frames per second
clock = pygame.time.Clock()

# Function to draw the floor
def draw_floor():
    screen.blit(floor_img, (floor_x, screen_height - 100))
    screen.blit(floor_img, (floor_x + screen_width, screen_height - 100))

# Function to create pipes with a small gap
def create_pipes():
    pipe_y = random.choice(pipe_height)
    gap_size = 200  # Reduced pipe gap
    top_pipe = pipe_img.get_rect(midbottom=(-67, pipe_y - gap_size))
    bottom_pipe = pipe_img.get_rect(midtop=(-67, pipe_y))
    return top_pipe, bottom_pipe

# Function for pipe animation
def pipe_animation():
    global game_over, score_time
    for pipe in pipes:
        if pipe.top < 0:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)
        else:
            screen.blit(pipe_img, pipe)

        pipe.centerx += 2.5  # Pipe speed for difficulty
        if pipe.left > screen_width:
            pipes.remove(pipe)

        if bird_rect.colliderect(pipe):
            game_over = True

# Function to draw the score
def draw_score(game_state):
    if game_state == "game_on":
        score_text = score_font.render(str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(screen_width // 2, 66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(screen_width // 2, 66))
        screen.blit(score_text, score_rect)

        high_score_text = score_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(screen_width // 2, screen_height - 116))
        screen.blit(high_score_text, high_score_rect)

# Function to update the score
def score_update():
    global score, score_time, high_score
    if pipes:
        for pipe in pipes:
            if screen_width // 2 - 2 < pipe.centerx < screen_width // 2 + 2 and score_time:
                score += 1
                score_time = False
            if pipe.right >= screen_width:
                score_time = True

    if score > high_score:
        high_score = score

# Function to display the start game message
def display_start_message():
    start_text = score_font.render("Press Space to Start", True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(start_text, start_rect)

# Get screen resolution and set game window
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Flappy Bird")

# Get the base directory of the script
base_dir = os.path.dirname(__file__)

# Setting background and base image
back_day_img = pygame.image.load(os.path.join(base_dir, "assests", "img_46.png")).convert()  # Day background
back_night_img = pygame.image.load(os.path.join(base_dir, "assests", "night.png")).convert()  # Night background
back_day_img = pygame.transform.scale(back_day_img, (screen_width, screen_height))
back_night_img = pygame.transform.scale(back_night_img, (screen_width, screen_height))

# Initial background
background_img = back_day_img

floor_img = pygame.image.load(os.path.join(base_dir, "assests", "img_50.png")).convert()
floor_img = pygame.transform.scale(floor_img, (screen_width, 100))
floor_x = 0

# Different stages of bird
bird_up = pygame.image.load(os.path.join(base_dir, "assests", "img_47.png")).convert_alpha()
bird_down = pygame.image.load(os.path.join(base_dir, "assests", "img_48.png")).convert_alpha()
bird_mid = pygame.image.load(os.path.join(base_dir, "assests", "img_49.png")).convert_alpha()
birds = [bird_up, bird_mid, bird_down]
bird_index = 0
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 200)
bird_img = birds[bird_index]
bird_rect = bird_img.get_rect(center=(screen_width // 4, screen_height // 2))
bird_movement = 0
gravity = 0.1  # Increased gravity for faster falling

# Loading pipe image
pipe_img = pygame.image.load(os.path.join(base_dir, "assests", "greenpipe.png")).convert_alpha()
pipe_height = [screen_height // 2, screen_height // 2.5, screen_height // 1.5, screen_height // 1.75]

# For the pipes to appear
pipes = []
create_pipe = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe, 1400)

# Displaying game over image
game_over = False
over_img = pygame.image.load(os.path.join(base_dir, "assests", "img_45.png")).convert_alpha()
over_img = pygame.transform.scale(over_img, (screen_width // 2, screen_height // 2))
over_rect = over_img.get_rect(center=(screen_width // 2, screen_height // 2))

# Setting variables and font for score
score = 0
high_score = 0
score_time = True
score_font = pygame.font.Font("freesansbold.ttf", 27)

# Add a variable for the game start
game_started = False

# Track the number of attempts
attempts = 0

# Function to show pop-up message
def show_game_over_popup(score, high_score):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Game Over", f"Score: {score}\nHigh Score: {high_score}\nNo more attempts left.")
    root.destroy()

# Game loop
running = True
while running:
    clock.tick(120)

    # For checking the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:  # Start the game when space is pressed
                    game_started = True
                if not game_over:  # Allow bird movement
                    bird_movement = 0
                    bird_movement = -5  # Increased bird's ascent speed
                if game_over:  # Restart game on game over
                    if attempts < 5:  # Check if player has more attempts left
                        game_over = False
                        pipes = []
                        bird_movement = 0
                        bird_rect = bird_img.get_rect(center=(screen_width // 4, screen_height // 2))
                        score_time = True
                        score = 0
                        attempts += 1
                    else:
                        show_game_over_popup(score, high_score)  # Show pop-up after 2 attempts
                        running = False  # End the game after two attempts

        if event.type == bird_flap:
            bird_index += 1
            if bird_index > 2:
                bird_index = 0
            bird_img = birds[bird_index]
            bird_rect = bird_img.get_rect(center=bird_rect.center)

        if event.type == create_pipe and game_started and not game_over:
            pipes.extend(create_pipes())

    # Background change based on score
    # Determine background based on score thresholds (5, 10, 15, ..., 50)
    if (score % 10) >= 5:  # Night mode for scores 5-9, 15-19, 25-29, etc.
        background_img = back_night_img
    else:  # Day mode for scores 0-4, 10-14, 20-24, etc.
        background_img = back_day_img

    # Draw background
    screen.blit(background_img, (0, 0))

    if not game_started:  # Display the start message
        display_start_message()
    elif not game_over:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = pygame.transform.rotozoom(bird_img, bird_movement * -6, 1)

        if bird_rect.top < 5 or bird_rect.bottom >= screen_height - 100:
            game_over = True

        screen.blit(rotated_bird, bird_rect)
        pipe_animation()
        score_update()
        draw_score("game_on")
    elif game_over:
        screen.blit(over_img, over_rect)
        draw_score("game_over")

    floor_x -= 1
    if floor_x < -screen_width:
        floor_x = 0

    draw_floor()

    pygame.display.update()

pygame.quit()
sys.exit()
