import pygame
import time
import random
import json
import os

pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_green = (0, 100, 0)

# Display settings
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 20  # Increased block size
snake_speed = 15

# Improved fonts
font_style = pygame.font.SysFont('arial', 50)
score_font = pygame.font.SysFont('arial', 35)

# Load high score
def load_high_score():
    try:
        with open('high_score.json', 'r') as f:
            return json.load(f)['high_score']
    except:
        return 0

def save_high_score(score):
    with open('high_score.json', 'w') as f:
        json.dump({'high_score': score}, f)

def draw_snake_segment(surface, x, y, block_size, is_head=False, direction=(1,0)):
    """Draw a single snake segment with rounded edges"""
    if is_head:
        # Draw snake head
        center = (int(x + block_size/2), int(y + block_size/2))
        pygame.draw.circle(surface, green, center, int(block_size/2))
        
        # Add eyes
        eye_color = (255, 255, 255)  # White eyes
        pupil_color = (0, 0, 0)      # Black pupils
        
        # Adjust eye positions based on direction
        if direction == (1, 0):  # Right
            left_eye = (x + block_size*3/4, y + block_size/4)
            right_eye = (x + block_size*3/4, y + block_size*3/4)
        elif direction == (-1, 0):  # Left
            left_eye = (x + block_size/4, y + block_size/4)
            right_eye = (x + block_size/4, y + block_size*3/4)
        elif direction == (0, -1):  # Up
            left_eye = (x + block_size/4, y + block_size/4)
            right_eye = (x + block_size*3/4, y + block_size/4)
        else:  # Down
            left_eye = (x + block_size/4, y + block_size*3/4)
            right_eye = (x + block_size*3/4, y + block_size*3/4)
            
        # Draw eyes
        pygame.draw.circle(surface, eye_color, (int(left_eye[0]), int(left_eye[1])), int(block_size/8))
        pygame.draw.circle(surface, eye_color, (int(right_eye[0]), int(right_eye[1])), int(block_size/8))
        # Draw pupils
        pygame.draw.circle(surface, pupil_color, (int(left_eye[0]), int(left_eye[1])), int(block_size/16))
        pygame.draw.circle(surface, pupil_color, (int(right_eye[0]), int(right_eye[1])), int(block_size/16))
    else:
        # Draw body segment
        center = (int(x + block_size/2), int(y + block_size/2))
        pygame.draw.circle(surface, green, center, int(block_size/2))
        # Add scales effect
        scale_color = (0, 200, 0)  # Slightly darker green
        pygame.draw.arc(surface, scale_color, (x, y, block_size, block_size), 0, 3.14, 2)

def our_snake(snake_block, snake_list):
    # Calculate direction of snake head
    if len(snake_list) > 1:
        head = snake_list[-1]
        neck = snake_list[-2]
        direction = (
            (head[0] - neck[0])/snake_block,
            (head[1] - neck[1])/snake_block
        )
    else:
        direction = (1, 0)  # Default direction

    # Draw body segments
    for i, segment in enumerate(snake_list[:-1]):
        draw_snake_segment(dis, segment[0], segment[1], snake_block, False)
    
    # Draw head
    if snake_list:
        head = snake_list[-1]
        draw_snake_segment(dis, head[0], head[1], snake_block, True, direction)

def show_score(score, high_score):
    score_text = score_font.render(f"Score: {score}", True, white)
    high_score_text = score_font.render(f"High Score: {high_score}", True, yellow)
    dis.blit(score_text, [10, 10])
    dis.blit(high_score_text, [10, 50])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def draw_food(foodx, foody):
    # Draw apple-like food
    pygame.draw.circle(dis, red, (int(foodx + snake_block/2), int(foody + snake_block/2)), int(snake_block/2))
    pygame.draw.rect(dis, dark_green, [foodx + snake_block/3, foody - snake_block/4, snake_block/4, snake_block/4])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    
    high_score = load_high_score()
    current_score = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:
        while game_close:
            dis.fill((0, 0, 50))  # Dark blue background
            message("Game Over! Q-Quit or C-Play Again", red)
            show_score(current_score, high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        
        # Create gradient background
        dis.fill((0, 0, 50))  # Dark blue background
        
        # Draw grid lines
        for x in range(0, dis_width, snake_block):
            pygame.draw.line(dis, (20, 20, 70), (x, 0), (x, dis_height))
        for y in range(0, dis_height, snake_block):
            pygame.draw.line(dis, (20, 20, 70), (0, y), (dis_width, y))

        draw_food(foodx, foody)
        
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(current_score, high_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1
            current_score += 10
            
            if current_score > high_score:
                high_score = current_score
                save_high_score(high_score)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()