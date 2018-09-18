import pygame
import logging
from math import *
from modkeys import *
import os
import pickle
import pyperclip
import re
from time import time


# change directory to assests
INIT_DIR = os.path.abspath(os.path.curdir)
os.chdir(os.path.join(INIT_DIR, 'assets'))

# logger initiation
DEBUG_FILE = os.path.join(INIT_DIR, "debug", "debug_{}.log".format(time()))
if not os.path.exists(os.path.join(INIT_DIR, "debug")):
    os.makedirs(os.path.join(INIT_DIR, "debug"))
logger = logging.getLogger(__name__)
logging.basicConfig(filename=DEBUG_FILE, level=logging.DEBUG,
                    format="%(funcName)s:%(message)s")

# pygame display initiation
pygame.init()

pygame.key.set_repeat(300, 80)

display_width = 1200
display_height = 720

display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
pygame.display.set_caption("Function Simulator")
icon_img = pygame.image.load("icon.png")
pygame.display.set_icon(icon_img)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)
logo_img = pygame.image.load("quarkgame_logo.png")
tab_banner_img = pygame.image.load("tab_banner.png")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 128, 128)
GREY = (230, 230, 230)
DARK_GREY = (120, 120, 120)
LIGHT_BLUE = (153, 204, 255)
LIGHT_GREEN = (179, 255, 179)
LIGHT_YELLOW = (255, 255, 153)

FUNC_TAB = 1
VAR_TAB = 2
VIEW_TAB = 3

VAR_EXP_MATCH = 0
VAR_EXP_NAME = 1
VAR_EXP_VALUE = 2
VAR_EXP_LEGAL = 3

FPS = 30
SCALE_DX = 80
SCALE_DY = 80
SCALE_RATIO = 1.2

SS_PATH = os.path.join(os.path.expanduser('~'), "Desktop", "screenshot.jpg")
FULL_EXP = r"(?P<exp>.+)\[(?P<domain>.+)\]\s*$"
COE_PAIR = r"[0-9|\)|\w|_]x|x\("
VAR_EXP = r"(?P<vname>[\w|_]+)\s?=\s?(?P<value>\S+)\s*$"
FILE_PATH = r"(\w+)/?(\w+)"
PARENTHESIS = {'(': ')', '[': ']', '{': '}'}
CLOSE_PAREN = (')', ']', '}')


class Message:
    limit = 5
    delay_msg = []

    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 21)
        self.label_font = pygame.font.Font(None, 19)

    def label(self, x, y, textString, color=DARK_GREY):
        textString = str(textString)
        textBitmap = self.label_font.render(textString, True, color)
        textRect = textBitmap.get_rect()
        left_most = Tab.width if tab.visible else 0
        if x < left_most:
            x = left_most
        elif x > display_width - textRect.width:
            x = display_width - textRect.width
        if y < 0:
            y = 0
        elif y > display_height - textRect.height:
            y = display_height - textRect.height
        display.blit(textBitmap, [x + 1, y + 1])

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
            self.put(display, "Information")
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
        pygame.draw.line(display, DARK_GREY, (0, self.y), (Tab.width, self.y))
        self.y += 2


class File:

    def __init__(self, fname):
        self.fname = fname

    def get(self):
        try:
            with open(self.fname, 'rb') as f:
                Func.family = pickle.load(f)
                Var.family = pickle.load(f)
                coor.scalex = pickle.load(f)
                coor.scaley = pickle.load(f)
                coor.origin = pickle.load(f)
                coor.axis_show = pickle.load(f)
                coor.grid_show = pickle.load(f)
            if Func.family:
                Func.active = Func.family[Func._act_index]
            if Var.family:
                for var in Var.family:
                    var.exp = var.exp
                Var.active = Var.family[Var._act_index]
            logger.info("File {} is properly loaded".format(self.fname))
        except Exception as e:
            message.put_delayed(display, "Error occured while loading data")
            logger.error("File {} is not properly loaded".format(self.fname))

    def put(self):
        try:
            with open(self.fname, 'wb') as f:
                Tab.visible = True
                pickle.dump(Func.family, f)
                pickle.dump(Var.family, f)
                pickle.dump(coor.scalex, f)
                pickle.dump(coor.scaley, f)
                pickle.dump(coor.origin, f)
                pickle.dump(coor.axis_show, f)
                pickle.dump(coor.grid_show, f)
            logger.info("File {} properly saved".format(self.fname))
        except Exception as e:
            message.put_delayed(display, "Error occured while saving data")
            logger.error("File {} not properly saved".format(self.fname))

    def screenshot():
        pygame.image.save(display, SS_PATH)


