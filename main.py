import pygame
import random
import sys
import os


# Функция выхода из меню:


def terminate():
    pygame.quit()
    sys.exit()


# Функция распаковки уровня(На вход принимает имя файла с уровнем):


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# Функция зыгрузки изображения(На вход принимает имя файла в папке data):


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert_alpha()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# Функция генирации уровня(На вход принимает преобразованый список из файла):


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.' or level[y][x] == '@' or level[y][x] == '$':
                Water(x, y)
                MAP.board[y][x] = ['#']
            elif level[y][x] == '#':
                Land(x, y)
            elif level[y][x] == '%':
                Grass(x, y)
            if level[y][x] == '@':
                MAP.board[y][x] = []
                a = Boardred(x, y)
                pos_of_boards['red_board'] = [x, y]
                for _ in range(3):
                    p = Piratred(x, y)
                    p.pos()
            if level[y][x] == '$':
                MAP.board[y][x] = []
                b = Boardblue(x, y)
                pos_of_boards['blue_board'] = [x, y]
                for _ in range(3):
                    p = Piratblue(x, y)
                    p.pos()
    return x, y, a, b


#


def has_board(x, y):
    for i in pos_of_boards:
        if list(pos_of_boards[i]) == [x, y]:
            return True, i
    return False, 'not'


#


def ee(x, y, name):
    FT, bn = has_board(x, y)
    if FT and ((bn == 'red_board' and name == 'Piratblue') or ((bn == 'blue_board' and name == 'Piratred'))):
        return False
    return True


def count(pos_x, pos_y, a):
    if a != 0:
        font = pygame.font.Font(None, 17)
        text = font.render(f"{a}", True, pygame.Color('black'))
        screen.blit(text, (209 + (pos_x * title_width), 5 + pos_y * title_height))


def account():
    font = pygame.font.Font(None, 40)
    text = font.render(f": {play.coints['red']}", True, pygame.Color('white'))
    screen.blit(text, (45, 85))
    font = pygame.font.Font(None, 40)
    text = font.render(f": {play.coints['blue']}", True, pygame.Color('white'))
    screen.blit(text, (895, 85))



# Класс для получения координаты клетки поля по клику(на вход получает ширину и длину поля):


class Map:

    # Инициализатор класса(ширина и высота поля в пикселях):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[[] for _ in range(width)] for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 50

    # Определение координаты клетки поля:

    def get_cell(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (x not in range(self.left + 200, self.left + self.width * self.cell_size + 200)) or\
                (y not in range(self.top, self.top + self.height * self.cell_size)):
            return None
        else:
            a = int((x - self.left - 200) / self.cell_size)
            b = int((y - self.top) / self.cell_size)
            return a, b

    # Реакция на нажатие мыши(координаты мыши в пикселях, возвращает координаты клетки поля):

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        return cell


# Класс курсора мыши:

class Cursor(pygame.sprite.Sprite):

    # Инициализатор класса(на вход принимает группу спрайтов для курсора):

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(title_images['arrow'], (25, 25))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(size[0])
        self.rect.y = random.randrange(size[1])

    # Отвечает за перемещение нарисованной мыши вместе с курсором(На вход принимает координаты курсора):

    def update(self, *args):
        if args:
            self.rect.x = args[0].pos[0]
            self.rect.y = args[0].pos[1]


# Класс клетки воды (При инициализации принимает координаты клетки):

class Water(pygame.sprite.Sprite):

    # Инициализатор класса (на вход принимает координаты клетки поля):
    def __init__(self, pos_x, pos_y):
        super().__init__(water_group)
        self.image = title_images['water']
        self.rect = self.image.get_rect().move(title_width * pos_x + 200, title_height * pos_y)


# Класс клетки острова(При инициализации принимает тип поля при переворачивании клетки и координаты клетки:

class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(cell_group)

    def update(self):
        pass


class Land(Cell):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = title_images['land']
        self.rect = self.image.get_rect().move(title_width * pos_x + 200, title_height * pos_y)
        pole_play[(pos_x, pos_y)] = self
        self.open = True


class Grass(Cell):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(title_images['grass'], (50, 50))
        self.rect = self.image.get_rect().move(title_width * pos_x + 200, title_height * pos_y)
        pole_play[(pos_x, pos_y)] = self
        self.open = False

    def open_cell(self, pos_x, pos_y):
        name = random.choice(pole)
        Pole(pos_x, pos_y, name)
        pole.remove(name)
        self.open = True


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coins_group)
        self.image = pygame.transform.scale(title_images['coin'], (70, 70))
        self.rect = self.image.get_rect().move(title_width * pos_x + 200, title_height * pos_y)
        pos_of_coints[pos_y][pos_x] += 1
        coins_pos[(pos_x, pos_y)] = self


