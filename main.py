import math
import pygame
import logging

# from modkeys import *
from pygame.locals import (
    ACTIVEEVENT,
    ANYFORMAT,
    APPACTIVE,
    APPINPUTFOCUS,
    APPMOUSEFOCUS,
    APP_DIDENTERBACKGROUND,
    APP_DIDENTERFOREGROUND,
    APP_LOWMEMORY,
    APP_TERMINATING,
    APP_WILLENTERBACKGROUND,
    APP_WILLENTERFOREGROUND,
    ASYNCBLIT,
    AUDIODEVICEADDED,
    AUDIODEVICEREMOVED,
    AUDIO_ALLOW_ANY_CHANGE,
    AUDIO_ALLOW_CHANNELS_CHANGE,
    AUDIO_ALLOW_FORMAT_CHANGE,
    AUDIO_ALLOW_FREQUENCY_CHANGE,
    AUDIO_S16,
    AUDIO_S16LSB,
    AUDIO_S16MSB,
    AUDIO_S16SYS,
    AUDIO_S8,
    AUDIO_U16,
    AUDIO_U16LSB,
    AUDIO_U16MSB,
    AUDIO_U16SYS,
    AUDIO_U8,
    BIG_ENDIAN,
    BLENDMODE_ADD,
    BLENDMODE_BLEND,
    BLENDMODE_MOD,
    BLENDMODE_NONE,
    BLEND_ADD,
    BLEND_ALPHA_SDL2,
    BLEND_MAX,
    BLEND_MIN,
    BLEND_MULT,
    BLEND_PREMULTIPLIED,
    BLEND_RGBA_ADD,
    BLEND_RGBA_MAX,
    BLEND_RGBA_MIN,
    BLEND_RGBA_MULT,
    BLEND_RGBA_SUB,
    BLEND_RGB_ADD,
    BLEND_RGB_MAX,
    BLEND_RGB_MIN,
    BLEND_RGB_MULT,
    BLEND_RGB_SUB,
    BLEND_SUB,
    BUTTON_LEFT,
    BUTTON_MIDDLE,
    BUTTON_RIGHT,
    BUTTON_WHEELDOWN,
    BUTTON_WHEELUP,
    BUTTON_X1,
    BUTTON_X2,
    CLIPBOARDUPDATE,
    CONTROLLERAXISMOTION,
    CONTROLLERBUTTONDOWN,
    CONTROLLERBUTTONUP,
    CONTROLLERDEVICEADDED,
    CONTROLLERDEVICEREMAPPED,
    CONTROLLERDEVICEREMOVED,
    CONTROLLERSENSORUPDATE,
    CONTROLLERTOUCHPADDOWN,
    CONTROLLERTOUCHPADMOTION,
    CONTROLLERTOUCHPADUP,
    CONTROLLER_AXIS_INVALID,
    CONTROLLER_AXIS_LEFTX,
    CONTROLLER_AXIS_LEFTY,
    CONTROLLER_AXIS_MAX,
    CONTROLLER_AXIS_RIGHTX,
    CONTROLLER_AXIS_RIGHTY,
    CONTROLLER_AXIS_TRIGGERLEFT,
    CONTROLLER_AXIS_TRIGGERRIGHT,
    CONTROLLER_BUTTON_A,
    CONTROLLER_BUTTON_B,
    CONTROLLER_BUTTON_BACK,
    CONTROLLER_BUTTON_DPAD_DOWN,
    CONTROLLER_BUTTON_DPAD_LEFT,
    CONTROLLER_BUTTON_DPAD_RIGHT,
    CONTROLLER_BUTTON_DPAD_UP,
    CONTROLLER_BUTTON_GUIDE,
    CONTROLLER_BUTTON_INVALID,
    CONTROLLER_BUTTON_LEFTSHOULDER,
    CONTROLLER_BUTTON_LEFTSTICK,
    CONTROLLER_BUTTON_MAX,
    CONTROLLER_BUTTON_RIGHTSHOULDER,
    CONTROLLER_BUTTON_RIGHTSTICK,
    CONTROLLER_BUTTON_START,
    CONTROLLER_BUTTON_X,
    CONTROLLER_BUTTON_Y,
    Color,
    DOUBLEBUF,
    DROPBEGIN,
    DROPCOMPLETE,
    DROPFILE,
    DROPTEXT,
    FINGERDOWN,
    FINGERMOTION,
    FINGERUP,
    FULLSCREEN,
    GL_ACCELERATED_VISUAL,
    GL_ACCUM_ALPHA_SIZE,
    GL_ACCUM_BLUE_SIZE,
    GL_ACCUM_GREEN_SIZE,
    GL_ACCUM_RED_SIZE,
    GL_ALPHA_SIZE,
    GL_BLUE_SIZE,
    GL_BUFFER_SIZE,
    GL_CONTEXT_DEBUG_FLAG,
    GL_CONTEXT_FLAGS,
    GL_CONTEXT_FORWARD_COMPATIBLE_FLAG,
    GL_CONTEXT_MAJOR_VERSION,
    GL_CONTEXT_MINOR_VERSION,
    GL_CONTEXT_PROFILE_COMPATIBILITY,
    GL_CONTEXT_PROFILE_CORE,
    GL_CONTEXT_PROFILE_ES,
    GL_CONTEXT_PROFILE_MASK,
    GL_CONTEXT_RELEASE_BEHAVIOR,
    GL_CONTEXT_RELEASE_BEHAVIOR_FLUSH,
    GL_CONTEXT_RELEASE_BEHAVIOR_NONE,
    GL_CONTEXT_RESET_ISOLATION_FLAG,
    GL_CONTEXT_ROBUST_ACCESS_FLAG,
    GL_DEPTH_SIZE,
    GL_DOUBLEBUFFER,
    GL_FRAMEBUFFER_SRGB_CAPABLE,
    GL_GREEN_SIZE,
    GL_MULTISAMPLEBUFFERS,
    GL_MULTISAMPLESAMPLES,
    GL_RED_SIZE,
    GL_SHARE_WITH_CURRENT_CONTEXT,
    GL_STENCIL_SIZE,
    GL_STEREO,
    GL_SWAP_CONTROL,
    HAT_CENTERED,
    HAT_DOWN,
    HAT_LEFT,
    HAT_LEFTDOWN,
    HAT_LEFTUP,
    HAT_RIGHT,
    HAT_RIGHTDOWN,
    HAT_RIGHTUP,
    HAT_UP,
    HIDDEN,
    HWACCEL,
    HWPALETTE,
    HWSURFACE,
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYBUTTONDOWN,
    JOYBUTTONUP,
    JOYDEVICEADDED,
    JOYDEVICEREMOVED,
    JOYHATMOTION,
    KEYDOWN,
    KEYMAPCHANGED,
    KEYUP,
    KMOD_ALT,
    KMOD_CAPS,
    KMOD_CTRL,
    KMOD_GUI,
    KMOD_LALT,
    KMOD_LCTRL,
    KMOD_LGUI,
    KMOD_LMETA,
    KMOD_LSHIFT,
    KMOD_META,
    KMOD_MODE,
    KMOD_NONE,
    KMOD_NUM,
    KMOD_RALT,
    KMOD_RCTRL,
    KMOD_RGUI,
    KMOD_RMETA,
    KMOD_RSHIFT,
    KMOD_SHIFT,
    KSCAN_0,
    KSCAN_1,
    KSCAN_2,
    KSCAN_3,
    KSCAN_4,
    KSCAN_5,
    KSCAN_6,
    KSCAN_7,
    KSCAN_8,
    KSCAN_9,
    KSCAN_A,
    KSCAN_AC_BACK,
    KSCAN_APOSTROPHE,
    KSCAN_B,
    KSCAN_BACKSLASH,
    KSCAN_BACKSPACE,
    KSCAN_BREAK,
    KSCAN_C,
    KSCAN_CAPSLOCK,
    KSCAN_CLEAR,
    KSCAN_COMMA,
    KSCAN_CURRENCYSUBUNIT,
    KSCAN_CURRENCYUNIT,
    KSCAN_D,
    KSCAN_DELETE,
    KSCAN_DOWN,
    KSCAN_E,
    KSCAN_END,
    KSCAN_EQUALS,
    KSCAN_ESCAPE,
    KSCAN_EURO,
    KSCAN_F,
    KSCAN_F1,
    KSCAN_F10,
    KSCAN_F11,
    KSCAN_F12,
    KSCAN_F13,
    KSCAN_F14,
    KSCAN_F15,
    KSCAN_F2,
    KSCAN_F3,
    KSCAN_F4,
    KSCAN_F5,
    KSCAN_F6,
    KSCAN_F7,
    KSCAN_F8,
    KSCAN_F9,
    KSCAN_G,
    KSCAN_GRAVE,
    KSCAN_H,
    KSCAN_HELP,
    KSCAN_HOME,
    KSCAN_I,
    KSCAN_INSERT,
    KSCAN_INTERNATIONAL1,
    KSCAN_INTERNATIONAL2,
    KSCAN_INTERNATIONAL3,
    KSCAN_INTERNATIONAL4,
    KSCAN_INTERNATIONAL5,
    KSCAN_INTERNATIONAL6,
    KSCAN_INTERNATIONAL7,
    KSCAN_INTERNATIONAL8,
    KSCAN_INTERNATIONAL9,
    KSCAN_J,
    KSCAN_K,
    KSCAN_KP0,
    KSCAN_KP1,
    KSCAN_KP2,
    KSCAN_KP3,
    KSCAN_KP4,
    KSCAN_KP5,
    KSCAN_KP6,
    KSCAN_KP7,
    KSCAN_KP8,
    KSCAN_KP9,
    KSCAN_KP_0,
    KSCAN_KP_1,
    KSCAN_KP_2,
    KSCAN_KP_3,
    KSCAN_KP_4,
    KSCAN_KP_5,
    KSCAN_KP_6,
    KSCAN_KP_7,
    KSCAN_KP_8,
    KSCAN_KP_9,
    KSCAN_KP_DIVIDE,
    KSCAN_KP_ENTER,
    KSCAN_KP_EQUALS,
    KSCAN_KP_MINUS,
    KSCAN_KP_MULTIPLY,
    KSCAN_KP_PERIOD,
    KSCAN_KP_PLUS,
    KSCAN_L,
    KSCAN_LALT,
    KSCAN_LANG1,
    KSCAN_LANG2,
    KSCAN_LANG3,
    KSCAN_LANG4,
    KSCAN_LANG5,
    KSCAN_LANG6,
    KSCAN_LANG7,
    KSCAN_LANG8,
    KSCAN_LANG9,
    KSCAN_LCTRL,
    KSCAN_LEFT,
    KSCAN_LEFTBRACKET,
    KSCAN_LGUI,
    KSCAN_LMETA,
    KSCAN_LSHIFT,
    KSCAN_LSUPER,
    KSCAN_M,
    KSCAN_MENU,
    KSCAN_MINUS,
    KSCAN_MODE,
    KSCAN_N,
    KSCAN_NONUSBACKSLASH,
    KSCAN_NONUSHASH,
    KSCAN_NUMLOCK,
    KSCAN_NUMLOCKCLEAR,
    KSCAN_O,
    KSCAN_P,
    KSCAN_PAGEDOWN,
    KSCAN_PAGEUP,
    KSCAN_PAUSE,
    KSCAN_PERIOD,
    KSCAN_POWER,
    KSCAN_PRINT,
    KSCAN_PRINTSCREEN,
    KSCAN_Q,
    KSCAN_R,
    KSCAN_RALT,
    KSCAN_RCTRL,
    KSCAN_RETURN,
    KSCAN_RGUI,
    KSCAN_RIGHT,
    KSCAN_RIGHTBRACKET,
    KSCAN_RMETA,
    KSCAN_RSHIFT,
    KSCAN_RSUPER,
    KSCAN_S,
    KSCAN_SCROLLLOCK,
    KSCAN_SCROLLOCK,
    KSCAN_SEMICOLON,
    KSCAN_SLASH,
    KSCAN_SPACE,
    KSCAN_SYSREQ,
    KSCAN_T,
    KSCAN_TAB,
    KSCAN_U,
    KSCAN_UNKNOWN,
    KSCAN_UP,
    KSCAN_V,
    KSCAN_W,
    KSCAN_X,
    KSCAN_Y,
    KSCAN_Z,
    K_0,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_9,
    K_AC_BACK,
    K_AMPERSAND,
    K_ASTERISK,
    K_AT,
    K_BACKQUOTE,
    K_BACKSLASH,
    K_BACKSPACE,
    K_BREAK,
    K_CAPSLOCK,
    K_CARET,
    K_CLEAR,
    K_COLON,
    K_COMMA,
    K_CURRENCYSUBUNIT,
    K_CURRENCYUNIT,
    K_DELETE,
    K_DOLLAR,
    K_DOWN,
    K_END,
    K_EQUALS,
    K_ESCAPE,
    K_EURO,
    K_EXCLAIM,
    K_F1,
    K_F10,
    K_F11,
    K_F12,
    K_F13,
    K_F14,
    K_F15,
    K_F2,
    K_F3,
    K_F4,
    K_F5,
    K_F6,
    K_F7,
    K_F8,
    K_F9,
    K_GREATER,
    K_HASH,
    K_HELP,
    K_HOME,
    K_INSERT,
    K_KP0,
    K_KP1,
    K_KP2,
    K_KP3,
    K_KP4,
    K_KP5,
    K_KP6,
    K_KP7,
    K_KP8,
    K_KP9,
    K_KP_0,
    K_KP_1,
    K_KP_2,
    K_KP_3,
    K_KP_4,
    K_KP_5,
    K_KP_6,
    K_KP_7,
    K_KP_8,
    K_KP_9,
    K_KP_DIVIDE,
    K_KP_ENTER,
    K_KP_EQUALS,
    K_KP_MINUS,
    K_KP_MULTIPLY,
    K_KP_PERIOD,
    K_KP_PLUS,
    K_LALT,
    K_LCTRL,
    K_LEFT,
    K_LEFTBRACKET,
    K_LEFTPAREN,
    K_LESS,
    K_LGUI,
    K_LMETA,
    K_LSHIFT,
    K_LSUPER,
    K_MENU,
    K_MINUS,
    K_MODE,
    K_NUMLOCK,
    K_NUMLOCKCLEAR,
    K_PAGEDOWN,
    K_PAGEUP,
    K_PAUSE,
    K_PERCENT,
    K_PERIOD,
    K_PLUS,
    K_POWER,
    K_PRINT,
    K_PRINTSCREEN,
    K_QUESTION,
    K_QUOTE,
    K_QUOTEDBL,
    K_RALT,
    K_RCTRL,
    K_RETURN,
    K_RGUI,
    K_RIGHT,
    K_RIGHTBRACKET,
    K_RIGHTPAREN,
    K_RMETA,
    K_RSHIFT,
    K_RSUPER,
    K_SCROLLLOCK,
    K_SCROLLOCK,
    K_SEMICOLON,
    K_SLASH,
    K_SPACE,
    K_SYSREQ,
    K_TAB,
    K_UNDERSCORE,
    K_UNKNOWN,
    K_UP,
    K_a,
    K_b,
    K_c,
    K_d,
    K_e,
    K_f,
    K_g,
    K_h,
    K_i,
    K_j,
    K_k,
    K_l,
    K_m,
    K_n,
    K_o,
    K_p,
    K_q,
    K_r,
    K_s,
    K_t,
    K_u,
    K_v,
    K_w,
    K_x,
    K_y,
    K_z,
    LIL_ENDIAN,
    LOCALECHANGED,
    MIDIIN,
    MIDIOUT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION,
    MOUSEWHEEL,
    MULTIGESTURE,
    NOEVENT,
    NOFRAME,
    NUMEVENTS,
    OPENGL,
    OPENGLBLIT,
    PREALLOC,
    QUIT,
    RENDER_DEVICE_RESET,
    RENDER_TARGETS_RESET,
    RESIZABLE,
    RLEACCEL,
    RLEACCELOK,
    Rect,
    SCALED,
    SCRAP_BMP,
    SCRAP_CLIPBOARD,
    SCRAP_PBM,
    SCRAP_PPM,
    SCRAP_SELECTION,
    SCRAP_TEXT,
    SHOWN,
    SRCALPHA,
    SRCCOLORKEY,
    SWSURFACE,
    SYSTEM_CURSOR_ARROW,
    SYSTEM_CURSOR_CROSSHAIR,
    SYSTEM_CURSOR_HAND,
    SYSTEM_CURSOR_IBEAM,
    SYSTEM_CURSOR_NO,
    SYSTEM_CURSOR_SIZEALL,
    SYSTEM_CURSOR_SIZENESW,
    SYSTEM_CURSOR_SIZENS,
    SYSTEM_CURSOR_SIZENWSE,
    SYSTEM_CURSOR_SIZEWE,
    SYSTEM_CURSOR_WAIT,
    SYSTEM_CURSOR_WAITARROW,
    SYSWMEVENT,
    TEXTEDITING,
    TEXTINPUT,
    TIMER_RESOLUTION,
    USEREVENT,
    USEREVENT_DROPFILE,
    VIDEOEXPOSE,
    VIDEORESIZE,
    WINDOWCLOSE,
    WINDOWDISPLAYCHANGED,
    WINDOWENTER,
    WINDOWEXPOSED,
    WINDOWFOCUSGAINED,
    WINDOWFOCUSLOST,
    WINDOWHIDDEN,
    WINDOWHITTEST,
    WINDOWICCPROFCHANGED,
    WINDOWLEAVE,
    WINDOWMAXIMIZED,
    WINDOWMINIMIZED,
    WINDOWMOVED,
    WINDOWRESIZED,
    WINDOWRESTORED,
    WINDOWSHOWN,
    WINDOWSIZECHANGED,
    WINDOWTAKEFOCUS,
)

