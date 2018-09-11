import pygame
from pygame.locals import *
from math import *
import os
import re
import pyperclip

# set default directory to assets
os.chdir(os.path.join(os.path.abspath(os.path.curdir), 'assets'))

# pygame display initiation
pygame.init()

display_width = 1200
display_height = 720

display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
pygame.display.set_caption("Function Simulator")
icon_img = pygame.image.load("icon.png")
pygame.display.set_icon(icon_img)

clock = pygame.time.Clock()
FPS = 30

font = pygame.font.Font(None, 20)
logo_img = pygame.image.load("quarkgame_logo.png")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (153, 204, 255)

SS_PATH = os.path.join(os.path.expanduser('~'), "Desktop", "screenshot.jpg")
FULL_EXP = r"(?P<exp>.+)\[(?P<domain>.+)\]"
COE_PAIR = r"[0-9|\)]x"

ALTS = ((K_v, '√'),
        (K_p, 'π'),
        (K_t, '±'),
        (K_EQUALS, '≠'))
SHIFTS = ((K_5, "%"),
          (K_6, "^"),
          (K_8, '*'),
          (K_9, '('),
          (K_0, ')'),
          (K_EQUALS, '+'),
          (K_COMMA, '<'),
          (K_PERIOD, '>'))
SWITCH = (('√', "sqrt"),
          ('^', "**"),
          ('%', "*0.01"),
          ('π', "pi"),
          ("+-", '±'),
          ('=', "=="),
          ('≠', "!="))


class File:

    def __init__(self, fname):
        self.fname = fname

    def get(self):
        try:
            with open(self.fname, 'r') as f:
                cont = [s.replace('\n', '') for s in f.readlines()]
            return cont
        except FileNotFoundError:
            return ['']

    def put(self, cont):
        if cont:
            with open(self.fname, 'w') as f:
                for each in cont:
                    f.write(each + '\n')

    def screenshot():
        pygame.image.save(display, SS_PATH)


class Message:
    limit = 5
    delay_msg = []

    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 21)

    def put(self, screen, textString, color=BLACK):
        textBitmap = self.font.render(textString, True, color)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def put_delayed(self, screen, textString, show_time=1):
        Message.delay_msg.append([screen, textString, show_time * FPS])

    def show_delayed(self):
        if len(Message.delay_msg) >= Message.limit:
            del Message.delay_msg[:-5]
        if len(Message.delay_msg) != 0:
            self.put(display, "information")
            self.indent()
            for msg in Message.delay_msg:
                self.put(msg[0], msg[1])
                msg[2] -= 1
                if msg[2] <= 0:
                    Message.delay_msg.remove(msg)
            self.unindent()

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 18

    def indent(self):
        self.x += 15

    def unindent(self):
        self.x -= 15


class Coordinate:
    _stroke_width = 2

    def __init__(self):
        self.origin = [display_width / 2, display_height / 2]
        self.scalex = 50
        self.scaley = 50

    def axis(self):
        pygame.draw.line(display,
                         RED,
                         (0, self.origin[1]),
                         (display_width, self.origin[1]),
                         Coordinate._stroke_width)
        pygame.draw.line(display,
                         RED,
                         (self.origin[0], 0),
                         (self.origin[0], display_height),
                         Coordinate._stroke_width)

    def chori(self, move_x, move_y):
        self.origin[0] += move_x
        self.origin[1] += move_y


