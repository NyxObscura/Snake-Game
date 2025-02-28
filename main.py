import pygame
import time
import random

# Inisialisasi pygame
pygame.init()

# Warna
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_gray = (30, 30, 30)  # Warna background
light_blue = (100, 200, 255)  # Warna outline ular

# Ukuran layar
width = 600
height = 400

# Ukuran blok ular
snake_block = 10
snake_speed = 15  # Kecepatan ular

# Font
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("bahnschrift", 35)

# Buat layar game
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game by NyxObscura")

clock = pygame.time.Clock()

def message(msg, color, x, y, shadow=False):
    """ Menampilkan pesan di layar dengan opsi bayangan """
    if shadow:
        shadow_msg = font_style.render(msg, True, black)
        dis.blit(shadow_msg, [x + 2, y + 2])
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [x, y])

def display_score(score):
    """ Menampilkan skor di layar dengan bayangan """
    text = f"Skor: {score}"
    shadow = score_font.render(text, True, black)
    value = score_font.render(text, True, white)
    dis.blit(shadow, [12, 12])
    dis.blit(value, [10, 10])

def gameLoop():
    game_over = False
    game_close = False

    # Posisi awal ular
    x = width / 2
    y = height / 2

    # Pergerakan
    x_change = 0
    y_change = 0

    # Ular
    snake_body = []
    length_of_snake = 1

    # Posisi makanan
    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            dis.fill(dark_gray)
            message("Game Over! Tekan Q untuk keluar atau C untuk main lagi.", red, width / 10, height / 3, shadow=True)
            display_score(length_of_snake - 1)
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

        # Cek tabrakan dengan dinding
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True

        x += x_change
        y += y_change
        dis.fill(dark_gray)  # Background lebih soft
        pygame.draw.circle(dis, red, (int(food_x + snake_block / 2), int(food_y + snake_block / 2)), snake_block // 2)  # Makanan berbentuk lingkaran

        # Update badan ular
        snake_head = [x, y]
        snake_body.append(snake_head)

        if len(snake_body) > length_of_snake:
            del snake_body[0]

        # Cek tabrakan dengan badan sendiri
        for block in snake_body[:-1]:
            if block == snake_head:
                game_close = True

        # Gambar ular dengan outline
        for block in snake_body:
            pygame.draw.rect(dis, light_blue, [block[0] - 1, block[1] - 1, snake_block + 2, snake_block + 2])  # Outline
            pygame.draw.rect(dis, blue, [block[0], block[1], snake_block, snake_block])  # Badan

        display_score(length_of_snake - 1)
        pygame.display.update()

        # Jika ular makan makanan
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1  # Tambah panjang ular

        clock.tick(snake_speed)  # Kontrol kecepatan ular

    pygame.quit()
    quit()

gameLoop()