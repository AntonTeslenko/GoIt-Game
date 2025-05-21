"""
Аркадна гра, створена з використанням бібліотеки Pygame.

Гравець керує гусаком, який може рухатися вгору, вниз, вправо та вліво за допомогою клавіш зі стрілками.
Завдання гравця — уникати ворогів, що з’являються праворуч і рухаються вліво, та збирати бонуси, що падають згори.
За кожен зібраний бонус гравець отримує одне очко. Якщо гусак зіштовхується з ворогом — гра завершується.

Фон плавно прокручується, створюючи ефект руху. Графіка гусака анімована — зображення змінюються кожні 200 мс.

Код також реалізує:
- генерацію ворогів та бонусів з використанням таймерів;
- колізії між гравцем і об’єктами;
- підрахунок та виведення очок;
- очищення об’єктів, що вийшли за межі екрану.

"""
import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

# Ініціалізація таймера
FPS = pygame.time.Clock()

# Розміри вікна
HEIGHT = 800
WIDTH = 1200

# Шрифт для відображення рахунку
FONT = pygame.font.SysFont('Verdana', 20)

# Кольори
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = [0, 0, 255]
COLOR_RED = (255, 0, 0)

# Створення головного вікна
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

# Завантаження та масштабування фону
bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3  # Швидкість руху фону

# Завантаження зображень гравця з папки
IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

# Налаштування зображення гравця
player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()

# Напрями руху гравця
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]

# Завантаження зображень ворога та бонусу
enemy_image = pygame.image.load('enemy.png').convert_alpha()
bonus_image = pygame.image.load('bonus.png').convert_alpha()


# Функція створення ворога
def create_enemy():
    enemy_size = enemy_image.get_size()
    enemy = pygame.transform.scale(enemy_image, enemy_size)
    enemy_y = random.randint(0, HEIGHT - enemy_size[1])
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]  # Рух вліво
    return [enemy, enemy_rect, enemy_move]


# Функція створення бонусу
def create_bonus():
    bonus_size = bonus_image.get_size()
    bonus = pygame.transform.scale(bonus_image, bonus_size)
    bonus_x = random.randint(0, WIDTH - bonus_size[0])
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_move = [0, random.randint(4, 8)]  # Рух вниз
    return [bonus, bonus_rect, bonus_move]


# Події таймера
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)  # Створення ворога кожні 1.5 сек
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)  # Створення бонусу кожні 3 сек
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)  # Зміна кадру анімації

# Списки для ворогів і бонусів
enemies = []
bonuses = []

score = 0  # Рахунок гравця
image_index = 0  # Індекс зображення для анімації

playing = True  # Основний цикл гри

while playing:
    FPS.tick(120)  # Частота кадрів

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False  # Вихід з гри
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())  # Додати ворога
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())  # Додати бонус
        if event.type == CHANGE_IMAGE:
            # Зміна зображення гравця (анімація)
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    # Рух фону для створення ефекту руху
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    # Малювання фону
    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    # Обробка натискань клавіш для руху гравця
    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    # Оновлення та малювання ворогів
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        # Перевірка зіткнення з ворогом
        if player_rect.colliderect(enemy[1]):
            playing = False  # Кінець гри

    # Оновлення та малювання бонусів
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        # Перевірка зіткнення з бонусом
        if player_rect.colliderect(bonus[1]):
            score += 1  # Збільшення рахунку
            bonuses.pop(bonuses.index(bonus))  # Видалення зібраного бонусу

    # Відображення рахунку
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    # Відображення гравця
    main_display.blit(player, player_rect)

    pygame.display.flip()  # Оновлення екрану

    # Видалення ворогів, які вийшли за межі екрану
    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    # Видалення бонусів, які вийшли за межі екрану
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
