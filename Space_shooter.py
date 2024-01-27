import pygame
import random
import time

pygame.init()
pygame.mixer.init()
bakcground_music = pygame.mixer.Sound("battle_music.ogg")
bakcground_music.set_volume(0.2)
bakcground_music.play(loops=-1)


window_width = 1280
window_height = 720
windowGame = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space Shooter')
icon_image = pygame.image.load("icon.png")
pygame.display.set_icon(icon_image)

clock = pygame.time.Clock()
FPS = 60

black = (0, 0, 0)
white = (255, 255, 255)
gray = (90, 100, 110)
light_gray = (233, 236, 239)

light_blue = (142, 202, 230)
blue_green = (33, 158, 188)
dark_blue = (2, 48, 71)
yellow = (255, 183, 3)
orange = (251, 133, 0)

score = 0
font = pygame.font.SysFont("Arial", 25)
font2 = pygame.font.Font("UI/FreeSansBold.ttf", 80)
menu_font = pygame.font.Font("UI/FreeSansBold.ttf", 50)
title_font = pygame.font.Font("UI/FreeSans.ttf", 50)
score_x = 10
score_y = 10

# Define background
background_image = pygame.image.load("blue.png")
background_y = 0
num_repetitions_x = window_width // background_image.get_width() + 1
num_repetitions_y = window_height // background_image.get_height() + 1
background_surface = pygame.Surface((window_width, window_height * 2))

for x in range(num_repetitions_x):
    for y in range(num_repetitions_y * 2):
        background_surface.blit(
            background_image, (x * background_image.get_width(), y * background_image.get_height()))

 # Level Variables

wave_counter = 1
time_between_waves = 2
last_wave_time = time.time()
wave_finished = False

numerals_pngs = []
numeral_x = pygame.transform.scale(
    pygame.image.load("UI/numeralX.png"), (24, 24))
for i in range(10):
    frame = pygame.image.load(f"UI/numeral{i}.png")
    frame = pygame.transform.scale(frame, (24, 24))
    numerals_pngs.append(frame)

power_up_dropped = []
power_up_x = []
power_up_y = []
bolt_png = pygame.image.load("Power-ups/bolt_gold.png")
gold_start_png = pygame.image.load("Power-ups/star_gold.png")
pill_red_png = pygame.image.load("Power-ups/pill_red.png")
shield_silver_png = pygame.image.load("Power-ups/shield_silver.png")
power_ups_list = [bolt_png, gold_start_png, pill_red_png, shield_silver_png]
power_up_sound = pygame.mixer.Sound("powerUp.mp3")

shield_duration = 2
shield_life = 3
shield_time = 0
shield_active = False
shield_frame_index = 0
shield_frame_1 = pygame.image.load("Effects/shield1.png")
shield_frame_2 = pygame.image.load("Effects/shield2.png")
shield_frame_3 = pygame.image.load("Effects/shield3.png")
shield_sound_up = pygame.mixer.Sound("sfx_shieldUp.ogg")
shield_sound_down = pygame.mixer.Sound("sfx_shieldDown.ogg")
shield_frames = [shield_frame_1, shield_frame_2, shield_frame_3]

# UI
space_ship = pygame.image.load("player.png")
player_life_icon = pygame.image.load("UI/playerLife1_red.png")
ship_position_x = (window_width - space_ship.get_rect().width) / 2
ship_position_y = window_height - space_ship.get_rect().height - 20
ship_movement = 0
isDied = True
life = 3
num_lasers = 1
red_laser = pygame.image.load("laserRed.png")
laser_speed = 10
lasers = []
lasers_x = []
lasers_y = []
laser_sound = pygame.mixer.Sound("laser_sound.ogg")

enemy = pygame.image.load("enemyShip.png")
enemies = []
enemy_x = []
enemy_y = []
enemy_movement_x = []
enemy_movement_y = []