ALTS = ((K_v, "√"), (K_p, "π"), (K_t, "±"), (K_EQUALS, "≠"))
SHIFTS = (
    (K_5, "%"),
    (K_6, "^"),
    (K_8, "*"),
    (K_9, "("),
    (K_0, ")"),
    (K_EQUALS, "+"),
    (K_COMMA, "<"),
    (K_PERIOD, ">"),
    (K_a, "A"),
    (K_b, "B"),
    (K_c, "C"),
    (K_d, "D"),
    (K_e, "E"),
    (K_f, "F"),
    (K_g, "G"),
    (K_h, "H"),
    (K_i, "I"),
    (K_j, "J"),
    (K_k, "K"),
    (K_l, "L"),
    (K_m, "M"),
    (K_n, "N"),
    (K_o, "O"),
    (K_p, "P"),
    (K_q, "Q"),
    (K_r, "R"),
    (K_s, "S"),
    (K_t, "T"),
    (K_u, "U"),
    (K_v, "V"),
    (K_w, "W"),
    (K_x, "X"),
    (K_y, "Y"),
    (K_z, "Z"),
    (K_MINUS, "_"),
)
SWITCH = (
    ("√", "sqrt"),
    ("^", "**"),
    ("%", "*0.01"),
    ("π", "pi"),
    ("+-", "±"),
    #   ('=', "=="),
    ("≠", "!="),
)