class Coordinate:
    _stroke_width = 2

    def __init__(self):
        self.origin = [display_width / 2 + Tab.width / 2, display_height / 2]
        self._scalex = SCALE_DX
        self._scaley = SCALE_DY
        self.axis_show = True
        self.grid_show = True

    @property
    def scalex(self):
        return self._scalex

    @scalex.setter
    def scalex(self, value):
        old_scalex = self._scalex
        mouse_x = pygame.mouse.get_pos()[0]
        coor.chori((self.origin[0]-mouse_x)/old_scalex*(value-old_scalex), 0)
        self._scalex = value

    @property
    def scaley(self):
        return self._scaley

    @scaley.setter
    def scaley(self, value):
        old_scaley = self._scaley
        mouse_y = pygame.mouse.get_pos()[1]
        coor.chori(0, (self.origin[1]-mouse_y)/old_scaley*(value-old_scaley))
        self._scaley = value

    def chori(self, move_x, move_y):
        self.origin[0] += move_x
        self.origin[1] += move_y

    def axis(self):
        if self.axis_show:
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

    def grid(self):
        if not self.grid_show:
            return

        # initiate value
        ori_x, ori_y = map(int, coor.origin)
        gap_x, gap_y = SCALE_DX / coor.scalex, SCALE_DY / coor.scaley
        gap_x = sig_figure(gap_x, 2)
        gap_y = sig_figure(gap_y, 2)
        gap_px = int(gap_x * coor.scalex)
        gap_py = int(gap_y * coor.scaley)
        label_x, label_y = map(int, coor.origin)
        left_lim = Tab.width if tab.visible else 0

        # draw grid
        for line_x in range((ori_x - left_lim) % gap_px + left_lim,
                            display_width,
                            gap_px):
            pygame.draw.line(display,
                             GREY,
                             (line_x, 0),
                             (line_x, display_height),
                             Coordinate._stroke_width)
            val = (line_x - ori_x) / coor.scalex
            if val != 0:
                val = sig_figure(val, 2)
                message.label(line_x, label_y, val)
            else:
                message.label(line_x, label_y, 0)
        for line_y in range(ori_y % gap_py, display_height, gap_py):
            pygame.draw.line(display,
                             GREY,
                             (0, line_y),
                             (display_width, line_y),
                             Coordinate._stroke_width)
            val = (ori_y - line_y) / coor.scaley
            if val != 0:
                val = sig_figure(val, 2)
                message.label(label_x, line_y, val)