enemy_lasers = []
enemy_lasers_x = []
enemy_lasers_y = []
enemy_y_start = []
enemy_laser_speed = 8
enemy_last_time_shoot = []
enemy_laser = pygame.image.load("laserGreen.png")
enemies_destroyed = 0
num_enemies_per_wave = 2
enemy_shoot_cooldown = 3

boss = pygame.image.load("boss.png")
boss_hp = 100
boss_max_hp = 100
boss_hit_count = 0
boss_x = window_width / 2 - boss.get_width() / 2
boss_y = -boss.get_rect().height - 100
boss_movement_x = 2
boss_movement_y = 2
boss_shoot_cooldown = 4
boss_laser_cooldown = 0.15
boss_last_time_laser = time.time()
boss_last_time_shoot = time.time()
boss_lasers = []
boss_lasers_x = []
boss_lasers_y = []
boss_laser_speed = 8

explosion_frames = []
for i in range(64):
    frame = pygame.image.load(f"explosion/explosion{i + 1}.png")
    frame = pygame.transform.scale(frame, (320, 320))
    explosion_frames.append(frame)


explosion_effect = []
explosiones_index = []
explosion_x = []
explosion_y = []
explosion_sound = pygame.mixer.Sound("explosion_sound.flac")

destroyed_time = 0


def display_score(score):
    score_string = str(score).zfill(6)
    x_offset = window_width - 30

    for char in reversed(score_string):
        image = numerals_pngs[int(char)]
        x_offset -= image.get_width()
        windowGame.blit(image, (x_offset, 30))


def display_life(life):
    life_show = [player_life_icon, numeral_x, numerals_pngs[life]]
    x_offset = 30
    for i in range(3):
        image = life_show[i]
        windowGame.blit(image, (x_offset, 30))
        x_offset += image.get_width() + 20