import os
import pickle
import pyperclip
import re
import sys
import time
import traceback
import functools
import typing

import src

# change directory to assets
INIT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
ASSETS = os.path.join(INIT_DIR, "assets")

# logger initiation
DEBUG_FILE = os.path.join(INIT_DIR, "debug", f"debug_{time.time()}.log")
if not os.path.exists(os.path.join(INIT_DIR, "debug")):
    os.makedirs(os.path.join(INIT_DIR, "debug"))
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=DEBUG_FILE,
    level=logging.DEBUG,
    format="%(funcName)s:%(message)s",
)

# pygame display initiation
pygame.init()

pygame.key.set_repeat(300, 80)

display_width = 1200
display_height = 720

display = pygame.display.set_mode((display_width, display_height), RESIZABLE)
pygame.display.set_caption(os.path.join(ASSETS, "YEquals"))
icon_img = pygame.image.load(os.path.join(ASSETS, "icon.png"))
pygame.display.set_icon(icon_img)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)
logo_img = pygame.image.load(os.path.join(ASSETS, "quarkgame_logo.png"))
tab_banner_img = pygame.image.load(os.path.join(ASSETS, "tab_banner.png"))

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
RELA_TAB = 4

FPS = 30
SCALE_DX = 80
SCALE_DY = 80
SCALE_RATIO = 1.2