class Var:
    limit = 8
    family = []
    vars = {}
    active = None
    _act_index = 0

    def __init__(self, exp):
        if len(Var.family) < Var.limit:
            self._exp = ""
            self._vname = None
            self._value = None
            self.exp = exp
            self.cursor = len(exp)
            self.visible = True
            Var.family.append(self)
            Var.set_act(len(Var.family) - 1)
        else:
            message.put_delayed(display, "Maximum graph exceeded")

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp = value
        self.legal_check()
        if self.legality != VAR_EXP_LEGAL and self._vname in Var.vars:
            del Var.vars[self._vname]
        elif self.legality == VAR_EXP_LEGAL:
            Var.vars[self._vname] = self._value

    def set_act(index):
        if index == 'u':
            if Var._act_index > 0:
                Var._act_index -= 1
                Var.active = Var.family[Var._act_index]
        elif index == 'd':
            if Var._act_index < len(Var.family) - 1:
                Var._act_index += 1
                Var.active = Var.family[Var._act_index]
        elif Var.family:
            Var.active = Var.family[index]
            Var._act_index = index
        else:
            Var.active = None

    def remove():
        if Var.family:
            index = Var.family.index(Var.active)
            Var.family.remove(Var.active)
            if index == len(Var.family):
                Var.set_act(index-1)
            else:
                Var.set_act(index)
        else:
            message.put_delayed(display, "No variable to remove")

    def move_cursor(move):
        var = Var.active
        if move == -1:
            if var.cursor > 0:
                var.cursor -= 1
        elif move == 1:
            if var.cursor < len(var.exp):
                var.cursor += 1
        if move == -2:
            if var.cursor > 0:
                var.cursor = 0
        elif move == 2:
            if var.cursor < len(var.exp):
                var.cursor = len(var.exp)

    def insert(char):
        if not Var.active:
            message.put_delayed(display, "No variable has been created")
            return
        var = Var.active
        if len(var.exp) > 25:
            message.put_delayed(display, "Variable expression too long")
            return
        if char in CLOSE_PAREN:
            if var.cursor <= len(var.exp) - 1:
                if char == var.exp[var.cursor]:
                    var.cursor += 1
                    return
        var.exp = var.exp[0:var.cursor] + char + var.exp[var.cursor:]
        var.cursor += len(char)
        if char in PARENTHESIS:
            close = PARENTHESIS[char]
            var.exp = var.exp[0:var.cursor] + close + var.exp[var.cursor:]

    def delete():
        if not Var.active:
            message.put_delayed(display, "No variable has been created")
            return
        var = Var.active
        if var.cursor != 0:
            var.exp = var.exp[:var.cursor-1] + var.exp[var.cursor:]
            var.cursor -= 1

    def legal_check(self):
        # determine legality of a variable expression
        exp_match = re.match(VAR_EXP, self.exp)
        if not exp_match:
            self.legality = VAR_EXP_MATCH
        else:
            self._vname = exp_match.group("vname")
            self._value = exp_match.group("value")
            if not var_name(self._vname):
                self.legality = VAR_EXP_NAME
            elif not is_int(self._value):
                self.legality = VAR_EXP_VALUE
            else:
                self.legality = VAR_EXP_LEGAL
        return self.legality

    def show(self):
        if Var.active == self:
            message.put(display,
                        "var: " + self.exp[:self.cursor] +
                        '|' + self.exp[self.cursor:])
        else:
            message.put(display, "var: " + self.exp)

        # display variable status
        if self.legality == VAR_EXP_MATCH:
            msg = "the variable expression is illegal"
        elif self.legality == VAR_EXP_NAME:
            msg = "the name of the variable is illegal"
        elif self.legality == VAR_EXP_VALUE:
            msg = "the value of the variable is illegal"
        elif self.legality == VAR_EXP_LEGAL:
            msg = "the variable is legal"
        message.indent()
        message.put(display, msg)
        message.unindent()

    def __del__(self):
        del Var.vars[self._vname]


class Func:
    limit = 8
    family = []
    active = None
    _act_index = 0
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
            message.put_delayed(display, "Maximum graph exceeded")

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
        else:
            Func.active = None

    def remove():
        if Func.family:
            index = Func.family.index(Func.active)
            Func.family.remove(Func.active)
            if index == len(Func.family):
                Func.set_act(index-1)
            else:
                Func.set_act(index)
        else:
            message.put_delayed(display, "No graph expression to remove")

    def move_cursor(move):
        func = Func.active
        if move == -1:
            if func.cursor > 0:
                func.cursor -= 1
        elif move == 1:
            if func.cursor < len(func.exp):
                func.cursor += 1
        if move == -2:
            if func.cursor > 0:
                func.cursor = 0
        elif move == 2:
            if func.cursor < len(func.exp):
                func.cursor = len(func.exp)

    def insert(char):
        if not Func.active:
            message.put_delayed(display, "No expression has been created")
            return
        func = Func.active
        if len(func.exp) > 25:
            message.put_delayed(display, "Expression too long")
            return
        if char in CLOSE_PAREN:
            if func.cursor <= len(func.exp) - 1:
                if char == func.exp[func.cursor]:
                    func.cursor += 1
                    return
        func.exp = func.exp[0:func.cursor] + char + func.exp[func.cursor:]
        func.cursor += len(char)
        if char in PARENTHESIS:
            close = PARENTHESIS[char]
            func.exp = func.exp[0:func.cursor] + close + func.exp[func.cursor:]

    def delete():
        if not Func.active:
            message.put_delayed(display, "No expression has been created")
            return
        func = Func.active
        if func.cursor != 0:
            func.exp = func.exp[:func.cursor-1] + func.exp[func.cursor:]
            func.cursor -= 1

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
        while re.findall(COE_PAIR, exp):
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
        # draw graph of the expression
        old_pos = (-1, -1)
        drawability = display_width * Func._accuracy + 1
        for vname, value in Var.vars.items():
            exec("{0} = {1}".format(vname, value))

        for raw_x in range(-1, drawability - 1):
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
                                     (round(pixel_x), round(pixel_y)),
                                     Func._stroke_width)
                old_pos = (round(pixel_x), round(pixel_y))
            except Exception:
                drawability -= 1
        self.drawability = drawability

    def show(self):
        # display expression
        if pygame.key.get_pressed()[K_TAB]:
            message.put(display, "y = " + str(self.true_exp()))
        else:
            if Func.active == self:
                message.put(display,
                            "y = " + self.exp[:self.cursor] +
                            '|' + self.exp[self.cursor:])
            else:
                message.put(display, "y = " + self.exp)

        # display graph status
        if not self.visible:
            msg = "the graph is set to invisible"
        elif not self.drawability:
            msg = "the graph is not drawable"
        elif self.drawability != display_width * Func._accuracy + 1:
            msg = "the graph is not consistent"
        else:
            msg = "the graph is consistent in view"
        message.indent()
        message.put(display, msg)
        message.unindent()


