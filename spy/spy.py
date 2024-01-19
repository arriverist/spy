import pygame
import os
import sys
from random import randint as rd


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Move_sp(pygame.sprite.Sprite):
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def check_pos(self, pos):
        print(__class__.__name__)


class Dialog(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def update_pos(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]


class Dress_code(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def update(self):
        if self.cur_frame % 2 == 0:
            self.cur_frame = self.cur_frame + 1
        else:
            self.cur_frame = self.cur_frame - 1
        self.image = self.frames[self.cur_frame]

    def check_pos(self, pos):
        return self.rect.x + 42 <= pos[0] <= self.rect.x + 140 and self.rect.y + 54 <= pos[1] <= self.rect.y + 161


class Face(Move_sp):
    def __init__(self, sheet, columns, rows, x, y, i):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = i
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def update(self):
        if self.cur_frame % 2 == 0:
            self.cur_frame = self.cur_frame + 1
        else:
            self.cur_frame = self.cur_frame - 1
        self.image = self.frames[self.cur_frame]

    def check_pos(self, pos):
        return self.rect.x + 20 <= pos[0] <= self.rect.x + 100 and self.rect.y <= pos[1] <= self.rect.y + 140


class Eyes(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.up = 0

    def update(self):
        if self.up % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.up += 1


class Nose(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.up = 0

    def update(self):
        if self.up % 3 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        self.up += 1


class Teeth(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = rd(0, 4)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Hat(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = rd(0, 4)
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def check_pos(self, pos):
        return self.rect.x <= pos[0] <= self.rect.x + 120 and self.rect.y <= pos[1] <= self.rect.y + 55


class Book(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(10000, 10000)

    def update_pos(self, position):
        if position == (150, 25):
            self.posit = True
        else:
            self.posit = False
        self.rect.x = position[0]
        self.rect.y = position[1]


class back(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(10, 46)


class Window(Move_sp):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(10000, 10000)
        self.b = Book(load_image('book.png'), 1, 1, 300, 300)
        self.book = False
        self.posit = False

    def update_pos(self, position):
        if position == (400, 260):
            self.posit = True
        else:
            self.posit = False
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update_spy(self, spy):
        self.spy = spy

    def show_book(self):
        self.book = True
        self.b.update_pos((150, 25))

    def close_book(self):
        self.book = False
        self.b.update_pos((10000, 10000))

    def is_clicked(self, pos):
        x, y = pos[0], pos[1]
        if self.posit:
            if self.rect.x + 64 <= x <= self.rect.x + 148 and self.rect.y + 46 <= y <= self.rect.y + 133:
                return 1
            elif self.rect.x + 160 <= x <= self.rect.x + 244 and self.rect.y + 48 <= y <= self.rect.y + 134:
                return 2
            elif self.rect.x + 264 <= x <= self.rect.x + 347 and self.rect.y + 48 <= y <= self.rect.y + 134:
                return 3
            elif self.rect.x + 371 <= x <= self.rect.x + 456 and self.rect.y + 46 <= y <= self.rect.y + 133:
                return 4
        return 0


class Spy(Move_sp):
    head_forms = ['Head_forms.png', 'Head_forms_darker.png', 'Head_forms_white.png', 'Head_forms_yellow.png']
    eyes = ['eyes_elbrow_up.png', 'eyes_elbrow_up_blue.png', 'eyes_elbrow_up_purple.png', 'eyes_elbrow_up_red.png',
            'eyes_elbrow_up_red_pain.png', 'Plain_point_eyes.png', 'Bad_eyes.png']
    nose = ['Nose.png', 'Nose1.png', 'Nose2.png']
    leeps = ['teeths1.png', 'lips_blue.png', 'lips_dark_dark_red.png', 'lips_red.png', 'lips_green.png', 'lips_dark_red.png']
    dress = ['Coat1.png', 'Dress.png']

    def __init__(self, sheet, columns, rows, x, y, i):
        super().__init__(all_sprites)
        x = x * 1000 + 50
        y = rd(300, 500)
        print(x, y)
        self.dress = Dress_code(load_image(Spy.dress[rd(0, 1)]), 1, 1, 1, 1)
        self.dress.rect.x = x - 68
        self.dress.rect.y = y - 46 + rd(-5, 5)
        self.teeth = Teeth(load_image(Spy.leeps[rd(0, 5)]), 1, 5, 1, 1)
        self.teeth.rect.x = x
        self.teeth.rect.y = y
        self.angry = rd(0, 10)
        self.power = rd(0, 10)
        self.place = ''
        self.up = rd(0, 5)
        self.clever = rd(0, 10)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if i in [3, 11, 13, 1]:
            self.face = Face(load_image(Spy.head_forms[rd(0, 3)]), 4, 4, self.rect.x - 42, self.rect.y - 60, i)
            self.hat = Hat(load_image('Hat.png'), 1, 5, self.rect.x - 38, self.rect.y - 85)
            self.eye = Eyes(load_image(Spy.eyes[rd(0, 6)]), 2, 2, self.rect.x - 22, self.rect.y - 55)
            self.nose = Nose(load_image(Spy.nose[rd(0, 2)]), 2, 2, self.rect.x + 5, self.rect.y - 30)
        elif i in [2, 10, 12, 0]:
            self.face = Face(load_image(Spy.head_forms[rd(0, 3)]), 4, 4, self.rect.x - 42, self.rect.y - 63, i)
            self.hat = Hat(load_image('Hat.png'), 1, 5, self.rect.x - 38, self.rect.y - 85)
            self.eye = Eyes(load_image(Spy.eyes[rd(0, 6)]), 2, 2, self.rect.x - 22, self.rect.y - 55)
            self.nose = Nose(load_image(Spy.nose[rd(0, 2)]), 2, 2, self.rect.x + 5, self.rect.y - 30)
        elif i in [5, 7]:
            self.face = Face(load_image(Spy.head_forms[rd(0, 3)]), 4, 4, self.rect.x - 42, self.rect.y - 70, i)
            self.hat = Hat(load_image('Hat.png'), 1, 5, self.rect.x - 38, self.rect.y - 85)
            self.eye = Eyes(load_image(Spy.eyes[rd(0, 6)]), 2, 2, self.rect.x - 22, self.rect.y - 55)
            self.nose = Nose(load_image(Spy.nose[rd(0, 2)]), 2, 2, self.rect.x + 5, self.rect.y - 30)
        elif i in [4, 6]:
            self.face = Face(load_image(Spy.head_forms[rd(0, 3)]), 4, 4, self.rect.x - 42, self.rect.y - 73, i)
            self.hat = Hat(load_image('Hat.png'), 1, 5, self.rect.x - 38, self.rect.y - 85)
            self.eye = Eyes(load_image(Spy.eyes[rd(0, 6)]), 2, 2, self.rect.x - 22, self.rect.y - 55)
            self.nose = Nose(load_image(Spy.nose[rd(0, 2)]), 2, 2, self.rect.x + 5, self.rect.y - 30)
        elif i in [9, 15]:
            self.face = Face(load_image(Spy.head_forms[rd(0, 3)]), 4, 4, self.rect.x - 42, self.rect.y - 80, i)
            self.hat = Hat(load_image('Hat.png'), 1, 5, self.rect.x - 38, self.rect.y - 85)
            self.eye = Eyes(load_image(Spy.eyes[rd(0, 6)]), 2, 2, self.rect.x - 22, self.rect.y - 55)
            self.nose = Nose(load_image(Spy.nose[rd(0, 2)]), 2, 2, self.rect.x + 5, self.rect.y - 30)
        elif i in [8, 14]:
            self.face = Face(load_image(Spy.head_forms[rd(0, 3)]),4, 4, self.rect.x - 42, self.rect.y - 83, i)
            self.hat = Hat(load_image('Hat.png'), 1, 5, self.rect.x - 38, self.rect.y - 95)
            self.eye = Eyes(load_image(Spy.eyes[rd(0, 6)]), 2, 2, self.rect.x - 22, self.rect.y - 65)
            self.nose = Nose(load_image(Spy.nose[rd(0, 2)]), 2, 2, self.rect.x + 5, self.rect.y - 30)
        self.dialog = Dialog(load_image("Dialog_big.png"), 3, 5, 15, 10)

    def update(self, pos):
        pos1 = (self.rect.x + 22, self.rect.y + 9)
        self.eye.update()
        if self.up % 6 == 0:
            self.teeth.update()
        if self.check_pos(pos):
            self.dialog.update_pos((self.rect.x + 40, self.rect.y - 20))
            self.dialog.update()
        else:
            self.dialog.update_pos((10000, 10000))
        self.up += 1

    def check_pos(self, pos):
        return self.dress.check_pos(pos) or self.face.check_pos(pos) or self.hat.check_pos(pos)


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.music.load('data/music0.mp3')
    pygame.mixer.music.play()
    width, height = 1300, 700
    size = width, height
    all_sprites = pygame.sprite.Group()
    back = back(load_image('London_underground.jpg'), 1, 1, 0, 0)
    spy = [Spy(load_image('base.png'), 2, 2, i % 2, i // 2, rd(0, 15)) for i in range(4)]
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    running = True
    tx = pygame.font.Font('C:/NEIRO/data_boom/data/SlackCasual-Bold-Cyr.ttf', 60)
    text2 = tx.render("", False,
                      (0, 0, 0))
    window = Window(load_image('window.png'), 1, 1, 300, 300)
    window.update_pos((10000, 10000))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    count = 0
                    for i in range(len(spy)):
                        count += 1
                        if spy[i].check_pos(pygame.mouse.get_pos()):
                            if not window.posit:
                                window.update_spy(spy[i])
                                pygame.mixer.Channel(2).play(pygame.mixer.Sound('data/open.mp3'))
                                window.update_pos((400, 260))
                            break
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/button.mp3'))
                    window.close_book()
            if event.type == pygame.MOUSEBUTTONDOWN:
                res = window.is_clicked(pygame.mouse.get_pos())
                if res != 0:
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/button.mp3'))
                if res == 4:
                    window.update_pos((10000, 10000))
                elif res == 3:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('data/open.mp3'))
                    window.show_book()
        if window.book:
            text2 = tx.render("шпиён", False, (0, 0, 0))
        else:
            text2 = tx.render("", False, (0, 0, 0))
        screen.fill((0, 0, 0))
        for i in range(4):
            spy[i].update(pygame.mouse.get_pos())
        all_sprites.draw(screen)
        screen.blit(text2, (700, 300))
        clock.tick(30)
        pygame.display.flip()
