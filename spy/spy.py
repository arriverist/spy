import time
import pygame
import os
import sys
import sqlite3
from random import randint as rd
import datetime


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class basement(pygame.sprite.Sprite):
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_pos(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def check_pos(self, pos):
        return (self.rect.x + self.V[0][0] <= pos[0] <= self.rect.x + self.V[0][1] and
                self.rect.y + self.V[1][0] <= pos[1] <= self.rect.y + self.V[1][1])

    def update_spy(self, spy):
        self.spy = spy


class checker(basement):
    def check(self):
        return self.name if pygame.sprite.collide_mask(self, mouse) else ''


class update_opened(basement):
    def update_pos(self, position):
        if position == self.opened_pos:
            self.opened = True
        else:
            self.opened = False
        self.rect.x = position[0]
        self.rect.y = position[1]


class moving_sprite(basement):
    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class tick_moving_sprite(basement):
    def update(self):
        if self.step % self.tick == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.step += 1


class Dialog(moving_sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)


class Sound_button(moving_sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.play = True

    def check(self):
        if pygame.sprite.collide_mask(self, mouse):
            return True
        return False

    def turn(self):
        self.play = not self.play


class Dress_code(basement):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.V = [[42, 140], [54, 161]]


class Face(basement):
    def __init__(self, sheet, columns, rows, x, y, i):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = i
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.V = [[20, 100], [0, 140]]


class Eyes(tick_moving_sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.step = 0
        self.tick = 10


class Nose(basement):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.step = 0


class Teeth(moving_sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = rd(0, 4)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)


class Hat(basement):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = rd(0, 4)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.V = [[0, 120], [0, 55]]


class Glasses(moving_sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = rd(0, 4)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.V = [[0, 120], [0, 55]]


class MOUSE(basement):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(10000, 10000)
        self.mask = pygame.mask.from_surface(self.image)

    def change_back(self):
        self.frames = []
        self.cut_sheet(load_image('cursor1.png'), 1, 2)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]


class Item(checker):
    def __init__(self, sheet, columns, rows, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(10000, 10000)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = el


class Book(update_opened):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(10000, 10000)
        self.opened_pos = (150, 25)


class City(checker):
    def __init__(self, sheet, columns, rows, picture, pos, name):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.pos = pos
        self.picture = picture
        self.name = name
        self.rect = self.rect.move(pos[0], pos[1])

    def hide(self):
        self.rect.x = 10000
        self.rect.y = 10000

    def unhide(self):
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def give_ping(self):
        return self.picture


class BACK(basement):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(10, 46)
        self.cur_map_name = 'map'
        self.saif = Saif(load_image('seif.png'), 1, 1,  'seif')

    def change_back(self, adress):
        self.frames = []
        self.cut_sheet(load_image(adress + '_fon.png'), 1, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def open_start(self):
        self.cur_map_name = 'start'
        self.frames = []
        self.cut_sheet(load_image('bond_screen.png'), 1, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def open_end(self):
        self.cur_map_name = 'perg'
        self.frames = []
        self.cut_sheet(load_image('pergament.jpg'), 1, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def return_back(self):
        self.cur_map_name = 'map'
        self.frames = []
        self.cut_sheet(load_image('karta.jpg'), 1, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.saif.update_pos((10000, 10000))

    def bonds_house(self):
        self.frames = []
        self.cur_map_name = 'bond'
        self.cut_sheet(load_image('bonds_room.jpg'), 1, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.saif.update_pos((750, 310))


class Saif(checker):
    def __init__(self, sheet, columns, rows, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(10000, 10000)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = el


class Inventory(update_opened):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(10000, 10000)
        self.opened_pos = (380, 500)


class Comix(update_opened):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(10000, 10000)
        self.opened = False
        self.opened_pos = (0, 0)

    def change(self):
        self.cur_frame += 1
        self.cur_frame %= len(self.frames)
        self.image = self.frames[self.cur_frame]


class Window(update_opened):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(10000, 10000)
        self.book = Book(load_image('book.png'), 1, 1)
        self.book_opened = False
        self.inventory = Book(load_image('chooser.png'), 1, 1)
        self.inventory_opened = False
        self.opened = False
        self.opened_pos = (400, 260)

    def show_book(self):
        self.book_opened = True
        self.book.update_pos((150, 25))
        self.book.update_spy(self.spy)

    def show_enventory(self):
        self.inventory_opened = True
        self.inventory.update_pos((380, 500))
        self.inventory.update_spy(self.spy)

    def just_show_inv(self):
        self.inventory_opened = True
        self.inventory.update_pos((380, 500))

    def close_book(self):
        self.book_opened = False
        self.book.update_pos((10000, 10000))

    def close_env(self):
        self.inventory_opened = False
        self.inventory.update_pos((10000, 10000))

    def is_clicked(self, pos):
        x, y = pos[0], pos[1]
        if self.opened:
            if self.rect.x + 64 <= x <= self.rect.x + 148 and self.rect.y + 46 <= y <= self.rect.y + 133:
                return 1
            elif self.rect.x + 160 <= x <= self.rect.x + 244 and self.rect.y + 48 <= y <= self.rect.y + 134:
                return 2
            elif self.rect.x + 264 <= x <= self.rect.x + 347 and self.rect.y + 48 <= y <= self.rect.y + 134:
                return 3
            elif self.rect.x + 371 <= x <= self.rect.x + 456 and self.rect.y + 46 <= y <= self.rect.y + 133:
                return 4
        return 0


class Inside_saif(basement):
    def __init__(self, sheet, columns, rows):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(10000, 10000)


class Escape(checker):
    def __init__(self, sheet, columns, rows, x, y, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = el


class Info(checker):
    def __init__(self, sheet, columns, rows, x, y, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = el


class Info_screen(basement):
    def __init__(self, sheet, columns, rows, x, y, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(x, y)


class Bat(checker):
    def __init__(self, sheet, columns, rows, x, y, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = el

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 2
        self.image = self.frames[self.cur_frame]


class Door(checker):
    def __init__(self, sheet, columns, rows, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(10000, 10000)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = el


class Level_button(checker):
    def __init__(self, sheet, columns, rows, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(10000, 10000)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = el


class Newspaper(checker):
    def __init__(self, sheet, columns, rows, el):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image.get_rect()
        self.rect = self.rect.move(10000, 10000)
        self.mask = pygame.mask.from_surface(self.image)
        self.name = el

    def opened(self):
        if self.rect.x == 0 and self.rect.y == 0:
            return True
        else:
            return False


class Spy(basement):
    m_head_forms = ['Head_forms.png', 'Head_forms_darker.png', 'Head_forms_white.png', 'Head_forms_yellow.png']
    w_head_forms = ['Head_woman_forms.png', 'Head_woman_forms_darker.png', 'Head_woman_forms_white.png',
                    'Head_woman_forms_yellow.png']
    m_hair = ['Man_brown_hair.png', 'Man_dark_hair.png', 'Man_ginger_hair.png', 'Man_white_hair.png',
              'Man_yellow_hair.png']
    w_hair = ['Woman_brown_hair.png', 'Woman_dark_hair.png', 'Woman_ginger_hair.png', 'Woman_white_hair.png',
              'Woman_yellow_hair.png']
    m_eyes = ['eyes_elbrow_up.png', 'eyes_elbrow_up_blue.png', 'eyes_elbrow_up_purple.png', 'eyes_elbrow_up_red.png',
              'eyes_elbrow_up_red_pain.png', 'Plain_point_eyes.png', 'Bad_eyes.png']
    w_eyes = ['eyes_elbrow_up_red_woman.png', 'eyes_elbrow_up_green_woman.png', 'eyes_elbrow_up_purple_woman.png',
              'eyes_elbrow_up_blue_woman.png']
    nose = ['Nose.png', 'Nose1.png', 'Nose2.png']
    leaps = ['teeths1.png', 'lips_blue.png', 'lips_dark_dark_red.png', 'lips_red.png', 'lips_green.png',
             'lips_dark_red.png']
    dress = ['Coat.png', 'Dress.png']
    glass = ['Glasses_big_black.png', 'Glasses_big_black_with_gold.png', 'Glasses_big_black_with_silver.png',
             'Glasses_big_clear.png', 'Glasses_big_clear_with_gold.png', 'Glasses_big_clear_with_silver.png',
             'Steampunk_glasses.png']

    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)

        # личная информация
        self.alive = True
        self.bad = False
        self.gender = ['M', 'W'][rd(0, 1)]
        self.age = rd(16, 96)

        # настройка собственной картинки
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.knowings = ''

        # информация о выбранных спрайтах
        self.glasses_pict = Spy.glass[rd(0, 6)]
        self.nose_pict = Spy.nose[rd(0, 2)]
        self.head_form_pict = Spy.m_head_forms[rd(0, 3)] if self.gender == 'M' else Spy.w_head_forms[rd(0, 3)]
        self.eyes_pict = Spy.m_eyes[rd(0, 6)] if self.gender == 'M' else Spy.w_eyes[rd(0, 3)]
        self.hair_pict = Spy.m_hair[rd(0, 4)] if self.gender == 'M' else Spy.w_hair[rd(0, 4)]
        self.mouth_pict = Spy.leaps[0] if self.gender == 'M' else Spy.leaps[rd(1, 5)]

        # сгенерируем личный номер шпиона
        number_now = open('numbers.txt', 'r')
        numbers = number_now.read().split('\n')
        self.number = ''
        while self.number == '' or self.number in numbers and self.number != '007':
            self.number = rd(0, 100)
            self.number = '0' * (3 - len(str(self.number))) + str(self.number)
        numbers.append(str(self.number))
        if numbers[0] == '':
            del numbers[0]
        number_list = open('numbers.txt', 'w')
        number_list.write('\n'.join(numbers))

        # сгенерируем любимый предмет шпиона
        self.item = rd(0, 25)
        self.item_name = ''
        if self.item < 15:
            self.item_name = ['яблоко', 'рюкзак', 'книга',
                              'зажигалка', 'рыбка', 'карта', 'таблетки',
                              'веревка', 'мыло', 'ложка', 'фонарик', 'хлеб',
                              'ягоды', 'топливо', 'граната'][self.item]
        if self.item == '':
            self.good_answer_chanse = rd(60, 80)
        else:
            self.good_answer_chanse = rd(30, 50)
        con = sqlite3.connect('films.db')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM items WHERE name is ?""", (self.item_name,)).fetchall()
        if self.item_name != '':
            self.item_name = result[0][rd(0, 6)]
        gender_num = 1 if self.gender == 'W' else 0

        # сгенерируем внешний вид шпиона
        # · одежду в соответствии с полом
        self.dress = Dress_code(load_image(Spy.dress[gender_num]), 1, 1, x - 68, y - 46)

        # · зубы\губы в соответствии с полом
        self.mouth = Teeth(load_image(self.mouth_pict), 1, 5, x, y)
        self.step = rd(0, 5)

        # · лицо и волосы в соответствии с полом
        hair_type = rd(0, 6)
        if self.gender == 'M':
            face_type = rd(0, 15)

            if face_type in [3, 11, 13, 1]:
                self.face = Face(load_image(self.head_form_pict), 4, 4, x - 42, y - 60, face_type)
                self.hair = Face(load_image(self.hair_pict), 3, 3, x - 42, y - 82, hair_type)
            elif face_type in [2, 10, 12, 0]:
                self.face = Face(load_image(self.head_form_pict), 4, 4, x - 42, y - 63, face_type)
                self.hair = Face(load_image(self.hair_pict), 3, 3, x - 42, y - 85, hair_type)
            elif face_type in [5, 7]:
                self.face = Face(load_image(self.head_form_pict), 4, 4, x - 42, y - 70, face_type)
                self.hair = Face(load_image(self.hair_pict), 3, 3, x - 42, y - 92, hair_type)
            elif face_type in [4, 6]:
                self.face = Face(load_image(self.head_form_pict), 4, 4, x - 42, y - 73, face_type)
                self.hair = Face(load_image(self.hair_pict), 3, 3, x - 42, y - 95, hair_type)
            elif face_type in [9, 15]:
                self.face = Face(load_image(self.head_form_pict), 4, 4, x - 42, y - 80, face_type)
                self.hair = Face(load_image(self.hair_pict), 3, 3, x - 42, y - 102, hair_type)
            elif face_type in [8, 14]:
                self.face = Face(load_image(self.head_form_pict), 4, 4, x - 42, y - 83, face_type)
                self.hair = Face(load_image(self.hair_pict), 3, 3, x - 42, y - 105, hair_type)

            # · и шляпа, возможно...
            self.hat_on = rd(0, 1)
            if self.hat_on == 0:
                self.hat = Hat(load_image('Hat.png'), 1, 5, self.rect.x - 38, self.rect.y - 85)
        else:
            face_type = rd(0, 5)
            if face_type != 3:
                self.face = Face(load_image(self.head_form_pict), 3, 2, self.rect.x - 42,
                                 self.rect.y - 63, face_type)
                self.hair = Face(load_image(self.hair_pict), 3, 3, self.rect.x - 42, self.rect.y - 70,
                                 hair_type)
            else:
                self.face = Face(load_image(self.head_form_pict), 3, 2, self.rect.x - 42,
                                 self.rect.y - 73, face_type)
                self.hair = Face(load_image(self.hair_pict), 3, 3, self.rect.x - 42, self.rect.y - 80,
                                 hair_type)
        # · глаза в соответствии с полом
        eyes_frames = 2 if self.gender == 'M' else 3
        self.eye = Eyes(load_image(self.eyes_pict), eyes_frames, eyes_frames, self.rect.x - 22, self.rect.y - 55)

        # · и очки, возможно...
        self.glasses_on = rd(0, 4)
        if self.glasses_on == 0:
            self.glasses = Glasses(load_image(self.glasses_pict), 5, 6, x - 22, y - 55)

        # · нос
        self.nose = Nose(load_image(self.nose_pict), 2, 2, x + 5, y - 30)

        # · окошко диалога
        self.dialog = Dialog(load_image("Dialog_big.png"), 3, 5, 15, 10)

    def update(self, pos):
        self.eye.update()
        if self.glasses_on == 0:
            self.glasses.update()
        if self.step % 6 == 0:
            self.mouth.update()
        if self.check_pos(pos):
            self.dialog.update_pos((self.rect.x + 40, self.rect.y - 20))
            self.dialog.update()
        else:
            self.dialog.update_pos((10000, 10000))
        self.step += 1

    def check_item(self, pict):
        con = sqlite3.connect('films.db')
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM items WHERE code_name is ?""",
                             (pict.split('.')[0],)).fetchall()
        if self.item_name == '':
            return False
        if self.item_name in ', '.join(list(result[0])):
            self.good_answer_chanse += 30
            return True
        return False

    def check_pos(self, pos):
        hat_check = False if not (self.gender == 'M' and self.hat_on == 0) else self.hat.check_pos(pos)
        return self.dress.check_pos(pos) or self.face.check_pos(pos) or hat_check or self.hair.check_pos(pos)

    def remove(self, pos):
        self.dialog.update_pos((pos[0] + self.rect.x + 40, pos[1] + self.rect.y - 20))
        if self.gender == 'M' and self.hat_on == 0:
            self.hat.update_pos((pos[0] + self.rect.x - self.hat.rect.x, pos[1] + self.rect.y - self.hat.rect.y - 20))
        if self.glasses_on == 0:
            self.glasses.update_pos((pos[0] - 22, pos[1] - 60))
        self.face.update_pos((pos[0] + self.rect.x - self.face.rect.x, pos[1] + self.rect.y - self.face.rect.y))
        self.mouth.update_pos((pos[0] + self.rect.x - self.mouth.rect.x, pos[1] + self.rect.y - self.mouth.rect.y))
        self.nose.update_pos((pos[0] + self.rect.x - self.nose.rect.x, pos[1] + self.rect.y - self.nose.rect.y))
        self.eye.update_pos((pos[0] + self.rect.x - self.eye.rect.x, pos[1] + self.rect.y - self.eye.rect.y))
        self.dress.update_pos((pos[0] + self.rect.x - self.dress.rect.x, pos[1] + self.rect.y - self.dress.rect.y))
        self.hair.update_pos((pos[0] + self.rect.x - self.hair.rect.x, pos[1] + self.rect.y - self.hair.rect.y))
        self.rect.x = pos[0]
        self.rect.y = pos[1]


if __name__ == '__main__':
    pygame.init()
    now = datetime.datetime.now()
    pygame.mouse.set_visible(False)
    ans = open('numbers.txt', 'w')
    ans.write('')
    all_sprites = pygame.sprite.Group()
    back = BACK(load_image('karta.jpg'), 1, 1)
    places = []
    underscreen = (10000, 10000)
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
    screen = pygame.display.set_mode((1300, 700))
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
    clock = pygame.time.Clock()
    running = True
    opened_flag = False
    tx = pygame.font.Font('C:/NEIRO/data_boom/data/SlackCasual-Bold-Cyr.ttf', 60)
    tx_s = pygame.font.Font('C:/NEIRO/data_boom/data/SlackCasual-Bold-Cyr.ttf', 45)
    door = Door(load_image('door.png'), 1, 1, 'bond_door')
    door.update_pos((1219, 576))
    insaif = Inside_saif(load_image('seif_fon.png'), 1, 1)
    insaif.update_pos((10000, 10000))
    inven = ['apple', 'book', 'fish', 'map', 'rope', 'lamp', 'gazoline', 'granade', 'bread',
             'berry', 'soap', 'spoon', 'medecine', 'backpack', 'fire']
    for el in [['paris', (630, 250)], ['london', (540, 220)], ['moscow', (720, 220)],
               ['america', (200, 200)], ['china', (920, 300)], ['japan', (1100, 450)], ['egypt', (790, 340)]]:
        places.append([el[0], City(load_image(el[0] + '_c.jpg'), 1, 1, el[0] + '.png', el[1], el[0]),
                       [Spy(load_image('base.png'), 2, 2, i % 2, i // 2) for i in range(4)]])
        for elem in places[-1][-1]:
            elem.remove(underscreen)
    invent = []
    for i in range(5):
        invent.append(inven[rd(0, len(inven) - 1)])
        del inven[inven.index(invent[-1])]
    window = Window(load_image('window.png'), 1, 1)
    items = [Item(load_image(el), 1, 1, el) for el in ['apple.jpg', 'backpack.jpg',
                                                       'book.jpg', 'fire.jpg',
                                                       'fish.jpg', 'map.jpg',
                                                       'medecine.jpg', 'rope.jpg',
                                                       'soap.jpg', 'spoon.jpg',
                                                       'berry.jpg', 'bread.jpg',
                                                       'gazoline.jpg', 'granade.jpg',
                                                       'lamp.jpg']]
    good_comix = Comix(load_image('good_item.png'), 1, 2)
    bad_comix = Comix(load_image('bad_item.png'), 1, 2)
    comixes = [Comix(load_image(el[0]), 1, el[1]) for el in [('1_bad_ans.png', 3),
                                                                     ('1_good_ans.png', 3),
                                                                     ('3_bad_ans.png', 5), ('3_good_ans.png', 5),
                                                                     ('5_bad_ans.png', 7), ('5_good_ans.png', 7),
                                                                     ('6.png', 6), ('run.png', 6)]]
    news = Newspaper(load_image('news.png'), 1, 1, 'newspaper')
    info = Info(load_image('info.png'), 1, 1, 0, 0, 'info')
    bat = Bat(load_image('bat.png'), 1, 2, 900, 300, 'bat')
    level_screen = Info_screen(load_image('i_screen.png'), 1, 1, 10000, 10000, 'level_screen')
    info_screen = Info_screen(load_image('info_screen.png'), 1, 1, 10000, 10000, 'info_screen')
    easy_level = Level_button(load_image('level_button.png'), 1, 1, '1')
    medium_level = Level_button(load_image('level_button.png'), 1, 1, '2')
    hard_level = Level_button(load_image('level_button.png'), 1, 1, '3')
    music = Sound_button(load_image('music.png'), 1, 2, 1240, 0)
    escape = Escape(load_image('escape.png'), 1, 1, 0, 650, 'esc')
    Win = Info_screen(load_image('win.png'), 1, 1, 10000, 10000, 'w')
    Lose = Info_screen(load_image('lose.png'), 1, 1, 10000, 10000, 'l')
    mouse = MOUSE(load_image('cursor.png'), 1, 2)
    window.update_pos(underscreen)
    back.open_start()
    door.update_pos(underscreen)
    for elem in places:
        elem[1].hide()
    escape.update_pos(underscreen)
    com_counter = 25
    flag = False
    codes = {}
    text_news = (tx.render('', False, (0, 0, 0)), (250, 400))
    text_comix = (tx.render('', False, (0, 0, 0)), (800, 550))
    text_end = (tx.render('', False, (0, 0, 0)), (250, 400))
    level = (tx.render('', False, (0, 0, 0)), (20, 20))
    easy_level_t = (tx.render('', False, (0, 0, 0)), (20, 220))
    medium_level_t = (tx.render('', False, (0, 0, 0)), (20, 420))
    hard_level_t = (tx.render('', False, (0, 0, 0)), (20, 620))
    spyes = (tx.render('', False, (0, 0, 0)), (20, 220))
    secs = (tx.render('', False, (0, 0, 0)), (20, 420))
    cur_place = 'map'
    mcounter = 0
    point_counter = 0
    spy_count = 0
    win = False
    time_end = None
    while running:
        if time_end is not None:
            cur_time = datetime.datetime.now()
            if (cur_time - time_end).seconds >= 5:
                if win:
                    Win.update_pos((0, 0))
                    text_end = (tx.render('', False, (0, 0, 0)), (250, 400))
                    spyes = (tx.render('', False, (0, 0, 0)), (20, 220))
                    secs = (tx.render('', False, (0, 0, 0)), (20, 420))
                else:
                    Lose.update_pos((0, 0))
                    text_news = (tx.render('', False, (0, 0, 0)), (250, 400))
        if not pygame.mixer.Channel(0).get_busy():

            pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/music' + str(mcounter) + '.mp3'))
            pygame.mixer.music.set_volume(0.5)
            mcounter += 1
            mcounter %= 3
        texts = []
        if not pygame.mixer.music.get_busy():
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if (pygame.key.get_pressed()[pygame.K_ESCAPE] and not back.cur_map_name == 'perg' and
                        not Win.rect.x ==0 and not Lose.rect.x == 0):
                    if news.opened():
                        news.update_pos(underscreen)
                        text_news = (tx.render('', False, (0, 0, 0)), (250, 400))
                    if (((not good_comix.opened and not bad_comix.opened and not any([el.opened for el in comixes]) and
                            not window.book_opened and not window.inventory_opened and not window.opened) and
                            back.cur_map_name != 'start') and
                            not (info_screen.rect.x == 0 and info_screen.rect.y == 0) and
                            not (info_screen.rect.x == 0 and info_screen.rect.y == 0)):
                        back.return_back()
                        door.update_pos((1219, 576))
                        if cur_place != 'map':
                            for i in range(len(places[codes[cur_place]][-1])):
                                if (places[codes[cur_place]][-1][i].rect.x != 10000 and
                                        places[codes[cur_place]][-1][i] != 1000):
                                    places[codes[cur_place]][-1][i].remove(underscreen)
                        for elem in places:
                            if elem[1].name in [el for el in codes]:
                                elem[1].unhide()
                            else:
                                elem[1].hide()
                        if rd(0, 3) == 0 and cur_place != 'map' and spy_count > 3:
                            while True:
                                a1 = rd(0, 4)
                                b1 = rd(0, len([el for el in codes]) - 1)
                                if places[a1][-1][b1].alive:
                                    break
                            if places[a1][-1][b1].bad:
                                flag = True
                                text_news = (tx.render('Был убит шпион! ВЫ проиграли',
                                                       False, (0, 0, 0)), (250, 400))
                                win = False
                                time_end = datetime.datetime.now()
                            else:
                                text_news = (tx.render('Был убит шпион! Мафия торжествует',
                                                       False, (0, 0, 0)), (250, 400))
                            places[a1][-1][b1].alive = False
                            news.update_pos((0, 0))
                        cur_place = 'map'
                    if not window.book and not window.inventory_opened and window.opened:
                        window.update_pos(underscreen)
                    if (info_screen.rect.x == 0 and info_screen.rect.y == 0):
                        info_screen.update_pos(underscreen)
                        info.update_pos((0, 0))
                    if insaif.rect.x == 0 and insaif.rect.y == 0:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/close_saif_2.mp3'))
                        insaif.update_pos(underscreen)
                    else:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/button.mp3'))
                    if window.book:
                        window.close_book()
                    if window.inventory_opened:
                        window.close_env()
                        for el in items:
                            if el is not None:
                                el.update_pos(underscreen)
                    if good_comix.opened:
                        good_comix.update_pos(underscreen)
                    if bad_comix.opened:
                        bad_comix.update_pos(underscreen)
                    for el in comixes:
                        if el.opened:
                            el.update_pos(underscreen)
                            text_comix = (tx.render('', False, (0, 0, 0)), (800, 550))
                            opened_flag = False
                            if flag:
                                time_end = datetime.datetime.now()
                                info.update_pos(underscreen)
                                window.update_pos(underscreen)
                                text_end = (tx.render('Игра окончена', False, (0, 0, 0)), (540, 150))
                                spyes = (tx.render('Шпионов опрошено: ' + str(spy_count), False, (0, 0, 0)), (540, 250))
                                now1 = datetime.datetime.now()
                                secs = (tx.render('Времени потрачено: ' + str((now1 - now).seconds) + ' секунд',
                                                  False, (0, 0, 0)), (540, 350))
                                door.update_pos(underscreen)
                                back.open_end()
                                escape.update_pos(underscreen)
                                for i in range(len(places[codes[cur_place]][-1])):
                                    if places[codes[cur_place]][-1][i].alive:
                                        places[codes[cur_place]][-1][i].remove(underscreen)
                            for elem in places:
                                elem[1].hide()

            if event.type == pygame.MOUSEMOTION:
                mouse.update_pos(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONDOWN and not news.opened() and not Win.rect.x ==0 and not Lose.rect.x == 0:
                res = window.is_clicked(pygame.mouse.get_pos())
                if escape.check() == 'esc':
                    if news.opened():
                        news.update_pos(underscreen)
                        text_news = (tx.render('', False, (0, 0, 0)), (250, 400))
                    if (((not good_comix.opened and not bad_comix.opened and not any([el.opened for el in comixes]) and
                          not window.book_opened and not window.inventory_opened and not window.opened) and
                         back.cur_map_name != 'start') and
                            not (info_screen.rect.x == 0 and info_screen.rect.y == 0) and
                            not (level_screen.rect.x == 0 and level_screen.rect.y == 0)):
                        back.return_back()
                        door.update_pos((1219, 576))
                        if cur_place != 'map':
                            for i in range(len(places[codes[cur_place]][-1])):
                                if (places[codes[cur_place]][-1][i].rect.x != 10000 and
                                        places[codes[cur_place]][-1][i] != 1000):
                                    places[codes[cur_place]][-1][i].remove(underscreen)
                        for elem in places:
                            if elem[1].name in [el for el in codes]:
                                elem[1].unhide()
                            else:
                                elem[1].hide()
                        if rd(0, 3) == 0 and cur_place != 'map' and spy_count > 3:
                            while True:
                                a1 = rd(0, 4)
                                b1 = rd(0, len([el for el in codes]) - 1)
                                if places[a1][-1][b1].alive:
                                    break
                            if places[a1][-1][b1].bad:
                                flag = True
                                text_news = (tx.render('Был убит шпион! ВЫ проиграли',
                                                       False, (0, 0, 0)), (250, 400))
                                win = False
                                time_end = datetime.datetime.now()
                            else:
                                text_news = (tx.render('Был убит шпион! Мафия торжествует',
                                                       False, (0, 0, 0)), (250, 400))
                            places[a1][-1][b1].alive = False
                            news.update_pos((0, 0))
                        cur_place = 'map'
                    if not window.book and not window.inventory_opened and window.opened:
                        window.update_pos(underscreen)
                    if (info_screen.rect.x == 0 and info_screen.rect.y == 0):
                        info_screen.update_pos(underscreen)
                        info.update_pos((0, 0))
                    if insaif.rect.x == 0 and insaif.rect.y == 0:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/close_saif_2.mp3'))
                        insaif.update_pos(underscreen)
                    else:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/button.mp3'))
                    if window.book:
                        window.close_book()
                    if window.inventory_opened:
                        window.close_env()
                        for el in items:
                            if el is not None:
                                el.update_pos(underscreen)
                    if good_comix.opened:
                        good_comix.update_pos(underscreen)
                    if bad_comix.opened:
                        bad_comix.update_pos(underscreen)
                    for el in comixes:
                        if el.opened:
                            el.update_pos(underscreen)
                            text_comix = (tx.render('', False, (0, 0, 0)), (800, 550))
                            opened_flag = False
                            if flag:
                                time_end = datetime.datetime.now()
                                text_end = (tx.render('Игра окончена', False, (0, 0, 0)), (540, 150))
                                spyes = (tx.render('Шпионов опрошено: ' + str(spy_count), False, (0, 0, 0)), (540, 250))
                                now1 = datetime.datetime.now()
                                secs = (tx.render('Времени потрачено: ' + str((now1 - now).seconds) + ' секунд',
                                                  False, (0, 0, 0)), (540, 350))
                                door.update_pos(underscreen)
                                back.open_end()
                                escape.update_pos(underscreen)
                                for i in range(len(places[codes[cur_place]][-1])):
                                    if places[codes[cur_place]][-1][i].alive:
                                        places[codes[cur_place]][-1][i].remove(underscreen)
                            for elem in places:
                                elem[1].hide()
                if music.check():
                    music.update()
                    music.turn()
                    if music.play:
                        pygame.mixer.Channel(0).set_volume(0.5)
                        pygame.mixer.Channel(1).set_volume(1)
                    else:
                        pygame.mixer.Channel(0).set_volume(0)
                        pygame.mixer.Channel(1).set_volume(0)
                if cur_place != 'map':
                    for i in range(len(places[codes[cur_place]][-1])):
                        if places[codes[cur_place]][-1][i].check_pos(pygame.mouse.get_pos()):
                            if not window.opened:
                                window.update_spy(places[codes[cur_place]][-1][i])
                                pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/open.mp3'))
                                window.update_pos(window.opened_pos)
                            break
                if easy_level.check() == '1':
                    level = (tx.render('', False, (0, 0, 0)), (20, 20))
                    easy_level_t = (tx.render('', False, (0, 0, 0)), (220, 20))
                    medium_level_t = (tx.render('', False, (0, 0, 0)), (420, 20))
                    hard_level_t = (tx.render('', False, (0, 0, 0)), (620, 20))
                    level_screen.update_pos(underscreen)
                    easy_level.update_pos(underscreen)
                    medium_level.update_pos(underscreen)
                    hard_level.update_pos(underscreen)
                    inven = ['apple', 'book', 'fish', 'map', 'rope', 'lamp', 'gazoline', 'granade', 'bread',
                             'berry', 'soap', 'spoon', 'medecine', 'backpack', 'fire']
                    invent = []
                    for i in range(5):
                        invent.append(inven[rd(0, len(inven) - 1)])
                        del inven[inven.index(invent[-1])]

                    codes = {'paris': 0, 'london': 1, 'moscow': 2}
                    a = rd(0, 2)
                    b = rd(0, len(places[a][-1]) - 1)
                    places[a][-1][b].bad = True
                    cur_spy = places[a][-1][b]
                    it = 'Он не нуждается в предметах' if cur_spy.item_name == '' else 'Ему нужен предмет' + cur_spy.item_name
                    bad_info = [it,
                                'Он живет в ' + ['париже', 'лондоне', 'москве', 'америке', 'китае'][a],
                                'У него номер ' + cur_spy.number,
                                'Он ' + cur_spy.gender + ' пола',
                                'Ему ' + str(cur_spy.age) + ' лет',
                                'У него ' +
                                {'Nose.png': 'нос прямой', 'Nose1.png': 'нос горкой', 'Nose2.png': 'нос с горбинкой'}
                                [cur_spy.nose_pict],
                                {'eyes_elbrow_up.png': 'У него зеленые глаза',
                                 'eyes_elbrow_up_blue.png': 'У него голубые глаза',
                                 'eyes_elbrow_up_purple.png': 'У него фиолетовые глаза',
                                 'eyes_elbrow_up_red.png': 'У него красные глаза',
                                 'eyes_elbrow_up_green_woman.png': 'У него зеленые глаза',
                                 'eyes_elbrow_up_blue_woman.png': 'У него голубые глаза',
                                 'eyes_elbrow_up_purple_woman.png': 'У него фиолетовые глаза',
                                 'eyes_elbrow_up_red_woman.png': 'У него красные глаза',
                                 'eyes_elbrow_up_red_pain.png': 'У него больные глаза',
                                 'Plain_point_eyes.png': 'У него большие глаза',
                                 'Bad_eyes.png': 'слезящиеся глаза'}[cur_spy.eyes_pict],
                                'У него ' +
                                {'Head_forms.png': 'темный цвет кожи', 'Head_forms_darker.png': 'черный цвет кожи',
                                 'Head_forms_white.png': 'белый цвет кожи', 'Head_forms_yellow.png': 'желтый цвет кожи',
                                 'Head_woman_forms.png': 'темный цвет кожи',
                                 'Head_woman_forms_darker.png': 'черный цвет кожи',
                                 'Head_woman_forms_white.png': 'белый цвет кожи',
                                 'Head_woman_forms_yellow.png': 'желтый цвет кожи'
                                 }[cur_spy.head_form_pict],
                                'У него ' + {'Woman_brown_hair.png': 'коричневые волосы',
                                             'Woman_dark_hair.png': 'чёрные волосы',
                                             'Woman_ginger_hair.png': 'рыжие волосы',
                                             'Woman_white_hair.png': 'белые волосы',
                                             'Woman_yellow_hair.png': 'жёлтые волосы',
                                             'Man_brown_hair.png': 'коричневые волосы',
                                             'Man_dark_hair.png': 'чёрные волосы',
                                             'Man_ginger_hair.png': 'рыжие волосы',
                                             'Man_white_hair.png': 'белые волосы',
                                             'Man_yellow_hair.png': 'жёлтые волосы'}[cur_spy.hair_pict]]
                    cur_place = 'map'
                    for elem in places:
                        if elem[1].name in [el for el in codes]:
                            elem[1].unhide()
                        else:
                            elem[1].hide()
                    escape.update_pos((0, 650))
                elif medium_level.check() == '2':
                    level = (tx.render('', False, (0, 0, 0)), (20, 20))
                    easy_level_t = (tx.render('', False, (0, 0, 0)), (220, 20))
                    medium_level_t = (tx.render('', False, (0, 0, 0)), (420, 20))
                    hard_level_t = (tx.render('', False, (0, 0, 0)), (620, 20))
                    codes = {'paris': 0, 'london': 1, 'moscow': 2, 'america': 3, 'china': 4}
                    a = rd(0, 4)
                    b = rd(0, len(places[a][-1]) - 1)
                    places[a][-1][b].bad = True
                    cur_spy = places[a][-1][b]
                    it = 'Он не нуждается в предметах' if cur_spy.item_name == '' else 'Ему нужен предмет' + cur_spy.item_name
                    bad_info = [it,
                                'Он живет в ' + ['париже', 'лондоне', 'москве', 'америке', 'китае'][a],
                                'У него номер ' + cur_spy.number,
                                'Он ' + cur_spy.gender + ' пола',
                                'Ему ' + str(cur_spy.age) + ' лет',
                                'У него ' +
                                {'Nose.png': 'нос прямой', 'Nose1.png': 'нос горкой', 'Nose2.png': 'нос с горбинкой'}
                                [cur_spy.nose_pict],
                                {'eyes_elbrow_up.png': 'У него зеленые глаза',
                                 'eyes_elbrow_up_blue.png': 'У него голубые глаза',
                                 'eyes_elbrow_up_purple.png': 'У него фиолетовые глаза',
                                 'eyes_elbrow_up_red.png': 'У него красные глаза',
                                 'eyes_elbrow_up_green_woman.png': 'У него зеленые глаза',
                                 'eyes_elbrow_up_blue_woman.png': 'У него голубые глаза',
                                 'eyes_elbrow_up_purple_woman.png': 'У него фиолетовые глаза',
                                 'eyes_elbrow_up_red_woman.png': 'У него красные глаза',
                                 'eyes_elbrow_up_red_pain.png': 'У него больные глаза',
                                 'Plain_point_eyes.png': 'У него большие глаза',
                                 'Bad_eyes.png': 'слезящиеся глаза'}[cur_spy.eyes_pict],
                                'У него ' +
                                {'Head_forms.png': 'темный цвет кожи', 'Head_forms_darker.png': 'черный цвет кожи',
                                 'Head_forms_white.png': 'белый цвет кожи', 'Head_forms_yellow.png': 'желтый цвет кожи',
                                 'Head_woman_forms.png': 'темный цвет кожи',
                                 'Head_woman_forms_darker.png': 'черный цвет кожи',
                                 'Head_woman_forms_white.png': 'белый цвет кожи',
                                 'Head_woman_forms_yellow.png': 'желтый цвет кожи'
                                 }[cur_spy.head_form_pict],
                                'У него ' + {'Woman_brown_hair.png': 'коричневые волосы',
                                             'Woman_dark_hair.png': 'чёрные волосы',
                                             'Woman_ginger_hair.png': 'рыжие волосы',
                                             'Woman_white_hair.png': 'белые волосы',
                                             'Woman_yellow_hair.png': 'жёлтые волосы',
                                             'Man_brown_hair.png': 'коричневые волосы',
                                             'Man_dark_hair.png': 'чёрные волосы',
                                             'Man_ginger_hair.png': 'рыжие волосы',
                                             'Man_white_hair.png': 'белые волосы',
                                             'Man_yellow_hair.png': 'жёлтые волосы'}[cur_spy.hair_pict]]
                    cur_place = 'map'
                    level_screen.update_pos(underscreen)
                    easy_level.update_pos(underscreen)
                    medium_level.update_pos(underscreen)
                    hard_level.update_pos(underscreen)
                    inven = ['apple', 'book', 'fish', 'map', 'rope', 'lamp', 'gazoline', 'granade', 'bread',
                             'berry', 'soap', 'spoon', 'medecine', 'backpack', 'fire']
                    invent = []
                    for i in range(5):
                        invent.append(inven[rd(0, len(inven) - 1)])
                        del inven[inven.index(invent[-1])]
                        del inven[rd(0, len(inven) - 1)]
                    for elem in places:
                        if elem[1].name in [el for el in codes]:
                            elem[1].unhide()
                        else:
                            elem[1].hide()
                    escape.update_pos((0, 650))
                elif hard_level.check() == '3':
                    level = (tx.render('', False, (0, 0, 0)), (20, 20))
                    easy_level_t = (tx.render('', False, (0, 0, 0)), (220, 20))
                    medium_level_t = (tx.render('', False, (0, 0, 0)), (420, 20))
                    hard_level_t = (tx.render('', False, (0, 0, 0)), (620, 20))
                    codes = {'paris': 0, 'london': 1, 'moscow': 2, 'america': 3, 'china': 4, 'japan': 5, 'egypt': 6}
                    a = rd(0, 6)
                    b = rd(0, len(places[a][-1]) - 1)
                    places[a][-1][b].bad = True
                    cur_spy = places[a][-1][b]
                    it = 'Он не нуждается в предметах' if cur_spy.item_name == '' else 'Ему нужен предмет' + cur_spy.item_name
                    bad_info = [it,
                                'Он живет в ' + ['париже', 'лондоне', 'москве', 'америке', 'китае', 'японии',
                                                 'египте'][a],
                                'У него номер ' + cur_spy.number,
                                'Он ' + cur_spy.gender + ' пола',
                                'Ему ' + str(cur_spy.age) + ' лет',
                                'У него ' +
                                {'Nose.png': 'нос прямой', 'Nose1.png': 'нос горкой', 'Nose2.png': 'нос с горбинкой'}
                                [cur_spy.nose_pict],
                                {'eyes_elbrow_up.png': 'У него зеленые глаза',
                                 'eyes_elbrow_up_blue.png': 'У него голубые глаза',
                                 'eyes_elbrow_up_purple.png': 'У него фиолетовые глаза',
                                 'eyes_elbrow_up_red.png': 'У него красные глаза',
                                 'eyes_elbrow_up_green_woman.png': 'У него зеленые глаза',
                                 'eyes_elbrow_up_blue_woman.png': 'У него голубые глаза',
                                 'eyes_elbrow_up_purple_woman.png': 'У него фиолетовые глаза',
                                 'eyes_elbrow_up_red_woman.png': 'У него красные глаза',
                                 'eyes_elbrow_up_red_pain.png': 'У него больные глаза',
                                 'Plain_point_eyes.png': 'У него большие глаза',
                                 'Bad_eyes.png': 'слезящиеся глаза'}[cur_spy.eyes_pict],
                                'У него ' +
                                {'Head_forms.png': 'темный цвет кожи', 'Head_forms_darker.png': 'черный цвет кожи',
                                 'Head_forms_white.png': 'белый цвет кожи', 'Head_forms_yellow.png': 'желтый цвет кожи',
                                 'Head_woman_forms.png': 'темный цвет кожи',
                                 'Head_woman_forms_darker.png': 'черный цвет кожи',
                                 'Head_woman_forms_white.png': 'белый цвет кожи',
                                 'Head_woman_forms_yellow.png': 'желтый цвет кожи'
                                 }[cur_spy.head_form_pict],
                                'У него ' + {'Woman_brown_hair.png': 'коричневые волосы',
                                             'Woman_dark_hair.png': 'чёрные волосы',
                                             'Woman_ginger_hair.png': 'рыжие волосы',
                                             'Woman_white_hair.png': 'белые волосы',
                                             'Woman_yellow_hair.png': 'жёлтые волосы',
                                             'Man_brown_hair.png': 'коричневые волосы',
                                             'Man_dark_hair.png': 'чёрные волосы',
                                             'Man_ginger_hair.png': 'рыжие волосы',
                                             'Man_white_hair.png': 'белые волосы',
                                             'Man_yellow_hair.png': 'жёлтые волосы'}[cur_spy.hair_pict]]
                    cur_place = 'map'
                    level_screen.update_pos(underscreen)
                    easy_level.update_pos(underscreen)
                    medium_level.update_pos(underscreen)
                    hard_level.update_pos(underscreen)
                    inven = ['apple', 'book', 'fish', 'map', 'rope', 'lamp', 'gazoline', 'granade', 'bread',
                             'berry', 'soap', 'spoon', 'medecine', 'backpack', 'fire']
                    invent = []
                    for i in range(5):
                        invent.append(inven[rd(0, len(inven) - 1)])
                        del inven[inven.index(invent[-1])]
                    inven = []
                    for elem in places:
                        if elem[1].name in [el for el in codes]:
                            elem[1].unhide()
                        else:
                            elem[1].hide()
                    escape.update_pos((0, 650))
                else:
                    for el in places:
                        if (el[1].check() != '' and back.cur_map_name != 'start' and
                                info_screen.rect.x != 0):
                            pl = el[1].check()
                            back.change_back(pl)
                            door.update_pos(underscreen)
                            cur_place = pl
                            for i in range(len(places[codes[cur_place]][-1])):
                                if places[codes[cur_place]][-1][i].alive:
                                    places[codes[cur_place]][-1][i].remove((rd(200, 1100), rd(100, 600)))
                            for elem in places:
                                elem[1].hide()
                            break
                if back.saif.check() == 'seif':
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/open_saif.mp3'))
                    insaif.update_pos((0, 0))
                    counter = 0
                    for el in items:
                        if el is not None and el.name.split('.')[0] not in invent and el.name.split('.')[0] in inven:
                            el.update_pos((50 + (counter % 12) * 100, 50 + (counter // 12) * 100))
                            counter += 1
                    window.just_show_inv()
                    for el in items:
                        if el is not None and el.name.split('.')[0] in invent:
                            r = invent.index(el.name.split('.')[0])
                            if invent.index(el.name.split('.')[0]) < 5:
                                el.update_pos((((r + 1) * 25 + r * 77) + 380, 525))
                if info.check() == 'info':
                    info.update_pos(underscreen)
                    info_screen.update_pos((0, 0))
                if bat.check() == 'bat':
                    door.update_pos((1219, 576))
                    for elem in places:
                        elem[1].unhide()
                    back.return_back()
                    bat.update_pos(underscreen)
                    level_screen.update_pos((0, 0))
                    easy_level.update_pos((450, 150))
                    medium_level.update_pos((450, 350))
                    hard_level.update_pos((450, 550))
                    level = (tx.render('Выберите уровень', False, (0, 0, 0)), (470, 20))
                    easy_level_t = (tx.render('Легкий', False, (0, 0, 0)), (470, 190))
                    medium_level_t = (tx.render('Средний', False, (0, 0, 0)), (470, 390))
                    hard_level_t = (tx.render('Сложный', False, (0, 0, 0)), (470, 590))

                if door.check() == 'bond_door' and info_screen.rect.x != 0:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/door.mp3'))
                    if back.cur_map_name == 'map':
                        back.bonds_house()
                        for elem in places:
                            elem[1].hide()
                    else:
                        back.return_back()
                        for elem in places:
                            if elem[1].name in [el for el in codes]:
                                elem[1].unhide()
                            else:
                                elem[1].hide()
                for el in items:
                    if el is not None and el.check() != '':
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/button.mp3'))
                        if insaif.rect.x != 0 and insaif.rect.y != 0:
                            if window.spy.check_item(el.check()):
                                good_comix.cur_frame = 1
                                good_comix.change()
                                com_counter = 0
                                good_comix.update_pos((0, 0))
                            else:
                                bad_comix.cur_frame = 1
                                bad_comix.change()
                                com_counter = 0
                                bad_comix.update_pos((0, 0))
                            el.update_pos(underscreen)
                            invent[invent.index(el.name.split('.')[0])] = None
                            items[items.index(el)] = None
                            break
                        else:
                            if el.name.split('.')[0] in invent:
                                x = el
                                del items[items.index(el)]
                                items.append(x)
                                items[-1].update_pos((50 + (counter % 12) * 100,
                                                      50 + (counter // 12) * 100))
                                counter += 1
                                invent[invent.index(el.name.split('.')[0])] = None
                            else:
                                if None in invent:
                                    invent[invent.index(None)] = el.name.split('.')[0]
                                    x = el
                                    del items[items.index(el)]
                                    a = invent.index(el.name.split('.')[0])
                                    items = items[:a] + [x] + items[a:]
                                    items[a].update_pos((((a + 1) * 25 + a * 77) + 380, 525))
                            break
                if res in [1, 2, 3, 4] and not window.book and not window.inventory_opened:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/button.mp3'))
                if res == 4:
                    if not window.book_opened and not window.inventory_opened:
                        window.update_pos(underscreen)
                elif res == 1:
                    if window.inventory_opened is False and window.book_opened is False:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/open.mp3'))
                        window.show_enventory()
                        for el in items:
                            if el is not None and el.name.split('.')[0] in invent:
                                r = invent.index(el.name.split('.')[0])
                                if invent.index(el.name.split('.')[0]) < 5:
                                    el.update_pos((((r + 1) * 25 + r * 77) + 380, 525))
                elif res == 2:
                    spy_count += 1
                    chanse = window.spy.good_answer_chanse
                    text_comix = (tx.render('', False, (0, 0, 0)), (800, 550))
                    if chanse > rd(0, 100):
                        if window.spy.bad:
                            comixes[1].cur_frame = -1
                            comixes[1].change()
                            com_counter = 0
                            comixes[1].update_pos((0, 0))
                            win = True
                            flag = True
                        else:
                            comixes[0].cur_frame = -1
                            comixes[0].change()
                            com_counter = 0
                            comixes[0].update_pos((0, 0))
                            sp_text = str(bad_info[rd(0, len(bad_info) - 1)])
                            if places[codes[cur_place]][-1][places[codes[cur_place]][-1].index(window.spy)].knowings == '':
                                places[codes[cur_place]][-1][
                                    places[codes[cur_place]][-1].index(window.spy)].knowings = sp_text
                                window.spy.knowings = sp_text
                                text_comix = (tx_s.render(sp_text, False, (225, 227, 3)), (800, 550))
                            else:
                                text_comix = (tx_s.render(window.spy.knowings,
                                                        False, (225, 227, 3)), (800, 550))
                    else:
                        if chanse > rd(0, 100):
                            if window.spy.bad:
                                comixes[3].cur_frame = -1
                                comixes[3].change()
                                com_counter = 0
                                comixes[3].update_pos((0, 0))
                                win = True
                                flag = True
                            else:
                                comixes[2].cur_frame = -1
                                comixes[2].change()
                                com_counter = 0
                                comixes[2].update_pos((0, 0))
                                sp_text = str(bad_info[rd(0, len(bad_info) - 1)])
                                if places[codes[cur_place]][-1][places[codes[cur_place]][-1].index(window.spy)].knowings == '':
                                    places[codes[cur_place]][-1][places[codes[cur_place]][-1].index(window.spy)].knowings = sp_text
                                    window.spy.knowings = sp_text
                                    text_comix = (tx_s.render(sp_text, False, (225, 227, 3)), (800, 550))
                                else:
                                    text_comix = (tx_s.render(window.spy.knowings,
                                                            False, (225, 227, 3)), (800, 550))
                        else:
                            if rd(0, 1) == 0:
                                comixes[7].cur_frame = -1
                                comixes[7].change()
                                com_counter = 0
                                comixes[7].update_pos((0, 0))
                                places[codes[cur_place]][-1][places[codes[cur_place]][-1].index(window.spy)].remove(
                                    (10000, 10000))
                                window.update_pos((10000, 10000))
                            else:
                                if rd(0, 1) == 1:
                                    if window.spy.bad:
                                        comixes[5].cur_frame = -1
                                        comixes[5].change()
                                        com_counter = 0
                                        comixes[5].update_pos((0, 0))
                                        win = True
                                        flag = True
                                    else:
                                        comixes[4].cur_frame = -1
                                        comixes[4].change()
                                        com_counter = 0
                                        comixes[4].update_pos((0, 0))
                                        sp_text = str(bad_info[rd(0, len(bad_info) - 1)])
                                        if places[codes[cur_place]][-1][places[codes[cur_place]][-1].index(window.spy)].knowings == '':
                                            places[codes[cur_place]][-1][
                                                places[codes[cur_place]][-1].index(window.spy)].knowings = sp_text
                                            window.spy.knowings = sp_text
                                            text_comix = (tx_s.render(sp_text, False, (225, 227, 3)), (800, 550))
                                        else:
                                            text_comix = (tx_s.render(window.spy.knowings,
                                                                    False, (225, 227, 3)), (800, 550))
                                else:
                                    comixes[6].cur_frame = -1
                                    comixes[6].change()
                                    com_counter = 0
                                    comixes[6].update_pos((0, 0))
                                    places[codes[cur_place]][-1][places[codes[cur_place]][-1].index(window.spy)].remove(
                                        (10000, 10000))
                                    window.update_pos((10000, 10000))
                elif res == 3:
                    if window.book_opened is False and window.inventory_opened is False:
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/open.mp3'))
                        window.show_book()
        if window.book_opened:
            texts.append((tx.render('Агент №' + str(window.book.spy.number), False, (0, 0, 0)),
                          (330, 100)))
            texts.append((tx.render('Возраст: ' + str(window.book.spy.age), False, (0, 0, 0)),
                          (350, 450)))
            if window.book.spy.gender == 'M':
                texts.append((tx.render('Пол: Мужской', False, (0, 0, 0)), (350, 550)))
            else:
                texts.append((tx.render('Пол: Женский', False, (0, 0, 0)), (350, 550)))
            texts.append((tx.render("Особые приметы:", False, (0, 0, 0)), (750, 100)))
            if window.book.spy.item_name != '':
                texts.append((tx_s.render('Нужен предмет ' + window.book.spy.item_name, False,
                                        (120, 0, 120)), (710, 180)))
            else:
                texts.append((tx.render('Нет', False, (30, 30, 30)), (710, 180)))
        else:
            texts.append((tx.render("", False, (0, 0, 0)), (330, 100)))
            texts.append((tx.render("", False, (0, 0, 0)), (350, 450)))
            texts.append((tx.render("", False, (0, 0, 0)), (350, 550)))
            texts.append((tx.render("", False, (0, 0, 0)), (750, 100)))
            texts.append((tx.render("", False, (0, 0, 0)), (710, 180)))
        screen.fill((0, 0, 0))
        if cur_place != 'map':
            for el in places[codes[cur_place]][-1]:
                el.update(pygame.mouse.get_pos())
        all_sprites.draw(screen)
        for el in texts:
            screen.blit(el[0], el[1])
        screen.blit(level[0], level[1])
        screen.blit(easy_level_t[0], easy_level_t[1])
        screen.blit(medium_level_t[0], medium_level_t[1])
        screen.blit(hard_level_t[0], hard_level_t[1])
        screen.blit(text_news[0], text_news[1])
        screen.blit(text_end[0], text_end[1])
        screen.blit(spyes[0], spyes[1])
        screen.blit(secs[0], secs[1])
        if opened_flag:
            screen.blit(text_comix[0], (520, 250))
        com_counter += 1

        if com_counter % 26 == 15:
            if bad_comix.cur_frame < len(bad_comix.frames) - 1:
                bad_comix.change()
            if good_comix.cur_frame < len(good_comix.frames) - 1:
                good_comix.change()
            for el in comixes:
                if el.cur_frame < len(el.frames) - 1:
                    el.change()
                else:
                    if el.rect.x == 0:
                        opened_flag = True
        if com_counter % 30 == 0:
            bat.update()
        clock.tick(30)
        pygame.display.flip()
