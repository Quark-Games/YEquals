import pygame
from pygame.locals import *
from math import *
import os
import re

# set default directory to assets
os.chdir("assets")

# pygame display initiation
pygame.init()

display_width = 1000
display_height = 720

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Function Simulator")
icon_img = pygame.image.load("icon.png")
pygame.display.set_icon(icon_img)

clock = pygame.time.Clock()
FPS = 30

font = pygame.font.Font(None, 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

MODIFIERS = ("alt", "ctrl", "escape", "meta", "shift", "tab", "windows")


class File:

    def __init__(self, fname):
        self.fname = fname

    def get(self):
        try:
            with open(self.fname, 'r') as f:
                cont = [s.replace('\n','') for s in f.readlines()]
            return cont
        except FileNotFoundError:
            return ['']

    def put(self, cont):
        with open(self.fname, 'w') as f:
            for each in cont:
                f.write(each + '\n')


class Message:

    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def put(self, screen, textString):
        print(textString)
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
        self.scalex = 50
        self.scaley = 50

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


class Func:
    family = []
    active = None
    _act_index = -1

    def __init__(self, exp):
        self.exp = exp
        self.cursor = len(exp)
        Func.family.append(self)
        Func.set_act(len(Func.family) - 1)

    def set_act(index):
        if index == 'u':
            if Func._act_index > 0:
                Func._act_index -= 1
            Func.active = Func.family[Func._act_index]
        elif index == 'd':
            if Func._act_index < len(Func.family) - 1:
                Func._act_index += 1
            Func.active = Func.family[Func._act_index]
        elif Func.family:
            Func.active = Func.family[index]
            Func._act_index = index

    def remove():
        index = Func.family.index(Func.active)
        Func.family.remove(Func.active)
        Func.set_act(index - 1)

    def move_cursor(self, move):
        if move == -1:
            if self.cursor > 0:
                self.cursor -= 1
        elif move == 1:
            if self.cursor < len(self.exp):
                self.cursor += 1

    def insert(self, string):
        self.exp = self.exp[0:self.cursor] + string + self.exp[self.cursor:]
        self.cursor += len(string)

    def delete(self):
        self.exp = self.exp[:self.cursor-1] + self.exp[self.cursor:]
        self.cursor -= 1

    def draw(self):
        # draw graph of function
        old_pos = (-1, -1)
        drawability = display_width
        for pixel_x in range(0, display_width):
            try:
                x = (pixel_x - coor.origin[0]) / coor.scalex
                y = eval(self.exp)
                pixel_y = coor.origin[1] - y * coor.scaley
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

        # display function expression
        if Func.active == self:
            message.put(display,
                        "y = " + self.exp[:self.cursor] +
                        '|' + self.exp[self.cursor:])
        else:
            message.put(display, "y = " + self.exp)

        # display drawability message
        if not drawability:
            msg = "the function is not drawable"
        elif drawability != display_width:
            msg = "the function is not consistant"
        else:
            msg = "the function is consistant in view"
        message.indent()
        message.put(display, msg)
        message.unindent()


def main():
    functions = file.get()
    holding = set()

    pygame.key.set_repeat(300, 80)

    for func in functions:
        Func(func)

    while True:
        # reset
        message.reset()
        func = Func.active

        # keyboard controls
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_all(Func.family)
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
                            quit_all(Func.family)
                        elif event.key == K_MINUS:
                            coor.scalex /= 2
                            coor.scaley /= 2
                        elif event.key == K_EQUALS:
                            coor.scalex *= 2
                            coor.scaley *= 2
                        elif event.key == K_0:
                            coor.origin = [display_width/2, display_height/2]
                            coor.scalex, coor.scaley = 50, 50
                        elif event.key == K_9:
                            ave = (coor.scalex + coor.scaley) / 2
                            coor.scalex, coor.scaley = ave, ave
                        elif event.key == K_8:
                            coor.origin = [display_width/2, display_height/2]
                        elif event.key == K_BACKSPACE:
                            Func.remove()
                        elif event.key == K_n:
                            Func('')
                    elif "shift" in holding:
                        if event.key == K_6:
                            func.insert("**")
                        elif event.key == K_8:
                            func.insert('*')
                        elif event.key == K_9:
                            func.insert('(')
                        elif event.key == K_0:
                            func.insert(')')
                        elif event.key == K_EQUALS:
                            func.insert('+')
                    elif event.key == K_BACKSPACE:
                        if func:
                            func.delete()
                    elif event.key == K_LEFT:
                        func.move_cursor(-1)
                    elif event.key == K_RIGHT:
                        func.move_cursor(1)
                    elif event.key == K_UP:
                        Func.set_act('u')
                    elif event.key == K_DOWN:
                        Func.set_act('d')
                    elif event.key == K_SPACE:
                        func.insert(' ')
                    # basic input
                    else:
                        func.insert(key_name)
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
        elif mouse_press[2]:
            mouse_move = pygame.mouse.get_rel()
            coor.scalex *= 1 + mouse_move[0] / 100
            coor.scaley *= 1 + mouse_move[1] / -100
        else:
            # reset mouse release position
            pygame.mouse.get_rel()
            focus_x = mouse_pos[0]

        # display
        display.fill(WHITE)

        coor.axis()

        for func in Func.family:
            func.draw()

        # show focus point location

        pygame.display.flip()

        clock.tick(FPS)


def quit_all(data):
    file.put(data)
    pygame.quit()
    quit()


def error():
    quit_all([])


main()