SS_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "screenshot.jpg")
FULL_EXP = r"(?P<exp>.+)\[(?P<domain>.+)\]\s*$"
COE_PAIR = r"[\d\)\w_]x|x\(|\)x"
VAR_EXP = r"(?P<vname>[\w|_]+)\s?=\s?(?P<value>\S+)\s*$"
FILE_PATH = r"(\w+)/?(\w+)"
PARENTHESIS = {"(": ")", "[": "]", "{": "}"}
CLOSE_PAREN = (")", "]", "}")


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
            with open(self.fname, "rb") as f:
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
            logger.info("File %s is properly loaded", self.fname)
        except Exception as e:
            message.put_delayed(display, "Error occured while loading data")
            logger.error("File %s is not properly loaded", self.fname)

    def put(self):
        try:
            with open(self.fname, "wb") as f:
                Tab.visible = True
                pickle.dump(Func.family, f)
                pickle.dump(Var.family, f)
                pickle.dump(coor.scalex, f)
                pickle.dump(coor.scaley, f)
                pickle.dump(coor.origin, f)
                pickle.dump(coor.axis_show, f)
                pickle.dump(coor.grid_show, f)
            logger.info("File %s properly saved", self.fname)
        except Exception as e:
            message.put_delayed(display, "Error occured while saving data")
            logger.error("File %s not properly saved", self.fname)

    @staticmethod
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
        coor.chori((self.origin[0] - mouse_x) / old_scalex * (value - old_scalex), 0)
        self._scalex = value

    @property
    def scaley(self):
        return self._scaley

    @scaley.setter
    def scaley(self, value):
        old_scaley = self._scaley
        mouse_y = pygame.mouse.get_pos()[1]
        coor.chori(0, (self.origin[1] - mouse_y) / old_scaley * (value - old_scaley))
        self._scaley = value

    def chori(self, move_x, move_y):
        self.origin[0] += move_x
        self.origin[1] += move_y

    def axis(self):
        if self.axis_show:
            pygame.draw.line(
                display,
                RED,
                (0, self.origin[1]),
                (display_width, self.origin[1]),
                Coordinate._stroke_width,
            )
            pygame.draw.line(
                display,
                RED,
                (self.origin[0], 0),
                (self.origin[0], display_height),
                Coordinate._stroke_width,
            )

    def grid(self):
        if not self.grid_show:
            return

        def sig_figure(x, fig):
            return round(x, fig - int(math.floor(math.log10(abs(x)))) - 1)

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
        for line_x in range(
            (ori_x - left_lim) % gap_px + left_lim, display_width, gap_px
        ):
            pygame.draw.line(
                display,
                GREY,
                (line_x, 0),
                (line_x, display_height),
                Coordinate._stroke_width,
            )
            val = (line_x - ori_x) / coor.scalex
            if val != 0:
                val = sig_figure(val, 2)
                message.label(line_x, label_y, val)
            else:
                message.label(line_x, label_y, 0)
        for line_y in range(ori_y % gap_py, display_height, gap_py):
            pygame.draw.line(
                display,
                GREY,
                (0, line_y),
                (display_width, line_y),
                Coordinate._stroke_width,
            )
            val = (ori_y - line_y) / coor.scaley
            if val != 0:
                val = sig_figure(val, 2)
                message.label(label_x, line_y, val)


