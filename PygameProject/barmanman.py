import pygame
import os
import sys
import random
import datetime

cell = 100
width = 10 * cell
height = 10 * cell
pygame.init()
pygame.font.init()
size = width, height
game = 0
gl_running = True
all_days = 0
all_coins = 0
player_name = None

pygame.mixer.music.load('data/main_theme.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

table = open("data/records.txt", mode="rt").readlines()  # Загрузка таблицы рекордов
record_table_1 = []
for i, val in enumerate(table):  # Первые 3 места по дням
    if val == '\n':
        break
    if i < 3:
        record_table_1.append(val[:-1])
    else:
        break

record_table_2 = []
ok = False
for i in table:  # Первый 3 места по заработку
    if i == '\n':
        if not ok:
            ok = True
            continue
        else:
            break
    if len(record_table_2) > 3:
        break
    if ok:
        record_table_2.append(i[:-1])


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_font(name, size=20):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с шрифтом '{fullname}' не найден")
        sys.exit()
    font = pygame.font.Font(fullname, size)
    return font


def up_button(button):
    m_pos = pygame.mouse.get_pos()
    x, y = button.rect.x, button.rect.y
    width_b, height_b = button.rect.size
    if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
        button.clicked()
        return True
    return False


while gl_running:
    if game == 0:  # Игровое меню
        screen = pygame.display.set_mode(size)
        screen.fill("black")
        pygame.display.set_caption('Barmanman')
        main_font = load_font('mainfont.ttf', 25)
        bg_image = load_image("start_menu.jpg")
        bg_image = pygame.transform.scale(bg_image, [1002, 1002])
        button_im = load_image("button.png", -1)
        name_im = load_image("barmaman.png", -1)
        bettor_im = load_image("name.png")
        running = True

        all_sprites = pygame.sprite.Group()
        bg_group = pygame.sprite.Group()
        button_group = pygame.sprite.Group()
        game_player_group = pygame.sprite.Group()
        record_group = pygame.sprite.Group()


        class Barmaman(pygame.sprite.Sprite):  # Логотип
            def __init__(self, im):
                super().__init__(all_sprites)
                self.image = im
                self.rect = self.image.get_rect().move(430, 20)


        class Play(pygame.sprite.Sprite):  # Кнопка начала игры
            def __init__(self):
                super().__init__(all_sprites, button_group)
                self.image = button_im
                self.rect = self.image.get_rect().move(400, 400)
                self.tx = main_font.render('Играть', True, (255, 255, 255))

            def update(self):
                m_pos = pygame.mouse.get_pos()
                x, y = self.rect.x, self.rect.y
                width_b, height_b = self.rect.size
                if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
                    tx = main_font.render('Играть', True, (150, 150, 150))
                    screen.blit(tx, (473, 420))
                else:
                    screen.blit(self.tx, (473, 420))

            def clicked(self):
                global game
                global running
                game = 1
                running = False


        class Information(pygame.sprite.Sprite):  # Кнопка основной инфомации
            def __init__(self):
                super().__init__(all_sprites, button_group)
                self.image = button_im
                self.rect = self.image.get_rect().move(400, 480)
                self.tx = main_font.render('Игровая механика', True, (255, 255, 255))

            def update(self):
                m_pos = pygame.mouse.get_pos()
                x, y = self.rect.x, self.rect.y
                width_b, height_b = self.rect.size
                if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
                    tx = main_font.render('Игровая механика', True, (150, 150, 150))
                    screen.blit(tx, (410, 500))
                else:
                    screen.blit(self.tx, (410, 500))

            def clicked(self):
                global game
                global running
                global gl_running
                gl_running = True
                game = 2
                running = False


        class Close(pygame.sprite.Sprite):  # Кнопка закрытия игры
            def __init__(self):
                super().__init__(all_sprites, button_group)
                self.image = button_im
                self.rect = self.image.get_rect().move(400, 560)
                self.tx = main_font.render('Закрыть', True, (255, 255, 255))

            def update(self):
                m_pos = pygame.mouse.get_pos()
                x, y = self.rect.x, self.rect.y
                width_b, height_b = self.rect.size
                if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
                    tx = main_font.render('Закрыть', True, (150, 150, 150))
                    screen.blit(tx, (473, 580))
                else:
                    screen.blit(self.tx, (473, 580))

            def clicked(self):
                global game
                global running
                global gl_running
                gl_running = False
                game = 0
                running = False


        class Record(pygame.sprite.Sprite):  # Отображение рекордов
            def __init__(self, table1, table2):
                super().__init__(all_sprites, record_group)
                self.image = pygame.Surface([200, 100], pygame.SRCALPHA)
                self.rect = self.image.get_rect().move(700, 700)
                self.table_1 = [' '.join(j) for j in table1]
                self.table_2 = [' '.join(j) for j in table2]

            def update(self):
                name_day_coins = main_font.render(
                    'Имя      День Заработано Имя      День Заработано',
                    True, (255, 255, 255))
                screen.blit(name_day_coins, (200, 780))
                for j, text in enumerate(self.table_1):
                    tx = main_font.render(text, True, (255, 255, 255))
                    screen.blit(tx, (200, 800 + j * 20))
                for j, text in enumerate(self.table_2):
                    tx = main_font.render(text, True, (255, 255, 255))
                    screen.blit(tx, (550, 800 + j * 20))


        class Bettor(pygame.sprite.Sprite):  # Поле ввода имени
            def __init__(self, im, font):
                super().__init__(all_sprites)
                self.image = im
                self.rect = self.image.get_rect().move(330, 700)
                self.font = main_font
                self.tx = '|'
                self.print = False

            def clicked(self):
                self.print = True

            def update(self):
                if self.print:
                    tx = self.font.render(self.tx, True, (0, 0, 0))
                    screen.blit(tx, (340, 720))

            def red_text(self, key):
                if key == -1:
                    self.tx = self.tx[:-1]
                elif len(self.tx) < 5:
                    self.tx += key


        class Bg(pygame.sprite.Sprite):  # Задний фон
            def __init__(self):
                super().__init__(all_sprites, bg_group)
                self.image = bg_image
                self.rect = self.image.get_rect().move(-2, -3)


        bg = Bg()
        play = Play()
        close = Close()
        inf = Information()
        name = Barmaman(name_im)
        bettor = Bettor(bettor_im, main_font)
        record = Record(record_table_1, record_table_2)

        while running:
            player_name = bettor.tx
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gl_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        up_button(play)
                        up_button(close)
                        up_button(inf)
                        up_button(bettor)
                if event.type == pygame.KEYDOWN:
                    if bettor.print:
                        if event.key == pygame.K_BACKSPACE:
                            bettor.red_text(-1)
                        else:
                            bettor.red_text(event.unicode)
            all_sprites.draw(screen)
            button_group.draw(screen)
            button_group.update()
            bettor.update()
            record.update()
            pygame.display.flip()
        if not gl_running:
            pygame.quit()

    elif game == 1:  # Основной игровой процесс
        def load_level(filename):
            filename = "data/" + filename
            # читаем уровень, убирая символы перевода строки
            with open(filename, 'r') as mapFile:
                level_map = [line.strip() for line in mapFile]

            # и подсчитываем максимальную длину
            max_width = max(map(len, level_map))

            # дополняем каждую строку пустыми клетками ('.')
            return list(map(lambda x: x.ljust(max_width, '.'), level_map))


        def get_place(pos, tp):  # Определение клетки и ее свободы
            x = pos[0]
            y = pos[1]
            for tiles in tiles_group:
                if x in range(tiles.rect.x, tiles.rect.x + cell) and y in range(tiles.rect.y,
                                                                                tiles.rect.y + cell):
                    if tiles.get_void() and pygame.sprite.spritecollideany(tiles, blockers_group):
                        if tp == 'rack' and coins.my_money() >= 20 or (
                                tp == 'case' and coins.my_money() >= 10):
                            blockers_group.update(player.rect.x, player.rect.y)
                            pygame.sprite.spritecollideany(tiles, blockers_group).select()
                            return x // cell, y // cell
            return False


        def place(pos, tp):  # Размещение объекта
            x = pos[0]
            y = pos[1]
            for tiles in tiles_group:
                if x in range(tiles.rect.x, tiles.rect.x + cell) and y in range(tiles.rect.y,
                                                                                tiles.rect.y + cell):
                    if tiles.get_void() and pygame.sprite.spritecollideany(tiles, blockers_group):
                        if tp == 'rack' and coins.my_money() >= 20:
                            coins.change_cap(-20)
                        elif tp == 'case' and coins.my_money() >= 10:
                            coins.change_cap(-10)
                        tiles.void = False
                        blockers_group.update(player.rect.x, player.rect.y)
                        pygame.sprite.spritecollideany(tiles, blockers_group).select()
                        return x // cell, y // cell
            return False


        def delete(pos):  # Удаление объекта
            x = pos[0]
            y = pos[1]
            for tiles in tiles_group:
                if x in range(tiles.rect.x, tiles.rect.x + cell) and y in range(tiles.rect.y,
                                                                                tiles.rect.y + cell):

                    if not tiles.get_void() and pygame.sprite.spritecollideany(tiles,
                                                                               blockers_group):
                        tiles.void = True
                        blockers_group.update(player.rect.x, player.rect.y)
                        pygame.sprite.spritecollideany(tiles, blockers_group).select()
                        block = pygame.sprite.spritecollideany(tiles, blockers_group)
                        deleted = pygame.sprite.spritecollide(block, obj_group, True)
                        deleted = pygame.sprite.spritecollide(block, drinks_group, True)
                        coins.change_cap(2)
            return False


        def sell(blocker):  # Продажа
            profit = 0
            if pygame.sprite.spritecollideany(blocker, visitors_group):
                visitor = pygame.sprite.spritecollideany(blocker, visitors_group)
                if visitor.cocktail:
                    cocktail = pygame.sprite.spritecollideany(visitor, cocktail_group)
                    gl = glass.gl
                    stage_1_c = [i[0] for i in cocktail.cocktail]
                    stage_1_g = [i[0] for i in gl]
                    if sorted(stage_1_c) == sorted(stage_1_g):
                        if stage_1_c == stage_1_g:
                            profit += 1
                        stage_2_c = sorted(cocktail.cocktail, key=lambda x: x[0])
                        stage_2_g = sorted(gl, key=lambda x: x[0])
                        for i, potion in enumerate(stage_2_c):
                            if potion[1] - 0.05 <= stage_2_g[i][1] <= potion[1] + 0.05:
                                profit += 1
                    else:
                        profit -= 1
            rack = pygame.sprite.spritecollideany(visitor, racks_group)
            rack.update(0)
            rack.relieve()
            visitor.kill()
            inside = pygame.sprite.spritecollide(cocktail, inside_group, True)
            cocktail.kill()
            coins.change_cap(profit)
            glass.gl = []
            glass.volume = 0


        num_of_people = 20
        st_num_of_people = 20

        screen = pygame.display.set_mode(size)
        screen.fill("black")
        pygame.display.set_caption('Barmanman')
        coins_font = load_font('mainfont.ttf', 25)
        inf_font = load_font('mainfont.ttf', 20)
        store_font = load_font('mainfont.ttf', 25)
        running = True
        esc = False

        tile_images = {
            'wall': load_image('wall.jpg'),
            'empty': load_image('floor.jpg'),
            'door_r': load_image('door_r.png'),
            'door_l': load_image('door_l.png')}

        visitor_image = [
            ('visitor1_front.png', 'visitor1_rear.png', 'visitor1_side_r.png',
             'visitor1_side_l.png'),
            ('visitor2_front.png', 'visitor2_rear.png', 'visitor2_side_r.png',
             'visitor2_side_l.png'),
            ('visitor3_front.png', 'visitor3_rear.png', 'visitor3_side_r.png',
             'visitor3_side_l.png'),
            ('visitor4_front.png', 'visitor4_rear.png', 'visitor4_side_r.png',
             'visitor4_side_l.png'),
            ('visitor5_front.png', 'visitor5_rear.png', 'visitor5_side_r.png',
             'visitor5_side_l.png'),
            ('visitor6_front.png', 'visitor6_rear.png', 'visitor6_side_r.png',
             'visitor6_side_l.png')]  # Изображения посетителей

        drinks_sorts = {'вишневый компот': "red", "газировка": "#5ED2B8", 'яблочный сок': "#B4F63D",
                        'кисель': "#E768AB"}  # Напитки игры

        cocktails = [[5, 5, 0, 0], [5, 0, 5, 0], [5, 0, 0, 5], [10, 0, 0, 0], [0, 5, 5, 0],
                     [0, 5, 0, 5],
                     [0, 10, 0, 0], [0, 0, 5, 5], [0, 0, 10, 0], [0, 0, 0, 10],
                     [0, 0, 0, 3.3333333333333335], [0, 0, 0, 6.666666666666667],
                     [0, 0, 3.3333333333333335, 0], [0, 0, 3.3333333333333335, 3.3333333333333335],
                     [0, 0, 3.3333333333333335, 6.666666666666667], [0, 0, 6.666666666666667, 0],
                     [0, 0, 6.666666666666667, 3.3333333333333335], [0, 3.3333333333333335, 0, 0],
                     [0, 3.3333333333333335, 0, 3.3333333333333335],
                     [0, 3.3333333333333335, 0, 6.666666666666667],
                     [0, 3.3333333333333335, 3.3333333333333335, 0],
                     [0, 3.3333333333333335, 3.3333333333333335, 3.3333333333333335],
                     [0, 3.3333333333333335, 6.666666666666667, 0], [0, 6.666666666666667, 0, 0],
                     [0, 6.666666666666667, 0, 3.3333333333333335],
                     [0, 6.666666666666667, 3.3333333333333335, 0], [3.3333333333333335, 0, 0, 0],
                     [3.3333333333333335, 0, 0, 3.3333333333333335],
                     [3.3333333333333335, 0, 0, 6.666666666666667],
                     [3.3333333333333335, 0, 3.3333333333333335, 0],
                     [3.3333333333333335, 0, 3.3333333333333335, 3.3333333333333335],
                     [3.3333333333333335, 0, 6.666666666666667, 0],
                     [3.3333333333333335, 3.3333333333333335, 0, 0],
                     [3.3333333333333335, 3.3333333333333335, 0, 3.3333333333333335],
                     [3.3333333333333335, 3.3333333333333335, 3.3333333333333335, 0],
                     [3.3333333333333335, 6.666666666666667, 0, 0], [6.666666666666667, 0, 0, 0],
                     [6.666666666666667, 0, 0, 3.3333333333333335],
                     [6.666666666666667, 0, 3.3333333333333335, 0],
                     [6.666666666666667, 3.3333333333333335, 0, 0]]  # Возможные комбинации напитков
        tile_width = tile_height = cell

        player_image = load_image('player_front.png', -1)
        player_rear = load_image('player_rear.png', -1)
        player_side_r = load_image('player_side_r.png', -1)
        player_side_l = load_image('player_side_l.png', -1)

        rack_h = load_image('rack_h.png')
        rack_v = load_image('rack_v.png')
        rack_h = pygame.transform.scale(rack_h, (100, 50))
        rack_v = pygame.transform.scale(rack_v, (50, 100))

        case = load_image('case.png')
        case = pygame.transform.scale(case, (90, 90))

        blockers = load_image("blockers.png", -1)
        blockers_s = load_image("blockers_select.png", -1)

        money = load_image("money.png", -1)

        glass_im = load_image("glass.png", -1)
        dream_im = pygame.transform.scale(glass_im, (25, 45))

        all_sprites = pygame.sprite.Group()
        tiles_group = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        blockers_group = pygame.sprite.Group()
        obj_group = pygame.sprite.Group()
        racks_group = pygame.sprite.Group()
        case_group = pygame.sprite.Group()
        drinks_group = pygame.sprite.Group()
        interface_group = pygame.sprite.Group()
        visitors_group = pygame.sprite.Group()
        cocktail_group = pygame.sprite.Group()
        inside_group = pygame.sprite.Group()
        button_group = pygame.sprite.Group()
        second_button_group = pygame.sprite.Group()


        class Blocker(pygame.sprite.Sprite):  # Выделение близжайших клеток
            def __init__(self, player_pos_x, player_pos_y, dir):
                super().__init__(blockers_group, all_sprites)
                self.image = load_image("blockers.png", -1)
                self.rect = self.image.get_rect()
                self.dir = dir
                self.selected = False
                if dir == 'up':
                    self.rect.y = player_pos_y - cell - 29
                    self.rect.x = player_pos_x - 36
                    self.image = blockers_s
                elif dir == 'down':
                    self.rect.y = player_pos_y + cell - 29
                    self.rect.x = player_pos_x - 36
                    self.image = blockers
                elif dir == 'left':
                    self.rect.x = player_pos_x - cell - 36
                    self.rect.y = player_pos_y - 29
                    self.image = blockers
                elif dir == 'right':
                    self.rect.x = player_pos_x + cell - 36
                    self.rect.y = player_pos_y - 29
                    self.image = blockers

            def update(self, player_pos_x, player_pos_y):
                if self.dir == 'up':
                    self.rect.y = player_pos_y - cell - 29
                    self.rect.x = player_pos_x - 36
                elif self.dir == 'down':
                    self.rect.y = player_pos_y + cell - 29
                    self.rect.x = player_pos_x - 36
                elif self.dir == 'left':
                    self.rect.x = player_pos_x - cell - 36
                    self.rect.y = player_pos_y - 29
                elif self.dir == 'right':
                    self.rect.x = player_pos_x + cell - 36
                    self.rect.y = player_pos_y - 29
                self.image = blockers
                self.selected = False

            def select(self):
                self.image = blockers_s
                self.selected = True


        class Rack(pygame.sprite.Sprite):  # Стойка
            def __init__(self, pos):
                pos_x = pos[0]
                pos_y = pos[1]
                super().__init__(all_sprites, racks_group, obj_group)
                pl_x, pl_y = player.rect.x // cell, player.rect.y // cell
                if pl_x == pos_x:
                    self.image = rack_h
                    if pl_y > pos_y:
                        self.rect = self.image.get_rect().move(
                            tile_width * pos_x, tile_height * pos_y + cell // 2)
                    else:
                        self.rect = self.image.get_rect().move(
                            tile_width * pos_x, tile_height * pos_y)
                if pl_y == pos_y:
                    self.image = rack_v
                    if pl_x > pos_x:
                        self.rect = self.image.get_rect().move(
                            tile_width * pos_x + cell // 2, tile_height * pos_y)
                    else:
                        self.rect = self.image.get_rect().move(
                            tile_width * pos_x, tile_height * pos_y)
                self.wall = True
                self.free = True
                self.time = 0

            def get_wall(self):
                return self.wall

            def get_info(self, font, store_font):
                viw = font.render('Стойка:', True, (255, 255, 255))
                screen.blit(viw, (40, 920))

            def get_free(self):
                return self.free

            def occupy(self):
                self.free = False

            def relieve(self):
                self.free = True

            def update(self, dt):
                if not self.free:
                    self.time = 8 * 1000000
                elif self.time > 0:
                    self.time -= dt
                elif self.time < 0:
                    self.time = 0


        class Case(pygame.sprite.Sprite):  # Хранилище ингредиентов
            def __init__(self, pos):
                pos_x = pos[0]
                pos_y = pos[1]
                super().__init__(all_sprites, case_group, obj_group)
                self.image = case
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x + 5, tile_height * pos_y + 5)
                self.wall = True
                self.completed = False
                self.drink = None
                self.lives = 2

            def get_info(self, font, font_store):
                viw = font.render('Бочка:', True, (255, 255, 255))
                screen.blit(viw, (40, 920))
                if self.completed:
                    drink = pygame.sprite.spritecollideany(self, drinks_group)
                    drink.get_inf(font)
                else:
                    viw = font.render('Пусто', True, (255, 255, 255))
                    screen.blit(viw, (120, 920))
                return self.store(font_store)

            def store(self, font):
                selected = None
                pos = pygame.mouse.get_pos()
                viw = font.render('Заказать:', True, (255, 255, 255))
                screen.blit(viw, (40, 940))
                if pos[0] in range(211, 416) and pos[1] in range(940, 965):
                    cherry_compote = font.render('Вишневый компот', True, (0, 255, 0))
                    selected = 'вишневый компот'
                else:
                    cherry_compote = font.render('Вишневый компот', True, (255, 255, 255))
                screen.blit(cherry_compote, (211, 940))
                if pos[0] in range(446, 575) and pos[1] in range(940, 965):
                    soda = font.render('Газировка', True, (0, 255, 0))
                    selected = 'газировка'
                else:
                    soda = font.render('Газировка', True, (255, 255, 255))
                screen.blit(soda, (446, 940))
                if pos[0] in range(605, 775) and pos[1] in range(940, 965):
                    apple_juice = font.render('Яблочный сок', True, (0, 255, 0))
                    selected = 'яблочный сок'
                else:
                    apple_juice = font.render('Яблочный сок', True, (255, 255, 255))
                screen.blit(apple_juice, (605, 940))
                if pos[0] in range(815, 900) and pos[1] in range(940, 965):
                    jelly = font.render('Кисель', True, (0, 255, 0))
                    selected = 'кисель'
                else:
                    jelly = font.render('Кисель', True, (255, 255, 255))
                screen.blit(jelly, (815, 940))
                return selected

            def fill(self):
                self.completed = True

            def get_wall(self):
                return self.wall

            def crushed(self):
                self.lives -= 1
                if self.lives < 0:
                    pygame.sprite.spritecollide(self, drinks_group, True)
                    pygame.sprite.spritecollideany(self, tiles_group).void = True
                    self.kill()


        class Drink(pygame.sprite.Sprite):  # Класс напитка в бочке
            def __init__(self, sort, pos_x, pos_y):
                super().__init__(drinks_group, all_sprites)
                self.image = pygame.Surface([88, 88], pygame.SRCALPHA)
                self.image.fill(drinks_sorts[sort])
                self.rect = pygame.Rect(pos_x + 6, pos_y + 6, 88, 88)
                self.sort = sort  # Его сорт
                self.fullness = 5  # Его колличество в стаканах

            def get_inf(self, font):
                name = font.render(str(self.sort), True, (255, 255, 255))
                screen.blit(name, (self.rect.x, self.rect.y - cell // 2))  # Вывод имени
                volume = font.render('количество:', True, (255, 255, 255))
                fu = font.render(str(int(self.fullness)), True,
                                 (255, 255, 255))  # Вывод заполненности
                screen.blit(volume, (self.rect.x, self.rect.y + 20 - cell // 2))
                screen.blit(fu, (self.rect.x + 120, self.rect.y + 20 - cell // 2))

            def change(self):
                v = 0.01
                if self.fullness > 0:
                    self.fullness -= v
                    self.image = pygame.transform.scale(self.image,
                                                        (88, int(self.fullness / 5 * 88)))
                    return True
                return False


        class Glass(pygame.sprite.Sprite):  # Бочка
            def __init__(self):
                super().__init__(all_sprites, interface_group)
                self.image = glass_im
                self.rect = self.image.get_rect().move(870, 850)
                self.gl = []
                self.volume = 0

            def pouring(self, case):
                if self.volume < 1:
                    v = 0.01
                    drink = pygame.sprite.spritecollideany(case, drinks_group)
                    if sum([i[1] for i in self.gl]) <= 1:
                        if drink.sort == 'вишневый компот':
                            if self.gl:
                                if self.gl[-1][0] == 'вишневый компот':
                                    self.gl[-1][1] += v
                                else:
                                    self.gl.append(['вишневый компот', 0])
                            else:
                                self.gl.append(['вишневый компот', 0])
                        if drink.sort == 'газировка':
                            if self.gl:
                                if self.gl[-1][0] == 'газировка':
                                    self.gl[-1][1] += v
                                else:
                                    self.gl.append(['газировка', 0])
                            else:
                                self.gl.append(['газировка', 0])
                        if drink.sort == 'яблочный сок':
                            if self.gl:
                                if self.gl[-1][0] == 'яблочный сок':
                                    self.gl[-1][1] += v
                                else:
                                    self.gl.append(['яблочный сок', 0])
                            else:
                                self.gl.append(['яблочный сок', 0])
                        if drink.sort == 'кисель':
                            if self.gl:
                                if self.gl[-1][0] == 'кисель':
                                    self.gl[-1][1] += v
                                else:
                                    self.gl.append(['кисель', 0])
                            else:
                                self.gl.append(['кисель', 0])
                    self.volume += v

            def update(self):
                image = []
                for potion in self.gl:
                    if potion[0] == 'вишневый компот':
                        image.append(["red", int(potion[1] * 65)])
                    elif potion[0] == 'газировка':
                        image.append(["#5ED2B8", int(potion[1] * 65)])
                    elif potion[0] == 'яблочный сок':
                        image.append(["#B4F63D", int(potion[1] * 65)])
                    elif potion[0] == 'кисель':
                        image.append(["#E768AB", int(potion[1] * 65)])
                for i, potion in enumerate(image):
                    if i == 0:
                        screen.fill(pygame.Color(potion[0]),
                                    (self.rect.x + 2, self.rect.y + 67 - potion[1], 33, potion[1]))
                        continue
                    bottom = 0
                    for j in range(i):
                        bottom += image[j][1]
                    screen.fill(pygame.Color(potion[0]),
                                (self.rect.x + 3, self.rect.y + 67 - bottom - potion[1], 33,
                                 potion[1]))

            def pour_out(self):
                v = 0.01
                if self.gl and self.gl[-1][1] <= 0:
                    self.gl[-1][1] = 0
                    del self.gl[-1]
                    self.volume -= v
                elif self.gl:
                    self.volume -= v
                    self.gl[-1][1] -= v


        class Visitor(pygame.sprite.Sprite):  # Посетитель
            def __init__(self, rack, visitor_im):
                global num_of_people
                num_of_people -= 1
                super().__init__(all_sprites, visitors_group)
                self.images = random.choice(visitor_im)
                self.image = load_image(self.images[0])
                self.rect = self.image.get_rect().move(450, 20)
                self.cocktail = None
                self.pos = None
                rack.occupy()
                self.pos = [rack.rect.x, rack.rect.y]
                if rack.image == rack_h:
                    self.h = True
                    if (self.pos[1] / cell) == int((self.pos[1] / cell)):
                        self.offset = -cell // 2
                    else:
                        self.offset = -cell // 2
                    self.pos[1] += self.offset
                else:
                    self.h = False
                    if (self.pos[0] / cell) == int((self.pos[0] / cell)):
                        self.offset = -cell // 2
                    else:
                        self.offset = -cell // 2
                    self.pos[0] += self.offset

            def update(self):
                a = (350 - self.pos[0]) / (20 - self.pos[1])
                vy = -1
                if self.pos[1] != self.rect.y:
                    vy = 15 * (self.pos[1] - self.rect.y) // abs(self.pos[1] - self.rect.y)
                    vx = a * vy
                if vy > 0:
                    self.rect.x += vx
                    self.rect.y += vy
                else:
                    self.rect.x = self.pos[0]
                    self.rect.y = self.pos[1]
                    if not self.h:
                        self.image = load_image(self.images[2])
                    if not self.cocktail:
                        self.get_demand()
                    if not pygame.sprite.spritecollide(self, racks_group, False):
                        deleted = pygame.sprite.spritecollide(self, cocktail_group, True)
                        deleted = pygame.sprite.spritecollide(self, inside_group, True)
                        self.kill()

            def get_demand(self):
                self.cocktail = random.choice(cocktails)
                Cocktail(self.cocktail, self.rect.x, self.rect.y)

            def get_info(self, inf_font, store_font):
                if self.cocktail:
                    viw = store_font.render('Ингредиенты:', True, (255, 255, 255))
                    screen.blit(viw, (40, 940))
                    for i, potion in enumerate(self.cocktail):
                        if i == 0 and potion != 0:
                            cherry_compote = store_font.render('Вишневый компот', True,
                                                               (255, 255, 255))
                            screen.blit(cherry_compote, (211, 940))
                        if i == 1 and potion != 0:
                            soda = store_font.render('Газировка', True, (255, 255, 255))
                            screen.blit(soda, (446, 940))
                        if i == 2 and potion != 0:
                            apple_juice = store_font.render('Яблочный сок', True, (255, 255, 255))
                            screen.blit(apple_juice, (605, 940))
                        if i == 3 and potion != 0:
                            jelly = store_font.render('Кисель', True, (255, 255, 255))
                            screen.blit(jelly, (815, 940))


        class Cocktail(pygame.sprite.Sprite):  # Коктель(Отображение стакана - все ост к Inside)
            def __init__(self, cocktail, pos_x, pos_y):
                super().__init__(all_sprites, cocktail_group)
                self.image = dream_im
                self.cocktail = []
                self.rect = self.image.get_rect().move(pos_x, pos_y)
                size = 0
                for i, potion in enumerate(cocktail):
                    if i == 0 and potion:
                        self.cocktail.append(['вишневый компот', potion / 10])
                    if i == 1 and potion:
                        self.cocktail.append(['газировка', potion / 10])
                    if i == 2 and potion:
                        self.cocktail.append(['яблочный сок', potion / 10])
                    if i == 3 and potion:
                        self.cocktail.append(['кисель', potion / 10])
                    size += potion / 10
                Inside(pos_x, pos_y, self.cocktail, size)


        class Inside(pygame.sprite.Sprite):  # Содержимое коктеля
            def __init__(self, pos_x, pos_y, cocktail, size):
                super().__init__(inside_group, all_sprites)
                self.image = pygame.Surface([22, 45], pygame.SRCALPHA)
                self.rect = pygame.Rect(pos_x + 2, pos_y, 22, int(size * 43))
                self.cocktail = cocktail
                image = []
                for potion in self.cocktail:
                    if potion[0] == 'вишневый компот':
                        image.append(["red", int(potion[1] * 43)])
                    elif potion[0] == 'газировка':
                        image.append(["#5ED2B8", int(potion[1] * 43)])
                    elif potion[0] == 'яблочный сок':
                        image.append(["#B4F63D", int(potion[1] * 43)])
                    elif potion[0] == 'кисель':
                        image.append(["#E768AB", int(potion[1] * 43)])
                for i, potion in enumerate(image):
                    bottom = 0
                    for j in range(i):
                        bottom += image[j][1]
                    screen.fill(pygame.Color(potion[0]),
                                (self.rect.x + 2, self.rect.y - bottom, 20, potion[1]))

            def update(self):
                image = []
                for potion in self.cocktail:
                    if potion[0] == 'вишневый компот':
                        image.append(["red", int(potion[1] * 44)])
                    elif potion[0] == 'газировка':
                        image.append(["#5ED2B8", int(potion[1] * 44)])
                    elif potion[0] == 'яблочный сок':
                        image.append(["#B4F63D", int(potion[1] * 44)])
                    elif potion[0] == 'кисель':
                        image.append(["#E768AB", int(potion[1] * 44)])
                for i, potion in enumerate(image):
                    if i == 0:
                        screen.fill(pygame.Color(potion[0]),
                                    (self.rect.x + 1, self.rect.y + 45 - potion[1], 20, potion[1]))
                        continue
                    bottom = 0
                    for j in range(i):
                        bottom += image[j][1]
                    screen.fill(pygame.Color(potion[0]),
                                (self.rect.x + 1, self.rect.y + 45 - bottom - potion[1], 20,
                                 potion[1]))


        class Coins(pygame.sprite.Sprite):  # Кошелек игрока
            def __init__(self, font, screen):
                super().__init__(all_sprites, interface_group)
                self.font = font
                self.image = money
                self.rect = self.image.get_rect().move(950, 10)
                self.cap = 100
                cap_viw = self.font.render(str(self.cap), True, (200, 200, 0))
                screen.blit(cap_viw, (940, 15))

            def update(self):
                cap_viw = self.font.render(str(self.cap), True, (200, 200, 0))
                screen.blit(cap_viw, (890, 15))

            def my_money(self):
                return self.cap

            def change_cap(self, count):
                global all_coins
                if count > 0:
                    all_coins += count
                self.cap += count


        class Days:  # игровой таймер
            def __init__(self, font):
                self.ms = 0
                self.s = 0
                self.m = 0
                self.d = 0
                self.font = font

            def update(self, dt):
                global st_num_of_people
                global num_of_people
                global all_days
                self.ms += dt
                if self.ms > 1000000:
                    self.s += 1
                    self.ms -= 1000000
                    pygame.display.update()
                if self.s > 60:
                    self.m += 1
                    self.s -= 60
                if self.m == 4:
                    self.d += 1
                    coins.change_cap(-1 * self.d * 5 - num_of_people * 2)
                    visitors_group.empty()
                    cocktail_group.empty()
                    inside_group.empty()
                    st_num_of_people += 2 + len(racks_group)
                    num_of_people = st_num_of_people
                    for rack in racks_group:
                        rack.time = 0
                    self.m = 0
                    all_days += 1
                    pygame.mixer.music.play()
                self.ms += clock.tick_busy_loop(60)
                time_viw = self.font.render('Время:', True, (255, 255, 255))
                screen.blit(time_viw, (910, 60))
                time_viw = self.font.render(str(self.m) + ':' + str(self.s), True, (255, 255, 255))
                screen.blit(time_viw, (910, 85))
                day_viw = self.font.render('День:', True, (255, 255, 255))
                screen.blit(day_viw, (910, 125))
                day_viw = self.font.render(str(self.d), True, (255, 255, 255))
                screen.blit(day_viw, (910, 155))
                peop = self.font.render('Людей:', True, (255, 255, 255))
                screen.blit(peop, (910, 175))
                peop = self.font.render(str(num_of_people), True, (255, 255, 255))
                screen.blit(peop, (910, 200))


        class Tile(pygame.sprite.Sprite):  # Клетки игры
            def __init__(self, tile_type, pos_x, pos_y):
                super().__init__(tiles_group, all_sprites)
                self.image = tile_images[tile_type]
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x, tile_height * pos_y)
                self.wall = False  # Способность не проходить
                self.void = True  # Пустота клетки
                if tile_type == 'wall' or tile_type == 'door_l' or tile_type == 'door_r':
                    self.wall = True
                    self.void = False

            def get_wall(self):
                return self.wall

            def get_void(self):
                return self.void


        class Player(pygame.sprite.Sprite):  # Игрок
            def __init__(self, pos_x, pos_y):
                super().__init__(player_group, all_sprites)
                self.image = player_image
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x + cell // 2 - self.image.get_size()[0] // 2,
                    tile_height * pos_y + cell // 2 - self.image.get_size()[1] // 2)

            def walk(self, direction):
                blockers_group.update(self.rect.x, self.rect.y)
                if direction == 'up':
                    if not pygame.sprite.spritecollideany(block_u,
                                                          tiles_group).get_wall() \
                            and not pygame.sprite.spritecollideany(block_u, obj_group):
                        self.rect.y -= cell

                elif direction == 'down':
                    if not pygame.sprite.spritecollideany(block_d,
                                                          tiles_group).get_wall() \
                            and not pygame.sprite.spritecollideany(block_d, obj_group):
                        self.rect.y += cell

                elif direction == 'left':
                    if not pygame.sprite.spritecollideany(block_l,
                                                          tiles_group).get_wall() \
                            and not pygame.sprite.spritecollideany(block_l, obj_group):
                        self.rect.x -= cell
                elif direction == 'right':
                    if not pygame.sprite.spritecollideany(block_r,
                                                          tiles_group).get_wall() \
                            and not pygame.sprite.spritecollideany(block_r, obj_group):
                        self.rect.x += cell
                blockers_group.update(self.rect.x, self.rect.y)
                if direction == 'up':
                    self.image = player_rear
                    pygame.sprite.spritecollideany(block_u, blockers_group).select()
                elif direction == 'down':
                    self.image = player_image
                    pygame.sprite.spritecollideany(block_d, blockers_group).select()
                elif direction == 'left':
                    self.image = player_side_l
                    pygame.sprite.spritecollideany(block_l, blockers_group).select()
                elif direction == 'right':
                    self.image = player_side_r
                    pygame.sprite.spritecollideany(block_r, blockers_group).select()


        player = None


        class Continue(pygame.sprite.Sprite):  # Кнопка начала следующего дня
            def __init__(self):
                super().__init__(all_sprites, button_group)
                self.image = pygame.Surface([200, 40])
                self.image.fill(pygame.Color(100, 100, 100))
                self.rect = self.image.get_rect().move(800, 800)
                self.tx = inf_font.render("Следующий день", True, (255, 255, 255))

            def update(self):
                m_pos = pygame.mouse.get_pos()
                x, y = self.rect.x, self.rect.y
                width_b, height_b = self.rect.size
                if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
                    tx = inf_font.render('Следующий день', True, (100, 100, 100))
                    screen.blit(tx, (840, 815))
                else:
                    tx = inf_font.render('Следующий день', True, (255, 255, 255))
                    screen.blit(tx, (840, 815))

            def clicked(self):
                days.m = 4
                days.update(0)


        def generate_level(level):
            new_player, x, y = None, None, None
            for y in range(len(level)):
                for x in range(len(level[y])):
                    if level[y][x] == '.':
                        Tile('empty', x, y)
                    elif level[y][x] == '#':
                        Tile('wall', x, y)
                    elif level[y][x] == '@':
                        Tile('empty', x, y)
                        new_player = Player(x, y)
                    elif level[y][x] == '/':
                        Tile('door_l', x, y)
                    elif level[y][x] == '\\':
                        Tile('door_r', x, y)
            # вернем игрока, а также размер поля в клетках
            return new_player, x, y


        def upload_map(map):
            # Загрузить карту
            try:
                player, level_x, level_y = generate_level(load_level(map))
                return player, level_x, level_y
            except FileNotFoundError:
                print('В папке date нет такого файла')
                return upload_map(input())


        cont = Continue()
        player, level_x, level_y = upload_map("map.txt")
        block_r = Blocker(player.rect.x, player.rect.y, 'right')
        block_l = Blocker(player.rect.x, player.rect.y, 'left')
        block_d = Blocker(player.rect.x, player.rect.y, 'down')
        block_u = Blocker(player.rect.x, player.rect.y, 'up')
        coins = Coins(coins_font, screen)
        glass = Glass()
        days = Days(coins_font)

        clock = pygame.time.Clock()
        fps = 60


        class Play(pygame.sprite.Sprite):  # Кнопка продолжения игры
            def __init__(self):
                super().__init__(second_button_group)
                self.image = button_im
                self.rect = self.image.get_rect().move(400, 400)
                self.tx = main_font.render('Продолжить', True, (255, 255, 255))

            def update(self):
                m_pos = pygame.mouse.get_pos()
                x, y = self.rect.x, self.rect.y
                width_b, height_b = self.rect.size
                if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
                    tx = main_font.render('Продолжить', True, (150, 150, 150))
                    screen.blit(tx, (453, 420))
                else:
                    screen.blit(self.tx, (453, 420))

            def clicked(self):
                global esc
                inf.cl = False
                esc = False


        class Information(pygame.sprite.Sprite):  # Кнопка информации во время паузы
            def __init__(self):
                super().__init__(second_button_group)
                self.image = button_im
                self.rect = self.image.get_rect().move(400, 480)
                self.tx = main_font.render('Игровая механика', True, (255, 255, 255))
                self.cl = False

            def update(self):
                if self.cl:
                    tx = ["Цель: продавать правильный напиток",
                          "Правильный напиток - напиток, который запросил посетитель",
                          "Посетители приходят за стойки",
                          "Поставить стойку - лкм(цена - 20 монет)",
                          "Ингредиенты для напитков находятся и покупаются в бочках",
                          "Поставить бочку - пкм(цена - 10 монет) - на 6 заказ ломается",
                          "В бочке можно покупать ингредиенты по 5 монет",
                          "Каждый день снимаются деньги (+ 5 монет за каждый день)",
                          'Для заработка продавайте коктейли(\"Е\")',
                          'Оценивается правильность ингредиентов и их соотношение',
                          'Бочки и стойки можно продовать - Ctrl + ЛКМ']
                    for i, st in enumerate(tx):
                        st = main_font.render(st, True, (255, 255, 255))
                        if i > 6:
                            screen.blit(st, (100, 400 + i * 40))
                        else:
                            screen.blit(st, (100, 100 + i * 40))


                else:
                    self.image = button_im
                    self.rect = self.image.get_rect().move(400, 480)
                    self.tx = main_font.render('Игровая механика', True, (255, 255, 255))
                    m_pos = pygame.mouse.get_pos()
                    x, y = self.rect.x, self.rect.y
                    width_b, height_b = self.rect.size
                    if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
                        tx = main_font.render('Игровая механика', True, (150, 150, 150))
                        screen.blit(tx, (410, 500))
                    else:
                        screen.blit(self.tx, (410, 500))

            def clicked(self):
                if not self.cl:
                    self.cl = True
                else:
                    self.cl = False


        class Close(pygame.sprite.Sprite):  # Закончить игру
            def __init__(self):
                super().__init__(second_button_group)
                self.image = button_im
                self.rect = self.image.get_rect().move(400, 560)
                self.tx = main_font.render('Закрыть', True, (255, 255, 255))

            def update(self):
                m_pos = pygame.mouse.get_pos()
                x, y = self.rect.x, self.rect.y
                width_b, height_b = self.rect.size
                if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
                    tx = main_font.render('Закрыть', True, (150, 150, 150))
                    screen.blit(tx, (473, 580))
                else:
                    screen.blit(self.tx, (473, 580))

            def clicked(self):
                global game
                global running
                global gl_running
                global esc
                esc = False
                gl_running = False
                running = False


        play = Play()
        inf = Information()
        close = Close()
        then = datetime.datetime.now()

        while running:
            blocker = None
            for blocker in blockers_group:
                if blocker.selected:
                    break
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:  # Выход
                    gl_running = False
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if num_of_people == 0 and not visitors_group and event.button == 1:
                        button_group.draw(screen)
                        cont.update()  # Обновление кнопки следующего уровня
                        up_button(cont)
                    if event.button == 1 and keys[pygame.K_LCTRL]:  # Удаление
                        delete(pygame.mouse.get_pos())
                    elif event.button == 1 and get_place(pygame.mouse.get_pos(),
                                                         'rack'):  # Создание стойки
                        Rack(place(pygame.mouse.get_pos(), 'rack'))
                    elif event.button == 1 and pygame.sprite.spritecollideany(blocker,
                                                                              case_group) and \
                            pygame.sprite.spritecollideany(blocker, case_group).store(
                                store_font) and coins.my_money() >= 5:  # Заказ ингредиентов
                        pygame.sprite.spritecollideany(blocker, case_group).crushed()
                        if pygame.sprite.spritecollideany(blocker, case_group):
                            d = pygame.sprite.spritecollide(blocker, drinks_group, True)
                            Drink(
                                str(pygame.sprite.spritecollideany(blocker, case_group).store(
                                    store_font)),
                                blocker.rect.x, blocker.rect.y)  # Создание жидкости
                            pygame.sprite.spritecollideany(blocker,
                                                           case_group).fill()  # Передача жидкости в контейнер
                            coins.change_cap(-5)
                    elif event.button == 3 and get_place(pygame.mouse.get_pos(),
                                                         'case'):  # Создание бочки
                        Case(place(pygame.mouse.get_pos(), 'case'))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        player.walk('up')
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        player.walk('down')
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.walk('left')
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.walk('right')
                    elif event.key == pygame.K_e and pygame.sprite.spritecollideany(blocker,
                                                                                    visitors_group):  # Продажа
                        sell(blocker)
                    elif event.key == pygame.K_ESCAPE:  # Пауза
                        esc = True
                        while esc:
                            for event2 in pygame.event.get():
                                if event2.type == pygame.QUIT:
                                    running = False
                                    gl_running = False
                                    esc = False
                                if event2.type == pygame.KEYDOWN:
                                    if event2.key == pygame.K_ESCAPE:
                                        inf.cl = False
                                        esc = False
                                if event2.type == pygame.MOUSEBUTTONDOWN:
                                    if event2.button == 1:
                                        up_button(play)
                                        up_button(inf)
                                        up_button(close)
                            second_button_group.draw(screen)
                            second_button_group.update()
                            pygame.display.flip()
                    if not running:
                        break
                    if not gl_running:
                        pygame.quit()
                        running = False

                if keys[pygame.K_f]:  # Сливание жидкости
                    glass.pour_out()
                    glass.update()
                if keys[pygame.K_SPACE] and glass.volume < 1:  # Навбор жидкости
                    if pygame.sprite.spritecollideany(blocker, case_group):
                        if pygame.sprite.spritecollideany(blocker, case_group).completed:
                            if pygame.sprite.spritecollideany(blocker, drinks_group).change():
                                glass.pouring(
                                    pygame.sprite.spritecollideany(blocker, case_group))

            clock.tick(fps)
            all_sprites.draw(screen)
            if pygame.sprite.spritecollideany(blocker,
                                              obj_group):  # Передача информации о блоке
                obj = pygame.sprite.spritecollideany(blocker, obj_group)
                obj.get_info(inf_font, store_font)
            if pygame.sprite.spritecollideany(blocker,
                                              visitors_group):  # Передача информации о блоке
                obj = pygame.sprite.spritecollideany(blocker, visitors_group)
                obj.get_info(inf_font, store_font)
            if racks_group and num_of_people:
                if any([i.get_free() for i in racks_group]):
                    rack = None
                    for rack in racks_group:
                        if rack.get_free() and rack.time == 0:
                            Visitor(rack, visitor_image)
            if coins.my_money() < 0:
                running = False
            case_group.draw(screen)  # Отрисовка бочек
            glass.update()  # Обновление стакана
            visitors_group.update()  # Обновление посетителей
            obj_group.draw(screen)  # Отрисовка всех объектов
            inside_group.update()  # Обновление комплектующих запросов
            cocktail_group.draw(screen)  # Отрисовка коктэйля
            player_group.draw(screen)  # Отрисовка игрока
            interface_group.update()  # Обновление интерфейса
            interface_group.draw(screen)  # Отрисовка интерфейса
            now = datetime.datetime.now()  # Время сейчас
            days.update((now - then).microseconds)  # Обновление дней
            racks_group.update((now - then).microseconds)  # Обновление стоек
            then = datetime.datetime.now()  # Начало времени до цикла
            if num_of_people == 0 and not visitors_group:
                button_group.draw(screen)
                cont.update()  # Обновление кнопки следующего уровня
            pygame.display.flip()
        if not gl_running:
            pygame.quit()

    elif game == 2:  # Экран информации
        screen = pygame.display.set_mode(size)
        screen.fill("black")
        pygame.display.set_caption('Barmanman')
        main_font = load_font('mainfont.ttf', 25)
        bg_image = load_image("start_menu.jpg")
        bg_image = pygame.transform.scale(bg_image, [1002, 1002])
        button_im = load_image("button.png", -1)
        running = True

        tx = ["Цель: продавать правильный напиток",
              "Правильный напиток - напиток, который запросил посетитель",
              "Посетители приходят за стойки",
              "Поставить стойку - лкм(цена - 20 монет)",
              "Ингредиенты для напитков находятся и покупаются в бочках",
              "Поставить бочку - пкм(цена - 10 монет)",
              "В бочке можно покупать ингредиенты по 5 монет",
              "Каждый день снимаются деньги (+ 5 монет за каждый день)",
              'Для заработка продавайте коктейли(\"Е\")',
              'Оценивается правильность ингредиентов и их соотношение']

        all_sprites = pygame.sprite.Group()
        bg_group = pygame.sprite.Group()
        button_group = pygame.sprite.Group()


        class Back(pygame.sprite.Sprite):  # Вернуться к главному меню
            def __init__(self):
                super().__init__(all_sprites, button_group)
                self.image = button_im
                self.rect = self.image.get_rect().move(10, 10)
                self.tx = main_font.render('Назад', True, (255, 255, 255))

            def update(self):
                m_pos = pygame.mouse.get_pos()
                x, y = self.rect.x, self.rect.y
                width_b, height_b = self.rect.size
                if m_pos[0] in range(x, x + width_b) and m_pos[1] in range(y, y + height_b):
                    tx = main_font.render('Назад', True, (150, 150, 150))
                    screen.blit(tx, (90, 30))
                else:
                    screen.blit(self.tx, (90, 30))

            def clicked(self):
                global game
                global running
                game = 0
                running = False


        class Bg(pygame.sprite.Sprite):  # Задний фон
            def __init__(self):
                super().__init__(all_sprites, bg_group)
                self.image = bg_image
                self.rect = self.image.get_rect().move(-2, -3)


        bg = Bg()
        back = Back()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    gl_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        up_button(back)
            all_sprites.draw(screen)
            button_group.draw(screen)
            for i, st in enumerate(tx):
                st = main_font.render(st, True, (255, 255, 255))
                screen.blit(st, (100, 100 + i * 40))
            button_group.update()
            pygame.display.flip()
        if not gl_running:
            pygame.quit()
if all_coins > 0:
    records = open("data/records.txt", mode="rt").readlines()
    if records:
        record = []
        for i in records:
            if i == '\n':
                break
            i = i.split(' ')
            if len(i[0]) < 5:
                i[0] = i[0] + '_' * (5 - len(i[0]))
            record.append((i[0], int(i[1]), int(i[2])))
    else:
        record = []
    if len(player_name) < 5:
        player_name = player_name + '_' * (5 - len(player_name))
    record.append((player_name, all_days, all_coins))
    record1 = sorted(record, key=lambda x: x[1], reverse=True)
    record2 = sorted(record, key=lambda x: x[2], reverse=True)
    records = open("data/records.txt", mode="w")
    for lines in record1:
        records.write(str(lines[0]) + ' ' + str(lines[1]) + ' ' + str(lines[2]) + '\n')
    records.write('\n')
    for lines in record2:
        records.write(str(lines[0]) + ' ' + str(lines[1]) + ' ' + str(lines[2]) + '\n')
    records.write('\n')
    records.close()