class Func:
    limit = 8
    family = []
    active = None
    _act_index = -1
    _accuracy = 1
    _stroke_width = 2

    def __init__(self, exp):
        if len(Func.family) < Func.limit:
            self.exp = exp
            self.cursor = len(exp)
            self.visible = True
            Func.family.append(self)
            Func.set_act(len(Func.family) - 1)
        else:
            message.put_delayed(display, "Number of function reached maximum")

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
        if Func.family:
            index = Func.family.index(Func.active)
            Func.family.remove(Func.active)
            if index == len(Func.family):
                Func.set_act(index-1)
            else:
                Func.set_act(index)
        else:
            message.put_delayed(display, "No function to remove")

    def move_cursor(self, move):
        if move == -1:
            if self.cursor > 0:
                self.cursor -= 1
        elif move == 1:
            if self.cursor < len(self.exp):
                self.cursor += 1
        if move == -2:
            if self.cursor > 0:
                self.cursor = 0
        elif move == 2:
            if self.cursor < len(self.exp):
                self.cursor = len(self.exp)

    def insert(self, string):
        self.exp = self.exp[0:self.cursor] + string + self.exp[self.cursor:]
        self.cursor += len(string)

    def delete(self):
        if self.exp:
            self.exp = self.exp[:self.cursor-1] + self.exp[self.cursor:]
            self.cursor -= 1

    def true_exp(self):
        exp_match = re.match(FULL_EXP, self.exp)
        if not exp_match:
            exp = self.exp
        else:
            exp = exp_match.group("exp")
            domain = exp_match.group("domain")
            for switch in SWITCH:
                domain = domain.replace(switch[0], switch[1])

        for switch in SWITCH:
            exp = exp.replace(switch[0], switch[1])
        for pair in set(re.findall(COE_PAIR, exp)):
            exp = exp.replace(pair, pair[0] + '*' + pair[1])

        if not exp_match:
            return exp
        else:
            return exp, domain

    def draw(self):
        true_exp = self.true_exp()
        if self.visible:
            if type(true_exp) == str:
                if '±' not in true_exp:
                    self.graph(true_exp)
                else:
                    message.indent()
                    self.graph(true_exp.replace('±', '+'))
                    self.graph(true_exp.replace('±', '-'))
                    message.unindent()
            else:
                exp, domain = true_exp
                if '±' not in exp:
                    self.graph(exp, domain)
                else:
                    message.indent()
                    self.graph(exp.replace('±', '+'), domain)
                    self.graph(exp.replace('±', '-'), domain)
                    message.unindent()

    def graph(self, exp, domain="True"):
        # draw graph of function
        old_pos = (-1, -1)
        drawability = display_width
        for raw_x in range(-1, display_width * Func._accuracy):
            try:
                pixel_x = raw_x / Func._accuracy
                x = (pixel_x - coor.origin[0]) / coor.scalex
                y = eval(exp)
                pixel_y = coor.origin[1] - y * coor.scaley
                temp = 0 < old_pos[1] < display_height
                temp = temp or 0 < pixel_y < display_height
                temp = temp and eval(domain)
                if pixel_x - old_pos[0] <= 1 and temp:
                    pygame.draw.line(display,
                                     BLACK,
                                     old_pos,
                                     (int(pixel_x), int(pixel_y)),
                                     Func._stroke_width)
                old_pos = (int(pixel_x), int(pixel_y))
            except Exception:
                drawability -= 1
        self.drawability = drawability

    def show(self):
        # display function expression
        if pygame.key.get_pressed()[K_TAB]:
            message.put(display, "y = " + str(self.true_exp()))
        else:
            if Func.active == self:
                message.put(display,
                            "y = " + self.exp[:self.cursor] +
                            '|' + self.exp[self.cursor:])
            else:
                message.put(display, "y = " + self.exp)

        # display function status
        if not self.visible:
            msg = "the function is set to invisible"
        elif not self.drawability:
            msg = "the function is not drawable"
        elif self.drawability != display_width:
            msg = "the function is not consistent"
        else:
            msg = "the function is consistent in view"
        message.indent()
        message.put(display, msg)
        message.unindent()

class Tab:
    def __init__(self):
        self.visible = True

    def draw(self):
        if self.visible:
            pygame.draw.rect(display, LIGHT_BLUE, (0, 0, 300, display_height))
            for func in Func.family:
                func.show()