class Var:

    VAR_EXP_MATCH = 0
    VAR_EXP_NAME = 1
    VAR_EXP_VALUE = 2
    VAR_EXP_LEGAL = 3
    limit = 8
    family = []
    vars = {}
    active: typing.Optional[typing.Self] = None
    _act_index = 0

    def __init__(self, expression: str = ""):
        if len(Var.family) < Var.limit:
            self._exp = ""
            self._vname = None
            self._value = None
            self.exp = expression
            self.cursor = len(expression)
            self.visible = True
            Var.family.append(self)
            Var.set_active(len(Var.family) - 1)
        else:
            message.put_delayed(display, "Maximum variable limit exceeded")

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp = value
        self.legal_check()
        if self.legality != Var.VAR_EXP_LEGAL and self._vname in Var.vars:
            del Var.vars[self._vname]
        elif self.legality == Var.VAR_EXP_LEGAL:
            Var.vars[self._vname] = self._value

    @staticmethod
    def set_active(index):
        if index == "u":
            if Var._act_index > 0:
                Var._act_index -= 1
                Var.active = Var.family[Var._act_index]
        elif index == "d":
            if Var._act_index < len(Var.family) - 1:
                Var._act_index += 1
                Var.active = Var.family[Var._act_index]
        elif Var.family:
            Var.active = Var.family[index]
            Var._act_index = index
        else:
            Var.active = None

    @staticmethod
    def remove():
        if Var.family:
            index = Var.family.index(Var.active)
            Var.family.remove(Var.active)
            if index == len(Var.family):
                Var.set_active(index - 1)
            else:
                Var.set_active(index)
        else:
            message.put_delayed(display, "No variable to remove")

    @staticmethod
    def move_cursor(move: int):
        var = Var.active
        assert var is not None
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

    @staticmethod
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
        var.exp = var.exp[0 : var.cursor] + char + var.exp[var.cursor :]
        var.cursor += len(char)
        if char in PARENTHESIS:
            close = PARENTHESIS[char]
            var.exp = var.exp[0 : var.cursor] + close + var.exp[var.cursor :]

    @staticmethod
    def delete():
        if not Var.active:
            message.put_delayed(display, "No variable has been created")
            return
        var = Var.active
        if var.cursor != 0:
            var.exp = var.exp[: var.cursor - 1] + var.exp[var.cursor :]
            var.cursor -= 1

    def legal_check(self):
        # determine legality of a variable expression
        exp_match = re.match(VAR_EXP, self.exp)
        if not exp_match:
            self.legality = Var.VAR_EXP_MATCH
        else:
            self._vname = exp_match.group("vname")
            self._value = exp_match.group("value")
            if not var_name(self._vname):
                self.legality = Var.VAR_EXP_NAME
            elif not is_int(self._value):
                self.legality = Var.VAR_EXP_VALUE
            else:
                self.legality = Var.VAR_EXP_LEGAL
        return self.legality

    def show(self):
        if Var.active == self:
            message.put(
                display,
                "var: " + self.exp[: self.cursor] + "|" + self.exp[self.cursor :],
            )
        else:
            message.put(display, "var: " + self.exp)

        # display variable status
        if self.legality == Var.VAR_EXP_MATCH:
            msg = "The variable expression is illegal"
        elif self.legality == Var.VAR_EXP_NAME:
            msg = "The name of the variable is illegal"
        elif self.legality == Var.VAR_EXP_VALUE:
            msg = "The value of the variable is illegal"
        elif self.legality == Var.VAR_EXP_LEGAL:
            msg = "The variable is legal"
        else:
            msg = "Unknown message"
        message.indent()
        message.put(display, msg)
        message.unindent()

    def __del__(self):
        del Var.vars[self._vname]


