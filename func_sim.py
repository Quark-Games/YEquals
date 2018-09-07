import pygame
from pygame.locals import *
from math import *
import os
import re

os.chdir("assets")

pygame.init()

display_width = 1000
display_height = 720

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Function Simulator")
icon_img = pygame.image.load("icon.png")
pygame.display.set_icon(icon_img)

clock = pygame.time.Clock()
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

MODIFIERS = ("alt", "ctrl", "escape", "meta", "shift", "tab", "windows")
ACC = 10

font = pygame.font.Font(None, 20)


class File:

    def __init__(self, fname):
        self.fname = fname

    def get(self):
        try:
            with open(self.fname, 'r') as f:
                cont = f.read()
            return cont
        except FileNotFoundError:
            return ''

    def put(self, cont):
        with open(self.fname, 'w') as f:
            f.write(str(cont))


class Message:

    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def put(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


class Coordinate:

    def __init__(self):
        self.origin = [display_width / 2, display_height / 2]
        self.scale = 50

    def p2f(px, py):
        fx, fy = 0, 0
        return fx, fy

    def f2p(fx, fy):
        px, py = 0, 0
        return px, py

    def axis(self):
        pygame.draw.line(display,
                         RED,
                         (0, self.origin[1]),
                         (display_width, self.origin[1]))
        pygame.draw.line(display,
                         RED,
                         (self.origin[0], 0),
                         (self.origin[0], display_height))

    def chori(self, move_x, move_y):
        self.origin[0] += move_x
        self.origin[1] += move_y


file = File("data")
message = Message()
coor = Coordinate()


def main():
    func = file.get()
    holding = set()

    while True:

        # keyboard controls
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_all(func)
            if event.type == KEYDOWN:
                # holding down the modifier keys
                key_name = pygame.key.name(event.key)
                for modifier in MODIFIERS:
                    if modifier in key_name:
                        holding.add(modifier)
                        break
                else:
                    # special operations
                    if "meta" in holding:
                        if event.key == K_q:
                            quit_all(func)
                        elif event.key == K_MINUS:
                            coor.scale /= 2
                        elif event.key == K_EQUALS:
                            coor.scale *= 2
                        elif event.key == K_BACKSPACE:
                            func = ""
                    elif "shift" in holding:
                        if event.key == K_6:
                            func += '**'
                        elif event.key == K_8:
                            func += '*'
                        elif event.key == K_9:
                            func += '('
                        elif event.key == K_0:
                            func += ')'
                        elif event.key == K_EQUALS:
                            func += '+'
                    elif event.key == K_BACKSPACE:
                        if func:
                            func = func[:-1]
                    elif event.key == K_SPACE:
                        func += ' '
                    else:
                        func += key_name
            if event.type == KEYUP:
                # releasing the modifier keys
                key_name = pygame.key.name(event.key)
                for modifier in MODIFIERS:
                    if modifier in key_name:
                        holding.remove(modifier)
                        break
                else:
                    pass

        # mouse control
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mouse_press[0]:
            coor.chori(*pygame.mouse.get_rel())
        else:
            pygame.mouse.get_rel() # reset mouse release position
            focus_x = mouse_pos[0]

        # display
        display.fill(WHITE)

        bitmap = font.render("y = " + func, True, BLACK)
        display.blit(bitmap, (10, 10))

        coor.axis()

        # draw graph of function
        old_pos = (-1, -1)
        drawability = display_width
        # domain = [x / ACC for x in range(0, display_width * ACC)]
        for pixel_x in range(0, display_width):
            try:
                x = (pixel_x - display_width / 2) / coor.scale
                y = eval(func)
                pixel_y = display_height / 2 - y * coor.scale
                temp = 0 < old_pos[1] < display_height
                temp = temp or 0 < pixel_y < display_height
                if pixel_x - old_pos[0] <= 1 and temp:
                    pygame.draw.line(display,
                                     BLACK,
                                     old_pos,
                                     (int(pixel_x), int(pixel_y)))
                old_pos = (int(pixel_x), int(pixel_y))
            except Exception:
                drawability -= 1

        # display drawability message
        if not drawability:
            bitmap = font.render("this function not drawable", True, BLACK)
            display.blit(bitmap, (10, 30))
        elif drawability != display_width:
            bitmap = font.render("this function not consistant", True, BLACK)
            display.blit(bitmap, (10, 30))

        # show focus point location

        pygame.display.flip()

        clock.tick(FPS)


def quit_all(data):
    file.put(data)
    pygame.quit()
    quit()


def error():
    quit_all('')


main()