class Tab:
    width = 300

    def __init__(self):
        self._visible = True

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        temp = self._visible
        self._visible = value
        if not tab._visible:
            coor.chori(-Tab.width / 2, 0)
        elif not temp:
            coor.chori(Tab.width / 2, 0)

    def show_tab(self):
        if tab.visible:
            message.y += 40
        if tab.visible == FUNC_TAB:
            self.func_tab()
        elif tab.visible == VAR_TAB:
            self.var_tab()
        elif tab.visible == VIEW_TAB:
            self.view_tab()
        if tab.visible:
            display.blit(tab_banner_img, (0, 0))

    def func_tab(self):
        pygame.draw.rect(display,
                         LIGHT_BLUE,
                         (0, 0, Tab.width, display_height))
        for func in Func.family:
            func.show()

    def var_tab(self):
        pygame.draw.rect(display,
                         LIGHT_GREEN,
                         (0, 0, Tab.width, display_height))
        for var in Var.family:
            var.show()

    def view_tab(self):
        pygame.draw.rect(display,
                         LIGHT_YELLOW,
                         (0, 0, Tab.width, display_height))

    def resize_win(self, w, h):
        global display_width, display_height
        old_size = display.get_rect()
        old_w, old_h = old_size.right, old_size.bottom
        if w < 800:
            w = 800
            message.put_delayed(display, "minimal window width is 800")
        if h < 600:
            h = 600
            message.put_delayed(display, "minimal window height is 600")
        display_width, display_height = w, h
        pygame.display.set_mode((w, h), RESIZABLE)
        coor.chori((w - old_w) / 2, (h - old_h) / 2)


data = File("data.p")
message = Message()
coor = Coordinate()
tab = Tab()


def sig_figure(x, fig):
    return round(x, fig - int(floor(log10(abs(x)))) - 1)


def is_int(literal):
    try:
        int(eval(literal))
    except Exception as e:
        return False
    else:
        return True


def var_name(literal):
    if literal in Var.vars:
        return True
    elif literal in vars():
        return False
    elif literal in globals():
        return False
    elif literal in vars(__builtins__):
        return False
    else:
        return True