# Класс Пиратского коробля(Красный):

class Board(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, name):
        super().__init__(group)
        a = 90
        self.play = ''
        if name == 'blue_board':
            self.play = 'blue'
        else:
            self.play = 'red'
        if name == 'blue_board':
            a = -90
        self.image = pygame.transform.rotate(title_images[name], angle=a)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            title_width * self.pos_x + 200, title_height * self.pos_y)

    def update(self, pos, a):
        x = pos[0]
        y = pos[1]
        delta = [(0, -1), (0, 1)]
        for dx, dy in delta:
            if pos == (self.pos_x + dx, self.pos_y + dy) and MAP.board[y][x + a] != ['#'] and\
                    MAP.board[self.pos_y][self.pos_x] != [] and self.play == play.player:
                a, b = self.pos_x, self.pos_y
                MAP.board[y][x] = []
                while MAP.board[self.pos_y][self.pos_x] != []:
                    MAP.board[self.pos_y][self.pos_x][0].update(pos, krot=False)
                MAP.board[b][a] = ['#']
                self.pos_x, self.pos_y = x, y
                self.rect = self.image.get_rect().move(
                    title_width * self.pos_x + 200, title_height * self.pos_y)
                if a == 1:
                    pos_of_boards['red_board'] = [self.pos_x, self.pos_y]
                else:
                    pos_of_boards['blue_board'] = [self.pos_x, self.pos_y]
                play.play()


class Boardred(Board):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, board_group_red, 'red_board')


# Класс Пиратского коробля(Синий):

class Boardblue(Board):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, board_group_blue, 'blue_board')


class Pirat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, name):
        super().__init__(group)
        self.play = ''
        if name == 'blue_pirat':
            self.play = 'blue'
        else:
            self.play = 'red'
        self.image = pygame.transform.scale(title_images[name], (70, 70))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.group = group
        self.rect = self.image.get_rect().move(
            title_width * self.pos_x + 20, title_height * self.pos_y - 20)
        MAP.board[self.pos_y][self.pos_x].append(self)

    def update(self, pos, krot=True):
        x = pos[0]
        y = pos[1]
        delta = [(0, -1), (0, 1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in delta:
            if pos == (self.pos_x + dx, self.pos_y + dy) and MAP.board[y][x] != ['#'] and\
                    ee(x, y, self.__class__.__name__) and self.play == play.player:
                self.die(x, y)
                MAP.board[y][x] += [MAP.board[self.pos_y][self.pos_x][0]]
                MAP.board[self.pos_y][self.pos_x] = MAP.board[self.pos_y][self.pos_x][1:]
                a, b = self.pos_x, self.pos_y
                self.pos_x, self.pos_y = x, y
                self.rect = self.image.get_rect().move(
                    title_width * self.pos_x + 200, title_height * self.pos_y)
                self.pos()
                if MAP.board[b][a] != []:
                    MAP.board[b][a][0].pos()
                if krot:
                    if money and pole_play[(x, y)].open:
                        pos_of_coints[b][a] -= 1
                        if pos_of_coints[b][a] == 0:
                            coins_group.remove(coins_pos[(a, b)])
                        if has_board(self.pos_x, self.pos_y)[0]:
                            play.coints[play.player] += 1
                        elif pos_of_coints[self.pos_y][self.pos_x] == 0:
                            Coin(self.pos_x, self.pos_y)
                        else:
                            pos_of_coints[self.pos_y][self.pos_x] += 1
                    if not pole_play[(x, y)].open:
                        pole_play[(x, y)].open_cell(x, y)
                    play.play()
                return True
        return False

    def pos(self):
        k = 0
        lot = []
        for i in self.group:
            if i.pos_x == self.pos_x and i.pos_y == self.pos_y:
                k += 1
                if i != self:
                    lot.append(i)
        if k == 1:
            self.rect = self.image.get_rect().move(
                title_width * self.pos_x + 190, title_height * self.pos_y - 10)
        elif k == 2:
            self.rect = self.image.get_rect().move(
                title_width * self.pos_x + 200, title_height * self.pos_y - 10)
            lot[0].rect = self.image.get_rect().move(
                title_width * self.pos_x + 180, title_height * self.pos_y - 10)
        elif k == 3:
            self.rect = self.image.get_rect().move(
                title_width * self.pos_x + 200, title_height * self.pos_y)
            lot[0].rect = self.image.get_rect().move(
                title_width * self.pos_x + 180, title_height * self.pos_y)
            lot[1].rect = self.image.get_rect().move(
                title_width * self.pos_x + 190, title_height * self.pos_y - 20)

    def paint(self):
        return self.rect.x, self.rect.y

    def die(self, x, y):
        lot = []
        for i in MAP.board[y][x]:
            if i.group != MAP.board[self.pos_y][self.pos_x][0].group:
                lot.append(i)
                if i.group == pirat_group_red:
                    i.pos_x, i.pos_y = redboard.pos_x, redboard.pos_y
                else:
                    i.pos_x, i.pos_y = blueboard.pos_x, blueboard.pos_y
                i.rect = i.image.get_rect().move(
                    title_width * i.pos_x, title_height * i.pos_y)
        for j in lot:
            if j.group == pirat_group_red:
                MAP.board[y][x].remove(j)
                MAP.board[redboard.pos_y][redboard.pos_x].append(j)
            else:
                MAP.board[y][x].remove(j)
                MAP.board[blueboard.pos_y][blueboard.pos_x].append(j)
            j.pos()


class Piratblue(Pirat):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, pirat_group_blue, 'blue_pirat')


class Piratred(Pirat):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, pirat_group_red, 'red_pirat')