data = File("data")
shortcuts = File("shortcuts")
message = Message()
coor = Coordinate()
tab = Tab()


def main():
    global display_width, display_height, shortcuts
    functions = data.get()
    shortcuts = shortcuts.get()

    pygame.key.set_repeat(300, 80)

    if functions:
        for func in functions:
            Func(func)
    else:
        Func('')

    while True:

        # reset
        message.reset()
        func = Func.active
        corner = pygame.Rect(display_width - 45, 0, 45, 36)

        # keyboard controls
        for event in pygame.event.get():
            if event.type == QUIT:
                quit_all([f.exp for f in Func.family])
            mods = pygame.key.get_mods()
            if event.type == KEYDOWN:
                # special operations
                if mods & KMOD_META:
                    if event.key == K_q:
                        quit_all([f.exp for f in Func.family])
                    elif event.key == K_m:
                        pygame.display.iconify()
                    elif event.key == K_s:
                        File.screenshot()
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
                    elif event.key == K_RETURN:
                        Func('')
                    elif event.key == K_f:
                        tab.visible = not tab.visible
                    elif event.key == K_c:
                        pyperclip.copy(func.exp)
                    elif event.key == K_v:
                        func.exp = pyperclip.paste()
                        func.move_cursor(2)
                    elif event.key == K_LEFT:
                        func.move_cursor(-2)
                    elif event.key == K_RIGHT:
                        func.move_cursor(2)
                elif mods & KMOD_SHIFT:
                    for shift in SHIFTS:
                        if event.key == shift[0]:
                            func.insert(shift[1])
                elif mods & KMOD_ALT:
                    for alt in ALTS:
                        if event.key == alt[0]:
                            func.insert(alt[1])
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
                elif event.key == K_RETURN:
                    func.visible = not func.visible
                elif event.key == K_SPACE:
                    func.insert(' ')
                # basic input
                else:
                    k_name = pygame.key.name(event.key)
                    if len(k_name) == 1:
                        func.insert(pygame.key.name(event.key))
            elif event.type == MOUSEBUTTONDOWN:
                if mods & KMOD_SHIFT:
                    if event.button == 4:
                        coor.scalex /= 1.2
                        coor.scaley /= 1.2
                    elif event.button == 5:
                        coor.scalex *= 1.2
                        coor.scaley *= 1.2
            elif event.type == VIDEORESIZE:
                display_width, display_height = event.w, event.h
                pygame.display.set_mode((event.w, event.h), RESIZABLE)

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
            if corner.collidepoint(mouse_pos):
                show_shortcuts()
            # reset mouse release position
            pygame.mouse.get_rel()
            focus_x = mouse_pos[0]

        # display
        display.fill(WHITE)

        coor.axis()

        for func in Func.family:
            func.draw()

        tab.draw()

        message.show_delayed()
        display.blit(logo_img, (display_width - 45, 10))

        if pygame.key.get_pressed()[K_CAPSLOCK]:
            message.put(display, "Frame per second")
            message.indent()
            message.put(display, str(clock.get_fps()))

        pygame.display.flip()

        clock.tick(FPS)


def show_shortcuts():
    global display_width, display_height

    display.fill(WHITE)
    message.reset()
    message.put(display, "Shortcuts")
    message.indent()
    for shortcut in shortcuts:
        message.put(display, shortcut)
    display.blit(logo_img, (display_width - 45, 10))
    pygame.display.flip()

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                display_width, display_height = event.w, event.h
                pygame.display.set_mode((event.w, event.h), RESIZABLE)
        mouse_pos = pygame.mouse.get_pos()
        corner = pygame.Rect(display_width - 45, 0, 45, 46)
        if not corner.collidepoint(mouse_pos):
            show = not show
        clock.tick(FPS)
    message.reset()


def quit_all(cont):
    data.put(cont)
    pygame.quit()
    quit()


def error():
    quit_all(None)


main()
