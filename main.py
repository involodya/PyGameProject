import os

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def new_coords(coords):
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


class Circle:
    def __init__(self, x, y, r, isObstacle):
        self.isObstacle = isObstacle
        self.x = x
        self.y = y
        self.r = r
        self.defeated = False
        self.color = pygame.Color('blue')
        self.color_def = pygame.Color('green')

    def draw(self, surf):
        if self.defeated:
            pygame.draw.circle(surf, self.color_def, (self.x, self.y), self.r)
        else:
            pygame.draw.circle(surf, self.color, (self.x, self.y), self.r)


class MainObject:
    def __init__(self, *move):
        if type(move) is not list:
            move = [move]
        else:
            move = move[0]
        self.move = [_ for _ in move]
        self.len = len(self.move)

    def go(self):
        if not self.move[0]:
            return
        self.len = len(self.move)
        self.move = new_coords(self.move)

    def erase(self):
        self.move = self.move[1:]
        print(self.move)

    def append(self, coord):
        self.move.append(coord)

    def clear(self):
        self.move = []

    def __len__(self):
        return len(self.move)

    def __str__(self):
        return str(self.move)


pygame.init()
size = W, H = 889, 500
# size = W, H = pygame.display.Info().current_w, pygame.display.Info().current_h
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# fon = pygame.transform.scale(load_image('fon.jpg'), (W, H))

screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 100

step = 1

main_object_color = pygame.Color('#CD5555')

circles = [Circle(100, 100, 20, False), Circle(180, 100, 20, False), Circle(180, 180, 20, False)]
circles.extend([Circle(200, 200, 20, True),
                Circle(280, 200, 20, True), Circle(280, 280, 20, True)])

running = True
isMainObjectCreation = isGameLost = isGameWon = False
main_object = MainObject()

while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP and event.key == 27:
            screen = pygame.display.set_mode((889, 500))
            W = 500
            H = 889

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            main_object.clear()
            main_object.append(list(event.pos))
            isMainObjectCreation = True
            for i in circles:
                i.defeated = False

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            main_object.append(list(event.pos))
            isMainObjectCreation = False
            for i in circles:
                i.defeated = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            main_object.clear()
            main_object.append(None)
            for i in circles:
                i.defeated = False

        if event.type == pygame.MOUSEMOTION:
            if isMainObjectCreation:
                main_object.append(list(event.pos))

    for i in circles:
        try:
            x1, y1 = main_object.move[-1]
            if (i.x - x1) ** 2 + (i.y - y1) ** 2 <= i.r ** 2:
                i.defeated = True
        except:
            pass
        i.draw(screen)

    for i in range(0, len(main_object) - 1, step):
        from_coord = main_object.move[i]
        to_coord = main_object.move[i + 1]
        if abs(from_coord[0] - to_coord[0]) > W // 2 or abs(from_coord[1] - to_coord[1]) > H:
            continue
        if from_coord[0] and to_coord[0]:
            pygame.draw.line(screen, main_object_color,
                             from_coord, to_coord, 4)

    if any([_.defeated and _.isObstacle for _ in circles]):
        isGameLost = True
    elif all([_.defeated and _.defeated != _.isObstacle for _ in circles]):
        isGameWon = True

    if isGameLost:
        main_object.erase()
        if not main_object:
            isGameLost = False
    elif isGameWon:
        pass
    elif not isMainObjectCreation:
        main_object.go()

    clock.tick(fps)

    pygame.display.flip()
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

pygame.quit()
