import os
import sys

import bcrypt
import pygame

MAX_LEVEL = 10

mixer1 = pygame.mixer
mixer2 = pygame.mixer


def save_level(level):
    with open('data/save_level.txt', 'wb+') as file:
        file.write(hash_level_number(level))


def hash_level_number(level_number):
    password = bytes(str(level_number), encoding='utf8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password, salt)

    return hashed


def unhash_level_number(level_number_hash):
    for i in range(1, MAX_LEVEL + 1):
        if bcrypt.checkpw(bytes(str(i), encoding='utf8'), level_number_hash):
            return i
    return 1


def load_music():
    mixer1.music.load('data/sounds/gameplay.mp3')
    mixer1.music.play(-1)


def start_game(velocity):
    global grass_y
    screen.fill(pygame.Color("#4d85d0"))
    screen.blit(fon, (0, grass_y))
    grass_y -= velocity * clock.tick() / 1000
    pygame.display.flip()


def game_won():
    global isAllGameWon, gameover_sprite
    isAllGameWon = True
    gameover_sprite = pygame.sprite.Sprite()
    gameover_sprite.image = pygame.transform.scale(load_image("gameover.png"), size)
    gameover_sprite.rect = gameover_sprite.image.get_rect()
    gameover_sprite.rect.x, gameover_sprite.rect.y = -list(gameover_sprite.image.get_rect())[2], 0
    all_sprites.add(gameover_sprite)


def start_screen():
    fon1 = pygame.transform.scale(load_image('cover.jpg'), size)
    fon2 = pygame.transform.scale(load_image('cover2.jpg'), size)
    fon = fon1
    easter = False
    screen.blit(fon1, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
                x, y = event.pos
                arrow_sprite.rect.x = x
                arrow_sprite.rect.y = y
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                try:
                    if event.key == pygame.K_f:
                        if easter:
                            fon = fon1
                            easter = False
                        else:
                            fon = fon2
                            effect = pygame.mixer.Sound('data/sounds/egg.wav')
                            effect.play()
                            easter = True
                    else:
                        return
                except:
                    return

        screen.blit(fon, (0, 0))
        arrow_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def load_image(name, way='data', colorkey=None):
    fullname = os.path.join(way, name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
        pass

    return image


def load_level(filename):
    global level_map, objects
    objects = []
    filename = 'data/levels/' + filename + ('.txt' if not filename.endswith('.txt') else '')
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    for j, line in enumerate(level_map):
        for i, obj in enumerate(level_map[j]):
            if obj == '#':
                objects.append(Object(all_sprites, cell_size * i, cell_size * j,
                                      True, 'mole.png',
                                      def_image_name='mole_hungry.png'))
            elif obj == 'a':
                objects.append(Object(all_sprites, cell_size * i, cell_size * j,
                                      False, 'apple.png',
                                      def_image_name='apple_eaten.png'))
            elif obj == 'c':
                objects.append(Object(all_sprites, cell_size * i, cell_size * j,
                                      False, 'carrot.png',
                                      def_image_name='carrot_eaten.png'))
            elif obj == 'l':
                objects.append(Object(all_sprites, cell_size * i, cell_size * j,
                                      False, 'lemon.png',
                                      def_image_name='lemon_eaten.png'))
            elif obj == 'r':
                objects.append(Object(all_sprites, cell_size * i, cell_size * j,
                                      False, 'radish.png',
                                      def_image_name='radish_eaten.png'))
            elif obj == 's':
                objects.append(Object(all_sprites, cell_size * i, cell_size * j,
                                      False, 'strawberry.png',
                                      def_image_name='strawberry_eaten.png'))


def delete_level():
    try:
        for obj in objects:
            obj.kill()
    except NameError:
        pass


def next_level():
    global level
    level += 1
    save_level(level)
    if level > MAX_LEVEL:
        game_won()
    else:
        delete_level()
        load_level(f'level{level}.txt')


def terminate():
    pygame.quit()
    sys.exit()


def new_coords(coords):
    try:
        if abs(coords[0][0] - coords[1][0]) >= W // 1.5 or \
                abs(coords[0][1] - coords[1][1]) >= H // 1.5:
            x_0, y_0 = coords[1]
            x_1, y_1 = coords[2]
        else:
            x_0, y_0 = coords[0]
            x_1, y_1 = coords[1]
        x_n, y_n = coords[-1]
        px = x_n + x_1 - x_0
        py = y_n + y_1 - y_0
        if coords[-1][0] > W:
            px = 0
        if coords[-1][0] < 0:
            px = W
        if coords[-1][1] > H:
            py = 0
        if coords[-1][1] < 0:
            py = H

        coords = coords[1:] + [[px, py]]

        return coords
    except IndexError:
        return coords


class Object(pygame.sprite.Sprite):
    def __init__(self, group, x, y, isObstacle, image_name, def_image_name=None):
        super().__init__(group)
        # print(x, y)
        self.cs = mole_size if isObstacle else fruit_size
        self.scs = mole_size if isObstacle else fruit_size
        self.x = x
        self.y = y
        self.isObstacle = isObstacle
        self.defeated = False
        self.image_name = image_name
        self.def_image_name = def_image_name
        self.image = pygame.transform.scale(load_image('characters/' + image_name),
                                            (self.cs, self.cs))
        self.mask = pygame.mask.from_surface(self.image)
        # if not isObstacle:
        #     self.def_image = load_image('data/characters/' + def_image_name)
        self.rect = pygame.Rect(x - self.cs // 2, y - self.cs // 2, x, y)
        self.srect = pygame.Rect(x - self.cs // 2, y - self.cs // 2, x, y)
        # print(self.rect)

    def update(self, *args):
        super().update(self, args)
        if self.defeated:
            if not self.isObstacle and self.cs < 200:
                self.cs += step * 2
                self.rect = pygame.Rect(self.rect[0] - step, self.rect[1] - step,
                                        self.rect[2] + step, self.rect[3] + step)
            elif self.cs >= 200:
                self.rect = pygame.Rect(-W, -W,
                                        -W, -W)
            self.image = pygame.transform.scale(load_image('characters/' + self.def_image_name),
                                                (self.cs, self.cs))

        else:
            self.cs = self.scs
            self.rect = self.srect
            self.image = pygame.transform.scale(load_image('characters/' + self.image_name),
                                                (self.cs, self.cs))


class MainObject(pygame.sprite.Sprite):
    def __init__(self, group, *move, image_name):
        super().__init__(group)
        if type(move) is not list:
            move = [move]
        else:
            move = move[0]
        self.move = [_ for _ in move]
        self.len = len(self.move)

        self.image = pygame.transform.scale(load_image('characters/' + image_name),
                                            (cell_size, cell_size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(-cell_size * 100, -cell_size * 100, 0, 0)

    def update(self, *args):
        super().update(self, args)
        # self.image = pygame.transform.flip(self.image, True, False)
        try:
            self.rect = pygame.Rect(self.move[-1][0] - cell_size // 2,
                                    self.move[-1][1] - cell_size // 2,
                                    self.move[-1][0],
                                    self.move[-1][1])
        except IndexError:
            pass
        if not isMainObjectCreation and not isGameLost and not isGameWon:
            self.go()
        elif isGameLost:
            self.rect = pygame.Rect(-cell_size * 100, -cell_size * 100, 0, 0)

    def go(self):
        try:
            if not self.move[0]:
                return
        except IndexError:
            return
        self.len = len(self.move)
        self.move = new_coords(self.move)

    def erase(self):
        self.move = self.move[1:]

    def append(self, coord):
        self.move.append(coord)

    def clear(self):
        self.move = []

    def __len__(self):
        try:
            return len(self.move)
        except TypeError:
            return 0

    def __str__(self):
        return str(self.move)


pygame.init()
pygame.mouse.set_visible(False)

load_music()

# size = W, H = pygame.display.Info().current_w, pygame.display.Info().current_h
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

size = W, H = 1200, 675
screen = pygame.display.set_mode((W, H))

fon = pygame.transform.scale(load_image('grass.jpg'), (W, H))
grass_y = H + 1

clock = pygame.time.Clock()
fps = 60

step = 5
cell_size = 20
mole_size = 40
fruit_size = 40

thickness = int(cell_size / 4.67)

main_object_color = pygame.Color('#a23b34')

all_sprites = pygame.sprite.Group()

try:
    with open('data/save_level.txt', 'rb') as file:
        level = unhash_level_number(file.read()) - 1
except FileNotFoundError:
    level = 0

next_level()

# Загрузка кастомного курсора

arrow_sprites = pygame.sprite.Group()
arrow_sprite = pygame.sprite.Sprite()
arrow_sprite.image = load_image("characters/arrow2.png")
arrow_sprite.rect = arrow_sprite.image.get_rect()
arrow_sprites.add(arrow_sprite)

start_screen()
while grass_y > 0:
    start_game(H // 2)

running = True
isMainObjectCreation = isGameLost = isGameLostF = isGameWon = isAllGameWon = False
main_object = MainObject(all_sprites, image_name='snake.png')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not isGameLost and not isGameWon:
                main_object.clear()
                main_object.append(list(event.pos))
                isMainObjectCreation = True
                for i in objects:
                    i.defeated = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            isMainObjectCreation = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if not isMainObjectCreation:
                next_level()

        if event.type == pygame.MOUSEMOTION and pygame.mouse.get_focused():
            x, y = event.pos
            arrow_sprite.rect.x = x
            arrow_sprite.rect.y = y

        if event.type == pygame.MOUSEMOTION:
            if isMainObjectCreation:
                main_object.append(list(event.pos))

    for i in objects:
        try:
            x1, y1 = main_object.move[-1]
            if pygame.sprite.collide_mask(i, main_object):
                i.defeated = True
                if i.isObstacle:
                    effect = pygame.mixer.Sound('data/sounds/death.wav')
                    effect.play()
                else:
                    effect = pygame.mixer.Sound('data/sounds/nom.wav')
                    effect.play()
        except:
            pass
    try:
        for i in range(0, len(main_object) - 1, 1):
            from_coord = main_object.move[i]
            to_coord = main_object.move[i + 1]
            if abs(from_coord[0] - to_coord[0]) > W // 2 or abs(from_coord[1] - to_coord[1]) > H:
                continue
            if from_coord[0] and to_coord[0]:
                pygame.draw.line(screen, main_object_color,
                                 from_coord, to_coord, thickness)
            # if i == 0:
            #     pygame.draw.circle(screen, main_object_color, from_coord, 8)
            # elif i == len(main_object) - 2:
            #     pygame.draw.circle(screen, main_object_color, from_coord, 8)
        all_sprites.draw(screen)
    except IndexError:
        pass

    if any([_.defeated for _ in objects]) and isMainObjectCreation:
        isMainObjectCreation = False
    elif any([_.defeated and _.isObstacle for _ in objects]):
        isGameLost = isGameLostF = True
    elif all([_.defeated != _.isObstacle for _ in objects]):
        isGameWon = True

    if isGameLost:
        main_object.erase()
        if not main_object:
            isGameLost = False
            if isGameLostF:
                for obj in objects:
                    if obj.defeated and not obj.isObstacle:
                        obj.defeated = False
                print('-')
            isGameLostF = False

    elif isGameWon:
        main_object.erase()
        if not main_object:
            isGameWon = False
            print('+')
            next_level()
    elif isAllGameWon:
        if gameover_sprite.rect.x != 0:
            gameover_sprite.rect.x += 1

    pygame.display.flip()
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    arrow_sprites.draw(screen)
    all_sprites.update()

    clock.tick(fps)

pygame.quit()