def display_lasers(num_lasers):
    laser_offset = 24
    laser_sound.play()
    if num_lasers % 2 == 0:
        start_offset = -laser_offset * (num_lasers // 2) + laser_offset / 2
    else:
        start_offset = -laser_offset * (num_lasers // 2)

    for i in range(num_lasers):
        laser_x = ship_position_x + space_ship.get_rect().width / 2 - \
            red_laser.get_rect().width / 2 + start_offset + i * laser_offset
        laser_y = ship_position_y - red_laser.get_rect().height
        lasers_x.append(laser_x)
        lasers_y.append(laser_y + abs(i - (num_lasers - 1) / 2) * 16)
        lasers.append(red_laser)


def draw_boss_hp_bar():
    bar_width = 300
    bar_height = 20
    hp_ratio = boss_hp / boss_max_hp
    remaining_hp_width = int(bar_width * hp_ratio)
    pygame.draw.rect(windowGame, (0, 0, 0), [
                     window_width // 2 - bar_width // 2, 50, bar_width, bar_height])
    pygame.draw.rect(windowGame, (255, 0, 0), [
                     window_width // 2 - bar_width // 2, 50, remaining_hp_width, bar_height])


def player_hit():
    global shield_active, shield_time, shield_life, shield_frame_index, life, ship_position_x, ship_position_y, isDied, destroyed_time
    if shield_active and time.time() - shield_time < 10:
        shield_life -= 1
        shield_frame_index -= 1
        if shield_life == 0:
            shield_active = False
            shield_sound_down.play()
    else:
        explosion_effect.append(explosion_frames)
        explosiones_index.append(0)
        explosion_x.append(player_collision.x +
                           space_ship.get_rect().width / 2)
        explosion_y.append(player_collision.y -
                           space_ship.get_rect().height / 2 - 10)
        explosion_sound.play()
        life -= 1
        ship_position_x = (window_width - space_ship.get_rect().width) / 2
        ship_position_y = window_height - space_ship.get_rect().height - 20
        if life == 0:
            isDied = True
            destroyed_time = time.time()


def update_high_scores(score):
    scores = read_high_scores()
    scores.append(score)
    scores.sort(reverse=True)
    if len(scores) > 10:
        scores = scores[:10]
    with open("shooterscore.txt", "w") as file:
        for s in scores:
            file.write(f"{s}\n")


def read_high_scores():
    try:
        with open("shooterscore.txt", "r") as file:
            scores = [int(line.strip()) for line in file]
            return scores
    except FileNotFoundError:
        return []


def display_high_scores(scores):
    window_img = pygame.transform.scale(
        pygame.image.load("Main_Menu/Window.png"), (400, 600))
    windowGame.blit(window_img, ((window_width - window_img.get_width()) //
                    2, (window_height - window_img.get_height()) // 2))

    total_scores_height = len(scores) * 50

    y_offset = (window_height - total_scores_height) // 2

    score_image = pygame.transform.scale(
        pygame.image.load("Main_Menu/Score.png"), (200, 40))
    score_text_x = ((window_width - window_img.get_width()) // 2) + \
        ((window_img.get_width() - score_image.get_width()) // 2)

    windowGame.blit(score_image, (score_text_x,
                    (window_height - window_img.get_height() + 28) // 2))

    for score in scores:
        score_string = str(score).zfill(6)
        x_offset = (window_width - len(score_string) * 30) // 2
        for char in score_string:
            image = numerals_pngs[int(char)]
            windowGame.blit(image, (x_offset, y_offset))
            x_offset += 30
        y_offset += 50


menu_running = True


def main_menu():
    global isDied, running, menu_running, background_y
    menu_running = True
    display_scores = False
    header_image = pygame.image.load("Main_Menu/Header.png")
    start_button_image = pygame.image.load("Main_Menu/Start_BTN.png")
    exit_button_image = pygame.image.load("Main_Menu/Exit_BTN.png")
    info_button_image = pygame.image.load("Main_Menu/Info_BTN.png")
    settings_button_image = pygame.image.load("Main_Menu/Settings_BTN.png")
    rating_button_image = pygame.image.load("Main_Menu/Rating_BTN.png")

    header_image = pygame.transform.scale(
        header_image, (window_width // 2, 180))
    info_button_image = pygame.transform.scale(info_button_image, (120, 120))
    settings_button_image = pygame.transform.scale(
        settings_button_image, (120, 120))
    rating_button_image = pygame.transform.scale(
        rating_button_image, (120, 120))

    header_rect = header_image.get_rect(center=(window_width // 2, 200))
    start_button_rect = start_button_image.get_rect(
        center=(window_width // 2, 400))
    exit_button_rect = exit_button_image.get_rect(
        center=(window_width // 2, 540))
    info_button_rect = info_button_image.get_rect(
        topright=(window_width - 20, 20))
    settings_button_rect = settings_button_image.get_rect(
        topright=(window_width - 20, 150))
    rating_button_rect = rating_button_image.get_rect(
        topright=(window_width - 20, 280))

    while menu_running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button_rect.collidepoint(mouse_pos):
                        menu_running = False
                        isDied = False
                    elif exit_button_rect.collidepoint(mouse_pos):
                        menu_running = False
                        running = False

                    elif info_button_rect.collidepoint(mouse_pos):
                        print("Info button clicked")

                    elif settings_button_rect.collidepoint(mouse_pos):
                        settings()

                    elif rating_button_rect.collidepoint(mouse_pos):
                        display_scores = not display_scores

        background_y -= 4

        if background_y <= -background_image.get_height():
            background_y = 0

        windowGame.blit(background_surface, (0, background_y))
        windowGame.blit(header_image, header_rect)
        windowGame.blit(start_button_image, start_button_rect)
        windowGame.blit(exit_button_image, exit_button_rect)
        windowGame.blit(info_button_image, info_button_rect)
        windowGame.blit(settings_button_image, settings_button_rect)
        windowGame.blit(rating_button_image, rating_button_rect)

        if display_scores:
            display_high_scores(read_high_scores())

        pygame.display.update()


def settings():
    global menu_running, running, background_y

    music_on = bakcground_music.get_volume() > 0
    sound_effects_on = laser_sound.get_volume() > 0

    header_image = pygame.image.load("Main_Menu/Setting/Header.png")
    music_button_image = pygame.image.load("Main_Menu/Setting/Music_BTN.png")
    sound_button_image = pygame.image.load("Main_Menu/Setting/Sound_BTN.png")
    back_button_image = pygame.image.load("Main_Menu/Setting/Backward_BTN.png")

    music_on_button_image = pygame.image.load(
        "Main_Menu/BTNs_Active/Music_BTN.png")
    sound_button_on_image = pygame.image.load(
        "Main_Menu/BTNs_Active/Sound_BTN.png")

    music_text_image = pygame.image.load("Main_Menu/Setting/Music.png")
    sound_text_image = pygame.image.load("Main_Menu/Setting/Sound.png")

    image_width = 100
    image_height = 100

    header_image = pygame.transform.scale(header_image, (400, 80))
    back_button_image = pygame.transform.scale(
        back_button_image, (image_width, image_height))
    music_button_image = pygame.transform.scale(
        music_button_image, (image_width, image_height))
    sound_button_image = pygame.transform.scale(
        sound_button_image, (image_width, image_height))
    music_on_button_image = pygame.transform.scale(
        music_on_button_image, (image_width, image_height))
    sound_button_on_image = pygame.transform.scale(
        sound_button_on_image, (image_width, image_height))

    header_image_rect = header_image.get_rect(center=(window_width // 2, 150))
    music_text_rect = music_text_image.get_rect(
        midleft=(window_width // 2 - 70, window_height // 2 - 80))
    sound_text_rect = sound_text_image.get_rect(
        midleft=(window_width // 2 - 70, window_height // 2 + 30))
    music_button_rect = music_button_image.get_rect(
        midright=(window_width // 2 - 90, window_height // 2 - 80))
    sound_button_rect = sound_button_image.get_rect(
        midright=(window_width // 2 - 90, window_height // 2 + 30))
    back_button_rect = back_button_image.get_rect(topleft=(20, 20))
    settings_running = True
    while settings_running:
        clock.tick(FPS)
        if music_on:
            music_btn = music_on_button_image
        else:
            music_btn = music_button_image
        if sound_effects_on:
            sound_btn = sound_button_on_image
        else:
            sound_btn = sound_button_image
        background_y -= 4
        if background_y <= -background_image.get_height():
            background_y = 0

        windowGame.blit(background_surface, (0, background_y))
        windowGame.blit(header_image, header_image_rect)
        windowGame.blit(music_btn, music_button_rect)
        windowGame.blit(sound_btn, sound_button_rect)
        windowGame.blit(back_button_image, back_button_rect)
        windowGame.blit(music_text_image, music_text_rect)
        windowGame.blit(sound_text_image, sound_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                menu_running = False
                settings_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if music_button_rect.collidepoint(mouse_pos):
                        if music_on:
                            bakcground_music.set_volume(0)
                            music_on = False
                        else:
                            bakcground_music.set_volume(0.2)
                            music_on = True
                    elif sound_button_rect.collidepoint(mouse_pos):
                        if sound_effects_on:
                            laser_sound.set_volume(0)
                            explosion_sound.set_volume(0)
                            sound_effects_on = False
                        else:
                            laser_sound.set_volume(1)
                            explosion_sound.set_volume(1)
                            sound_effects_on = True
                    elif back_button_rect.collidepoint(mouse_pos):
                        settings_running = False
        pygame.display.update()


def create_enemies():
    global enemies, enemy_x, enemy_y, enemy_movement_x, enemy_movement_y
    for _ in range(num_enemies_per_wave):
        enemy_x_pos = random.randint(
            enemy.get_rect().width, window_width - enemy.get_rect().width)
        enemy_y_pos = random.randint(-window_height //
                                     2, -enemy.get_rect().height)

        enemies.append(enemy)
        enemy_x.append(enemy_x_pos)
        enemy_y.append(enemy_y_pos)
        enemy_movement_x.append(2)
        enemy_movement_y.append(2)
        enemy_y_start.append(enemy_y_pos)
        enemy_last_time_shoot.append(enemy_shoot_cooldown)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not isDied:
            if event.key == pygame.K_RIGHT:
                ship_movement += 4
            if event.key == pygame.K_LEFT:
                ship_movement -= 4
            if event.key == pygame.K_SPACE:
                display_lasers(num_lasers)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                space_ship = pygame.image.load("player.png")
                ship_movement = 0

    ship_position_x += ship_movement
    if ship_position_x <= 0:
        ship_position_x = 0
    if ship_position_x >= window_width - space_ship.get_rect().width:
        ship_position_x = window_width - space_ship.get_rect().width

    remove_lasers = set()
    remove_enemies = set()

    for i in range(len(lasers)):
        lasers_y[i] -= laser_speed
        laser_collision = lasers[i].get_rect(
            topleft=(lasers_x[i], lasers_y[i]))
        boss_collision = boss.get_rect(topleft=(boss_x, boss_y))

        if boss_collision.colliderect(laser_collision):
            remove_lasers.add(i)
            boss_hit_count += 3
            boss_hp -= 1
            if boss_hp <= 0:
                destroyed_time = time.time()
                explosion_effect.append(explosion_frames)
                explosiones_index.append(0)
                explosion_x.append(boss_collision.x +
                                   boss.get_rect().width / 2)
                explosion_y.append(boss_collision.y -
                                   boss.get_rect().height / 2 - 10)
                explosion_sound.play()
                boss_x = window_width / 2 - boss.get_width() / 2
                boss_y = -boss.get_rect().height - 20
        if lasers_y[i] < -lasers[i].get_rect().height:
            remove_lasers.add(i)

        for j in range(len(enemies)):
            enemy_collision = enemies[j].get_rect(
                topleft=(enemy_x[j], enemy_y[j]))
            if enemy_collision.colliderect(laser_collision):
                score += 1
                remove_lasers.add(i)
                explosion_effect.append(explosion_frames)
                explosiones_index.append(0)
                explosion_x.append(enemy_collision.x +
                                   enemies[j].get_rect().width / 2)
                explosion_y.append(enemy_collision.y -
                                   enemies[j].get_rect().height / 2 - 10)
                explosion_sound.play()
                remove_enemies.add(j)
                enemies_destroyed += 1
                if random.randint(1, 100) < 50:
                    power_up_x.append(enemy_x[j] + enemy.get_rect().width / 2)
                    power_up_y.append(enemy_y[j] + enemy.get_rect().height)
                    power_up_dropped.append(
                        power_ups_list[random.randint(0, 3)])

    remove_power_up = []
    for i in range(len(power_up_dropped)):
        power_up_y[i] += 2
        drop_collision = power_up_dropped[i].get_rect(
            topleft=(power_up_x[i], power_up_y[i]))
        player_collision = space_ship.get_rect(
            topleft=(ship_position_x, ship_position_y))

        if power_up_y[i] > window_height:
            remove_power_up.append(i)
        if drop_collision.colliderect(player_collision) and not isDied:
            remove_power_up.append(i)
            if power_up_dropped[i] == gold_start_png:
                score += 100
                power_up_sound.play()
            elif power_up_dropped[i] == bolt_png:
                score += 50
                power_up_sound.play()
            elif power_up_dropped[i] == shield_silver_png:
                score += 30
                shield_active = True
                shield_sound_up.play()
                shield_duration = 10
                shield_life = 3
                shield_time = time.time()
            elif power_up_dropped[i] == pill_red_png:
                score += 15
                if num_lasers < 5:
                    num_lasers += 1
                power_up_sound.play()

    for index in reversed(remove_power_up):
        power_up_dropped.pop(index)
        power_up_y.pop(index)
        power_up_x.pop(index)

    for index in reversed(list(remove_enemies)):
        enemies.pop(index)
        enemy_x.pop(index)
        enemy_y.pop(index)
        enemy_movement_x.pop(index)
        enemy_movement_y.pop(index)
        enemy_y_start.pop(index)

    for index in reversed(list(remove_lasers)):
        lasers.pop(index)
        lasers_x.pop(index)
        lasers_y.pop(index)

    remove_explosiones = []
    for i in range(len(explosion_effect)):
        explosiones_index[i] += 1
        if explosiones_index[i] >= len(explosion_frames):
            remove_explosiones.append(i)

    for index in reversed(remove_explosiones):
        explosion_effect.pop(index)
        explosiones_index.pop(index)
        explosion_x.pop(index)
        explosion_y.pop(index)
    if wave_finished:
        if len(enemies) == 0 and time.time() - last_wave_time >= time_between_waves:
            num_enemies_per_wave += 1
            wave_finished = False
            wave_counter = wave_counter + 1
            enemies_destroyed = 0
            create_enemies()
    if len(enemies) == 0 and wave_counter < 4 and not wave_finished:
        wave_finished = True
        last_wave_time = time.time()
    for i in range(len(enemies)):
        if enemy_y[i] < abs(enemy_y_start[i] / 2):
            enemy_y[i] += enemy_movement_y[i]
        else:
            enemy_x[i] += enemy_movement_x[i]
        if enemy_x[i] <= 0:
            enemy_movement_x[i] = 2
        if enemy_x[i] >= window_width - enemies[i].get_rect().width:
            enemy_movement_x[i] = -2

        current_time = time.time()
        if current_time - enemy_last_time_shoot[i] >= enemy_shoot_cooldown:
            if random.randint(1, 100) < 2:
                enemy_lasers_x.append(
                    enemy_x[i] + enemies[i].get_rect().width / 2 - enemy_laser.get_rect().width / 2)
                enemy_lasers_y.append(
                    enemy_y[i] + enemies[i].get_rect().height)
                enemy_lasers.append(enemy_laser)
                laser_sound.play()
                enemy_last_time_shoot[i] = current_time
    remove_enemy_lasers = []
    for i in range(len(enemy_lasers)):
        enemy_lasers_y[i] += enemy_laser_speed

        player_collision = space_ship.get_rect(
            topleft=(ship_position_x, ship_position_y))
        enemy_laser_collision = enemy_lasers[i].get_rect(
            topleft=(enemy_lasers_x[i], enemy_lasers_y[i]))

        if enemy_lasers_y[i] > window_height:
            remove_enemy_lasers.append(i)
        elif player_collision.colliderect(enemy_laser_collision) and not isDied:
            player_hit()

    for index in reversed(remove_enemy_lasers):
        enemy_lasers.pop(index)
        enemy_lasers_x.pop(index)
        enemy_lasers_y.pop(index)

    background_y -= 4
    if background_y <= -background_image.get_height():
        background_y = 0
    windowGame.blit(background_surface, (0, background_y))
    if wave_finished:
        wave_text = font2.render("Wave: " + str(wave_counter), True, white)
        wave_text_rect = wave_text.get_rect(
            center=(window_width // 2, window_height // 2))
        windowGame.blit(wave_text, wave_text_rect)

    if not isDied:
        windowGame.blit(space_ship, (ship_position_x, ship_position_y))
        if shield_active and time.time() - shield_time < 10:
            shield_duration -= 1
            if shield_frame_index < shield_life - 1 and shield_duration == 0:
                shield_frame_index += 1
                shield_duration = 2

            shield_frame = shield_frames[shield_frame_index]
            shield_frame_width = shield_frame.get_width()
            shield_frame_height = shield_frame.get_height()
            shield_frame_x = ship_position_x + \
                (space_ship.get_width() - shield_frame_width) // 2
            shield_frame_y = ship_position_y + \
                (space_ship.get_height() - shield_frame_height) // 2
            windowGame.blit(shield_frame, (shield_frame_x, shield_frame_y))

    if wave_counter == 4 and len(enemies) == 0 and time.time() - last_wave_time >= time_between_waves:
        current_time = time.time()
        if boss_hp <= 0:
            wave_text = font2.render("FINISHED!", True, white)
            wave_text_rect = wave_text.get_rect(
                center=(window_width // 2, window_height // 2))
            windowGame.blit(wave_text, wave_text_rect)
            if time.time() - destroyed_time >= 2:
                update_high_scores(score)
                main_menu()
                life = 3
                wave_counter = 1
                wave_finished = False
                enemies.clear()
                enemy_y.clear()
                enemy_x.clear()
                num_enemies_per_wave = 1
                enemies_destroyed = 0
                boss_hp = 100
        else:
            if boss_y < boss.get_rect().width + 50:
                boss_y += boss_movement_y
            else:
                boss_x += boss_movement_x
            if boss_x <= 0:
                boss_movement_x = 2
            if boss_x >= window_width - boss.get_rect().width:
                boss_movement_x = -2
            if boss_hit_count > 0:
                boss_hit_count -= 1
                boss_with_hit = pygame.Surface.copy(boss)
                boss_with_hit.fill(
                    (255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
                windowGame.blit(boss_with_hit, (boss_x, boss_y))
            else:
                windowGame.blit(boss, (boss_x, boss_y))

            draw_boss_hp_bar()

            if current_time - boss_last_time_laser >= boss_shoot_cooldown:
                if current_time - boss_last_time_shoot >= boss_laser_cooldown:
                    boss_last_time_shoot = current_time
                    if len(boss_lasers) < 6:
                        boss_lasers_x.append(
                            boss_x + boss.get_width() / 2 - enemy_laser.get_rect().width / 2)
                        boss_lasers_y.append(boss_y + boss.get_height())
                        boss_lasers.append(enemy_laser)
                        laser_sound.play()
                    else:
                        boss_last_time_laser = current_time
            remove_boss_lasers = []
            remove_boss_missiles = []
            player_collision = space_ship.get_rect(
                topleft=(ship_position_x, ship_position_y))

            for i in range(len(boss_lasers)):
                boss_lasers_y[i] += boss_laser_speed
                laser_collision = boss_lasers[i].get_rect(
                    topleft=(boss_lasers_x[i], boss_lasers_y[i]))
                if laser_collision.colliderect(player_collision) and not isDied:
                    remove_boss_lasers.append(i)
                    player_hit()
                elif boss_lasers_y[i] > window_height:
                    remove_boss_lasers.append(i)

            for index in reversed(remove_boss_lasers):
                boss_lasers.pop(index)
                boss_lasers_x.pop(index)
                boss_lasers_y.pop(index)
            for i in range(len(boss_lasers)):
                windowGame.blit(
                    boss_lasers[i], (boss_lasers_x[i], boss_lasers_y[i]))

    for i in range(len(enemies)):
        windowGame.blit(enemies[i], (enemy_x[i], enemy_y[i]))
    for i in range(len(enemy_lasers)):
        windowGame.blit(enemy_lasers[i],
                        (enemy_lasers_x[i], enemy_lasers_y[i]))
    for i in range(len(lasers)):
        windowGame.blit(lasers[i], (lasers_x[i], lasers_y[i]))
    for i in range(len(explosion_effect)):
        frame = explosion_effect[i][explosiones_index[i]]
        frame_rect = frame.get_rect(center=(explosion_x[i], explosion_y[i]))
        windowGame.blit(frame, frame_rect)

    display_score(score)
    display_life(life)

    for i in range(len(power_up_dropped)):
        windowGame.blit(power_up_dropped[i], (power_up_x[i], power_up_y[i]))

    if isDied:
        wave_text = font2.render("GAME OVER", True, white)
        wave_text_rect = wave_text.get_rect(
            center=(window_width // 2, window_height // 2))
        windowGame.blit(wave_text, wave_text_rect)
        if time.time() - destroyed_time >= 2:
            main_menu()
            life = 3
            wave_counter = 1
            wave_finished = False
            enemies.clear()
            enemy_y.clear()
            enemy_x.clear()
            num_enemies_per_wave = 1
            enemies_destroyed = 0

    pygame.display.update()
    clock.tick(60)
pygame.quit()
exit()