class Func:
    limit = 8
    family = []
    active: typing.Optional[typing.Self] = None
    _act_index = 0
    _accuracy = 1
    _stroke_width = 2

    def __init__(self, exp: str = ""):
        if len(Func.family) < Func.limit:
            self.exp = exp
            self.cursor = len(exp)
            self.visible = True
            Func.family.append(self)
            Func.set_active(len(Func.family) - 1)
        else:
            message.put_delayed(display, "Maximum graph exceeded")

    @staticmethod
    def set_active(index):
        if index == "u":
            if Func._act_index > 0:
                Func._act_index -= 1
                Func.active = Func.family[Func._act_index]
        elif index == "d":
            if Func._act_index < len(Func.family) - 1:
                Func._act_index += 1
                Func.active = Func.family[Func._act_index]
        elif Func.family:
            Func.active = Func.family[index]
            Func._act_index = index
        else:
            Func.active = None

    @staticmethod
    def remove():
        if Func.family:
            index = Func.family.index(Func.active)
            Func.family.remove(Func.active)
            if index == len(Func.family):
                Func.set_active(index - 1)
            else:
                Func.set_active(index)
        else:
            message.put_delayed(display, "No graph expression to remove")

    @staticmethod
    def move_cursor(move):
        function = Func.active
        assert function is not None
        if move == -1:
            if function.cursor > 0:
                function.cursor -= 1
        elif move == 1:
            if function.cursor < len(function.exp):
                function.cursor += 1
        if move == -2:
            if function.cursor > 0:
                function.cursor = 0
        elif move == 2:
            if function.cursor < len(function.exp):
                function.cursor = len(function.exp)

    @staticmethod
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
        func.exp = func.exp[0 : func.cursor] + char + func.exp[func.cursor :]
        func.cursor += len(char)
        if char in PARENTHESIS:
            close = PARENTHESIS[char]
            func.exp = func.exp[0 : func.cursor] + close + func.exp[func.cursor :]

    @staticmethod
    def delete():
        if not Func.active:
            message.put_delayed(display, "No expression has been created")
            return
        func = Func.active
        if func.cursor != 0:
            func.exp = func.exp[: func.cursor - 1] + func.exp[func.cursor :]
            func.cursor -= 1

    def true_exp(self):
        exp_match = re.match(FULL_EXP, self.exp)
        if not exp_match:
            exp = self.exp
            domain = ""
        else:
            exp = exp_match.group("exp")
            domain = exp_match.group("domain")
            for switch in SWITCH:
                domain = domain.replace(switch[0], switch[1])

        for switch in SWITCH:
            exp = exp.replace(switch[0], switch[1])
        while re.findall(COE_PAIR, exp):
            for pair in set(re.findall(COE_PAIR, exp)):
                exp = exp.replace(pair, pair[0] + "*" + pair[1])

        if not exp_match:
            return exp
        else:
            return exp, domain

    def draw(self):
        true_exp = self.true_exp()
        if self.visible:
            if type(true_exp) == str:
                if "±" not in true_exp:
                    self.graph(true_exp)
                else:
                    message.indent()
                    self.graph(true_exp.replace("±", "+"))
                    self.graph(true_exp.replace("±", "-"))
                    message.unindent()
            else:
                exp, domain = true_exp
                if "±" not in exp:
                    self.graph(exp, domain)
                else:
                    message.indent()
                    self.graph(exp.replace("±", "+"), domain)
                    self.graph(exp.replace("±", "-"), domain)
                    message.unindent()

    def graph(self, exp, domain="True"):
        self.drawability = 1

        # check if the expression is function or relation
        if len(exp.split("=")) != 2:
            self.drawability = 0
            return
        pairs = None
        if "y" in exp.split("=")[0:2]:
            exp = exp.split("=")[1] if "y" == exp.split("=")[0] else exp.split("=")[0]
            if "y" not in exp:
                pairs = src.yeval.y_equals(exp, coor)
        if not pairs:
            pairs = src.yeval.xyre(exp, coor)

        # check for errors
        if pairs is None:
            return

        # loop through coordinate pairs
        for pair in pairs:

            # draw line
            pygame.draw.line(display, BLACK, *pair, Func._stroke_width)

        # return
        return

    def show(self):
        # display expression
        if pygame.key.get_pressed()[K_TAB]:
            message.put(display, "y = " + str(self.true_exp()))
        else:
            if Func.active == self:
                message.put(
                    display, f"{self.exp[:self.cursor]}|{self.exp[self.cursor:]}"
                )
            else:
                message.put(display, self.exp)

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
        pygame.draw.rect(display, LIGHT_BLUE, (0, 0, Tab.width, display_height))
        for func in Func.family:
            func.show()

    def var_tab(self):
        pygame.draw.rect(display, LIGHT_GREEN, (0, 0, Tab.width, display_height))
        for var in Var.family:
            var.show()

    def view_tab(self):
        pygame.draw.rect(display, LIGHT_YELLOW, (0, 0, Tab.width, display_height))

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