def main():
    global display_width, display_height, shortcuts

    data.get()
    with open("shortcuts.txt", 'r') as f:
        shortcuts = [line.replace('\n', '') for line in f.readlines()]

    while True:

        # reset
        message.reset()
        func = Func.active
        var = Var.active
        corner = pygame.Rect(display_width - 45, 0, 45, 36)

        # pygame event controls
        for event in pygame.event.get():
            logger.debug("event:{}".format(event))
            if event.type == QUIT:
                quit_all()
            mods = pygame.key.get_mods()
            if event.type == KEYDOWN:
                # keyboard shortcuts with modifiers
                if mods & KMOD_META and mods & KMOD_SHIFT:
                    if event.key == K_MINUS:
                        coor.scalex /= SCALE_RATIO
                        coor.scaley /= SCALE_RATIO
                    elif event.key == K_EQUALS:
                        coor.scalex *= SCALE_RATIO
                        coor.scaley *= SCALE_RATIO
                    elif event.key == K_c:
                        File.screenshot()
                elif mods & KMOD_META:
                    if event.key == K_q:
                        quit_all()
                    elif event.key == K_m:
                        pygame.display.iconify()
                    elif event.key == K_MINUS:
                        coor.scalex /= 2
                        coor.scaley /= 2
                    elif event.key == K_EQUALS:
                        coor.scalex *= 2
                        coor.scaley *= 2
                    elif event.key == K_0:
                        coor.scalex, coor.scaley = SCALE_DX, SCALE_DY
                        if tab.visible:
                            coor.origin = [display_width / 2 + Tab.width / 2,
                                           display_height / 2]
                        else:
                            coor.origin = [display_width/2, display_height/2]
                    elif event.key == K_9:
                        ave = (coor.scalex + coor.scaley) / 2
                        coor.scalex, coor.scaley = ave, ave
                    elif event.key == K_8:
                        if tab.visible:
                            coor.origin = [display_width / 2 + Tab.width / 2,
                                           display_height / 2]
                        else:
                            coor.origin = [display_width/2, display_height/2]
                    elif event.key == K_BACKSPACE:
                        if tab.visible == FUNC_TAB:
                            Func.remove()
                        if tab.visible == VAR_TAB:
                            Var.remove()
                    elif event.key == K_RETURN:
                        if tab.visible == FUNC_TAB:
                            Func('')
                        elif tab.visible == VAR_TAB:
                            Var('')
                    elif event.key == K_1:
                        if tab.visible == FUNC_TAB:
                            tab.visible = None
                        else:
                            tab.visible = FUNC_TAB
                    elif event.key == K_2:
                        if tab.visible == VAR_TAB:
                            tab.visible = None
                        else:
                            tab.visible = VAR_TAB
                    elif event.key == K_3:
                        if tab.visible == VIEW_TAB:
                            tab.visible = None
                        else:
                            tab.visible = VIEW_TAB
                    elif event.key == K_a:
                        coor.axis_show = not coor.axis_show
                    elif event.key == K_g:
                        coor.grid_show = not coor.grid_show
                    elif event.key == K_c:
                        if tab.visible == FUNC_TAB:
                            pyperclip.copy(func.exp)
                    elif event.key == K_v:
                        if tab.visible == FUNC_TAB:
                            func.exp = pyperclip.paste()
                            Func.move_cursor(2)
                    elif event.key == K_LEFT:
                        Func.move_cursor(-2)
                    elif event.key == K_RIGHT:
                        Func.move_cursor(2)
                elif not tab.visible:
                    pass
                elif tab.visible == FUNC_TAB:
                    # shift key alternatives
                    if mods & KMOD_SHIFT:
                        for shift in SHIFTS:
                            if event.key == shift[0]:
                                Func.insert(shift[1])
                    # alt key alternatives
                    elif mods & KMOD_ALT:
                        for alt in ALTS:
                            if event.key == alt[0]:
                                Func.insert(alt[1])
                    # single key shortcuts
                    elif event.key == K_BACKSPACE:
                        if func:
                            Func.delete()
                    elif event.key == K_LEFT:
                        Func.move_cursor(-1)
                    elif event.key == K_RIGHT:
                        Func.move_cursor(1)
                    elif event.key == K_UP:
                        Func.set_act('u')
                    elif event.key == K_DOWN:
                        Func.set_act('d')
                    elif event.key == K_RETURN:
                        if not Func.active:
                            message.put_delayed(display,
                                                "No expression available")
                        else:
                            func.visible = not func.visible
                    elif event.key == K_SPACE:
                        Func.insert(' ')
                    # basic input
                    else:
                        k_name = pygame.key.name(event.key)
                        if not mods and len(k_name) == 1:
                            Func.insert(pygame.key.name(event.key))
                elif tab.visible == VAR_TAB:
                    # shift key alternatives
                    if mods & KMOD_SHIFT:
                        for shift in SHIFTS:
                            if event.key == shift[0]:
                                Var.insert(shift[1])
                    # alt key alternatives
                    elif mods & KMOD_ALT:
                        for alt in ALTS:
                            if event.key == alt[0]:
                                Var.insert(alt[1])
                    # single key shortcuts
                    elif event.key == K_BACKSPACE:
                        if var:
                            Var.delete()
                    elif event.key == K_LEFT:
                        Var.move_cursor(-1)
                    elif event.key == K_RIGHT:
                        Var.move_cursor(1)
                    elif event.key == K_UP:
                        Var.set_act('u')
                    elif event.key == K_DOWN:
                        Var.set_act('d')
                    elif event.key == K_RETURN:
                        if not Var.active:
                            message.put_delayed(display,
                                                "No expression available")
                        else:
                            var.visible = not var.visible
                    elif event.key == K_SPACE:
                        Var.insert(' ')
                    # basic input
                    else:
                        k_name = pygame.key.name(event.key)
                        if not mods and len(k_name) == 1:
                            Var.insert(pygame.key.name(event.key))
            elif event.type == MOUSEBUTTONDOWN:
                if mods & KMOD_SHIFT:
                    if event.button == 4:
                        coor.scalex /= SCALE_RATIO
                        coor.scaley /= SCALE_RATIO
                    elif event.button == 5:
                        coor.scalex *= SCALE_RATIO
                        coor.scaley *= SCALE_RATIO
            elif event.type == VIDEORESIZE:
                tab.resize_win(event.w, event.h)

        # mouse control
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if mods & KMOD_CTRL:
            coor.chori(*pygame.mouse.get_rel())
        elif mouse_press[0]:
                coor.chori(*pygame.mouse.get_rel())
        elif mouse_press[2]:
            mouse_move = pygame.mouse.get_rel()
            minimal = min(display_width, display_height)
            coor.scalex *= 1 + mouse_move[0] / -minimal
            coor.scaley *= 1 + mouse_move[1] / minimal
        else:
            if corner.collidepoint(mouse_pos):
                show_shortcuts()
            # reset mouse release position
            pygame.mouse.get_rel()
            focus_x = mouse_pos[0]

        # display
        display.fill(WHITE)

        coor.grid()
        coor.axis()

        for func in Func.family:
            func.draw()

        tab.show_tab()

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

    show = True
    start = 0

    while show:

        for event in pygame.event.get():
            mods = pygame.key.get_mods()
            if mods & KMOD_META:
                if event.key == K_q:
                    quit_all()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    if start > 0:
                        start -= 1
                elif event.key == K_DOWN:
                    if start < len(shortcuts) - line_num - 1:
                        start += 1
            elif event.type == VIDEORESIZE:
                tab.resize_win(event.w, event.h)
        mouse_pos = pygame.mouse.get_pos()
        corner = pygame.Rect(display_width - 45, 0, 45, 36)
        if not corner.collidepoint(mouse_pos):
            show = not show

        display.fill(WHITE)
        message.reset()
        line_num = (display_height-10) / message.line_height - 1
        logger.debug("line_num -> {}".format(line_num))
        end = int(start + line_num)
        logger.debug("end -> {}".format(end))
        if end > len(shortcuts) - 1:
            end = len(shortcuts) - 1
        for i in range(start, end + 1):
            message.put(display, shortcuts[i])
        display.blit(logo_img, (display_width - 45, 10))
        pygame.display.flip()

        clock.tick(FPS)
    message.reset()


def error(e_name):
    logger.error(e.__class__.__name__, exc_info=True)

    display.fill(WHITE)
    message.reset()
    message.put(display, "Encontered Error")
    message.indent()
    message.put(display, "Error name: " + e_name)
    message.put(display, "Log location: " + os.path.abspath(os.path.curdir))
    message.put(display, "Press any key to exit...")
    display.blit(logo_img, (display_width - 45, 10))
    pygame.display.flip()

    show = True
    while show:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN:
                quit_all(False)
        clock.tick(FPS)


def quit_all(save=True):
    if save:
        data.put()
    logger.debug("Quit all called by user")
    pygame.quit()
    quit()


try:
    main()
except Exception as e:
    error(e.__class__.__name__)