class Tablo(pygame.sprite.Sprite):
    def __init__(self, a, b):
        super().__init__(tablo_group)
        self.image = pygame.transform.scale(title_images['coin'], (100, 100))
        self.rect = self.image.get_rect().move(a, b)


class Pole(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, name):
        super().__init__(pole_group)
        self.name = name
        self.image = pygame.transform.scale(title_images[self.name], (50, 50))
        self.rect = self.image.get_rect().move(title_width * pos_x + 200, title_height * pos_y)
        if name == 'chest':
            c = Coin(pos_x, pos_y)
            n = random.randint(0, 2)
            for _ in range(n):
                pos_of_coints[pos_y][pos_x] += 1

class Play:
    def __init__(self):
        self.players = ['red', 'blue']
        self.cords = [(0, 0), (850, 0)]
        self.k = random.randint(0, 1)
        self.pos = self.cords[self.k]
        self.pos1 = 1
        if self.k == 1:
            self.pos1 = self.cords[self.k - 1]
        if self.k == 0:
            self.pos1 = self.cords[self.k + 1]
        self.player = self.players[self.k]
        self.coints = {'red': 0, 'blue': 0}

    def play(self):
        self.k = self.k + 1
        if self.k > 1: self.k = 0
        self.pos = self.cords[self.k]
        if self.k == 1:
            self.pos1 = self.cords[self.k - 1]
        if self.k == 0:
            self.pos1 = self.cords[self.k + 1]
        self.player = self.players[self.k]