data = File(os.path.join(ASSETS, "data.p"))
message = Message()
coor = Coordinate()
tab = Tab()


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
    elif literal in ["x", "y"]:
        return False
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
    with open(os.path.join(ASSETS, "shortcuts.txt"), "r") as f:
        shortcuts = [line.replace("\n", "") for line in f.readlines()]

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

            # if key press
            if event.type == KEYDOWN:

                # cmd / ctrl + shift
                if (mods & KMOD_META and mods & KMOD_SHIFT) or (
                    mods & KMOD_CTRL and mods & KMOD_SHIFT
                ):
                    if event.key == K_MINUS:
                        coor.scalex /= SCALE_RATIO
                        coor.scaley /= SCALE_RATIO
                    elif event.key == K_EQUALS:
                        coor.scalex *= SCALE_RATIO
                        coor.scaley *= SCALE_RATIO
                    elif event.key == K_c:
                        File.screenshot()

                # cmd / ctrl
                elif (mods & KMOD_META) or (mods & KMOD_CTRL):
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
                            coor.origin = [
                                display_width / 2 + Tab.width / 2,
                                display_height / 2,
                            ]
                        else:
                            coor.origin = [
                                display_width / 2,
                                display_height / 2,
                            ]
                    elif event.key == K_9:
                        ave = (coor.scalex + coor.scaley) / 2
                        coor.scalex, coor.scaley = ave, ave
                    elif event.key == K_8:
                        if tab.visible:
                            coor.origin = [
                                display_width / 2 + Tab.width / 2,
                                display_height / 2,
                            ]
                        else:
                            coor.origin = [display_width / 2, display_height / 2]
                    elif event.key == K_BACKSPACE:
                        if tab.visible == FUNC_TAB:
                            Func.remove()
                        if tab.visible == VAR_TAB:
                            Var.remove()
                    elif event.key == K_RETURN:
                        if tab.visible == FUNC_TAB:
                            Func("")
                        elif tab.visible == VAR_TAB:
                            Var("")
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
                            assert func is not None
                            pyperclip.copy(func.exp)
                    elif event.key == K_v:
                        if tab.visible == FUNC_TAB:
                            assert func is not None
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
                        Func.set_active("u")
                    elif event.key == K_DOWN:
                        Func.set_active("d")
                    elif event.key == K_RETURN:
                        if not Func.active:
                            message.put_delayed(display, "No expression available")
                        else:
                            assert func is not None
                            func.visible = not func.visible
                    elif event.key == K_SPACE:
                        Func.insert(" ")
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
                        Var.set_active("u")
                    elif event.key == K_DOWN:
                        Var.set_active("d")
                    elif event.key == K_RETURN:
                        if not Var.active:
                            message.put_delayed(display, "No expression available")
                        else:
                            assert var is not None
                            var.visible = not var.visible
                    elif event.key == K_SPACE:
                        Var.insert(" ")
                    # basic input
                    else:
                        k_name = pygame.key.name(event.key)
                        if not mods and len(k_name) == 1:
                            Var.insert(pygame.key.name(event.key))
            elif event.type == MOUSEBUTTONDOWN:
                # if mods & KMOD_SHIFT:
                if event.button == 4:
                    coor.scalex //= SCALE_RATIO
                    coor.scaley //= SCALE_RATIO
                elif event.button == 5:
                    coor.scalex *= SCALE_RATIO
                    coor.scaley *= SCALE_RATIO
            elif event.type == VIDEORESIZE:
                tab.resize_win(event.w, event.h)

        # mouse control
        mods = pygame.key.get_mods()
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if (mods & KMOD_META) or (mods & KMOD_CTRL):
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

    line_num = 0

    while show:

        for event in pygame.event.get():
            mods = pygame.key.get_mods()
            if (mods & KMOD_META) or (mods & KMOD_CTRL):
                if event.type == KEYDOWN and event.key == K_q:
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
        line_num = (display_height - 10) / message.line_height - 1
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
    # This isn't used anywhere?
    raise Exception("Error function called")
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
    sys.exit()


if __name__ == "__main__":
    main()
