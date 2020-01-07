import pygame


def new_coords(coords):
    if abs(coords[0][0] - coords[1][0]) >= H // 1.2 or abs(coords[0][1] - coords[1][1]) >= W // 1.2:
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
    print(coords)

    return coords


class MainObject:
    def __init__(self, *move):
        if type(move) is not list:
            move = [move]
        else:
            move = move[0]
        self.move = [_ for _ in move]
        # self.speed = 10

    def go(self):
        if not self.move[0]:
            return
        self.len = len(self.move)
        self.move = new_coords(self.move)

    def append(self, coord):
        self.move.append(coord)

    def clear(self):
        self.move = []

    def __len__(self):
        return len(self.move)

    def __str__(self):
        return str(self.move)


pygame.init()
size = W, H = 500, 500
# size = W, H = pygame.display.Info().current_w, pygame.display.Info().current_h
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
fps = 100

step = 1

main_object_color = pygame.Color('black')

running = True
isMainObjectCreation = False
main_object = MainObject()

while running:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYUP and event.key == 27:
            screen = pygame.display.set_mode((500, 500))
            W = H = 500

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            main_object.clear()
            main_object.append(list(event.pos))
            isMainObjectCreation = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            main_object.append(list(event.pos))
            isMainObjectCreation = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            main_object.clear()
            main_object.append(None)

        if event.type == pygame.MOUSEMOTION:
            if isMainObjectCreation:
                main_object.append(list(event.pos))

    for i in range(0, len(main_object) - 1, step):
        from_coord = main_object.move[i]
        to_coord = main_object.move[i + 1]
        if abs(from_coord[0] - to_coord[0]) > H // 2 or abs(from_coord[1] - to_coord[1]) > W:
            continue
        if from_coord[0] and to_coord[0]:
            pygame.draw.line(screen, main_object_color,
                             from_coord, to_coord, 4)
    if not isMainObjectCreation:
        main_object.go()

    clock.tick(fps)
    # print(*[_ for _ in main_object.move])

    pygame.display.flip()
    pygame.display.set_caption("fps: " + str(clock.get_fps()))

pygame.quit()