if __name__ == '__main__':

    # Параметры клетки:

    title_width = title_height = 50

    # Распаковка файла с уровнем:

    map_island = load_level('map.txt')
    map_x, map_y = len(map_island[0]), len(map_island)
    MAP = Map(map_x, map_y)

    # Инициализация пайгейм:

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("The Jackal")
    size = width, heigth = map_x * title_width + 400, map_y * title_height
    screen = pygame.display.set_mode(size)

    # Создание групп спрайтов:

    water_group = pygame.sprite.Group()
    cell_group = pygame.sprite.Group()
    board_group_blue = pygame.sprite.Group()
    board_group_red = pygame.sprite.Group()
    coins_group = pygame.sprite.Group()
    pirat_group_red = pygame.sprite.Group()
    pirat_group_blue = pygame.sprite.Group()
    tablo_group = pygame.sprite.Group()
    pole_group = pygame.sprite.Group()

    # Спрайты:

    title_images = {
        'water': load_image('water2.png'),
        'land': load_image('land3.png'),
        'grass': load_image('grass.png'),
        'red_board': load_image('red_board.png', color_key=-1),
        'blue_board': load_image('blue_board.png', color_key=-1),
        'arrow': load_image('arrow.png'),
        'red_pirat': load_image('red_pirat.png', color_key=-1),
        'blue_pirat': load_image('blue_pirat.png', color_key=-1),
        'coin': load_image('coin.png', color_key=-1),
        'fortress': load_image('fortress.png', color_key=-1),
        'chest': load_image('chest.png', color_key=-1),
        'ice': load_image('ice.png', color_key=-1),
        'rum': load_image('rum.png', color_key=-1),
        'trap': load_image('trap.png', color_key=-1),
        'plain': load_image('plain.png', color_key=-1)
    }

    # Генерация уровня:

    pos_of_boards = {}
    pos_of_coints = [[0 for _ in range(map_x)] for _ in range(map_y)]
    pole = [['plain' for _ in range(7)] * 2 + ['chest' for _ in range(7)] * 2 + ['ice' for _ in range(7)] + \
            ['fortress' for _ in range(7)] + ['trap' for _ in range(7)]]
    pole = pole[0]
    pole_play = {}
    coins_pos = {}
    level_x, level_y, redboard, blueboard = generate_level(map_island)

    # Курсор:

    pygame.mouse.set_visible(False)
    cursor = pygame.sprite.Group()
    Cursor(cursor)
    in_screen = True

    # Табло:

    Tablo(5, 80)
    Tablo(855, 80)

    # Обработчик событий:

    running = True
    play = Play()
    clock = pygame.time.Clock()
    xod = False
    swi = False
    money = False
    color_of_board = ''
    xod_x = 0
    xod_y = 0
    a, b = 0, 0

    while running:
        pos = ()

        # Проверка событий:

        for event in pygame.event.get():

            # Остановка обработчика:

            if event.type == pygame.QUIT:
                running = False

            # Перемещение курсора:

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused():
                    cursor.update(event)
                    in_screen = True
                else:
                    in_screen = False

            #

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL):
                if xod and pos_of_coints[xod_y][xod_x] != 0:
                    money = True

            # Отвечает за ход пиратом:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = MAP.get_click(event.pos)
                if pos != None:
                    swi = False
                    if xod:
                        if MAP.board[xod_y][xod_x][0].update(pos) or\
                                (MAP.board[pos[1]][pos[0]] != [] and MAP.board[pos[1]][pos[0]] != ['#']):
                            xod = False
                            money = False
                    elif MAP.board[pos[1]][pos[0]] != [] and MAP.board[pos[1]][pos[0]] != ['#'] and\
                            MAP.board[pos[1]][pos[0]][0].play == play.player:
                        a, b = MAP.board[pos[1]][pos[0]][0].paint()
                        xod = True
                        xod_x, xod_y = pos[0], pos[1]

            # Отвечает за ход кораблём:

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos = MAP.get_click(event.pos)
                if pos != None:
                    boar, color = has_board(pos[0], pos[1])
                    xod = False
                    if boar:
                        color_of_board = color
                        if color_of_board == 'red_board' and play.player == 'red':
                            a, b = redboard.rect.x, redboard.rect.y
                            swi = True
                        elif color_of_board == 'blue_board' and play.player == 'blue':
                            a, b = blueboard.rect.x, blueboard.rect.y
                            swi = True
                    elif swi:
                        if color_of_board == 'red_board':
                            redboard.update(pos, 1)
                        else:
                            blueboard.update(pos, -1)
                        swi = False

        # Обновление поля и его отрисовка:

        screen.fill(pygame.Color('black'))
        water_group.draw(screen)
        cell_group.draw(screen)
        pole_group.draw(screen)
        board_group_red.draw(screen)
        board_group_blue.draw(screen)
        coins_group.draw(screen)
        pirat_group_red.draw(screen)
        pirat_group_blue.draw(screen)
        tablo_group.draw(screen)
        for i in range(len(pos_of_coints)):
            for j in range(len(pos_of_coints[0])):
                count(j, i, pos_of_coints[i][j])
        account()
        if xod and money:
            pygame.draw.circle(screen, pygame.Color('green'), (a + 34, b + 34), 12, width=1)
        elif xod:
            pygame.draw.circle(screen, pygame.Color('white'), (a + 34, b + 34), 12, width=1)
        if swi:
            pygame.draw.rect(screen, pygame.Color('white'), (a, b, title_width, title_height), width=1)
        pygame.draw.rect(screen, pygame.Color(play.player), (*play.pos, 200, 60))
        pygame.draw.rect(screen, pygame.Color('white'), (*play.pos, 200, 60), width=2)
        pygame.draw.rect(screen, pygame.Color('white'), (*play.pos1, 200, 60), width=2)
        if in_screen:
            cursor.draw(screen)
        pygame.display.flip()
        clock.tick(100)

    # Закрытие приложения:

    pygame.quit()
