import math
import pygame
import enum
import logging
import os
import pickle
import pyperclip
import re
import sys
import time
import traceback
import functools
import typing
import dataclasses
import fractions
import numpy

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


DISPLAY_WIDTH = 1200
DISPLAY_HEIGHT = 720


# change directory to assets
INIT_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
ASSETS = os.path.join(INIT_DIR, "assets")

# logger initiation
DEBUG_FILE = os.path.join(INIT_DIR, "debug", f"debug_{time.time()}.log")
if not os.path.exists(os.path.join(INIT_DIR, "debug")):
    os.makedirs(os.path.join(INIT_DIR, "debug"))
logger = logging.getLogger(__name__)
logging.basicConfig(filename=DEBUG_FILE, level=logging.DEBUG, format="%(funcName)s:%(message)s")

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
SCALE_RATIO = fractions.Fraction(12, 10)

SCREENSHOT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "screenshot.jpg")
FULL_EXP = r"(?P<exp>.+)\[(?P<domain>.+)\]\s*$"
COE_PAIR = r"[\d\)\w_]x|x\(|\)x"
VAR_EXP = r"(?P<vname>[\w|_]+)\s?=\s?(?P<value>\S+)\s*$"
FILE_PATH = r"(\w+)/?(\w+)"
PARENTHESIS = {"(": ")", "[": "]", "{": "}"}
CLOSE_PARENTHESIS = (")", "]", "}")


@dataclasses.dataclass
class Point:
    """
    Stores raw points

    Attributes:
        x: x coordinate
        y: y coordinate
    """

    x: numpy.float128
    y: numpy.float128


@dataclasses.dataclass
class DisplayPoint:
    """
    Stores points for display

    Attributes:
        x: x coordinate
        y: y coordinate
    """

    x: int
    y: int


class Message:
    @dataclasses.dataclass
    class DelayedMessage:
        surface: pygame.Surface
        text: str
        time: int

    limit = 5
    delayed_messages: list[DelayedMessage] = []

    def __init__(self) -> None:
        self.reset()
        self.font = pygame.font.Font(None, 21)
        self.label_font = pygame.font.Font(None, 19)

    def label(self, x: int, y: int, text_string: str, color: tuple[int, int, int] = DARK_GREY) -> None:
        text_string = str(text_string)
        text_bitmap = self.label_font.render(text_string, True, color)
        text_rect = text_bitmap.get_rect()
        left_most = Tab.width if tab.visible else 0
        if x < left_most:
            x = left_most
        elif x > display_width - text_rect.width:
            x = display_width - text_rect.width
        if y < 0:
            y = 0
        elif y > display_height - text_rect.height:
            y = display_height - text_rect.height
        display.blit(text_bitmap, [x + 1, y + 1])

    def put(self, screen: pygame.Surface, text_string: str, color: tuple[int, int, int] = BLACK) -> None:
        text_bitmap = self.font.render(text_string, True, color)
        screen.blit(text_bitmap, [self.x, self.y])
        self.y += self.line_height

    def put_delayed(self, screen: pygame.Surface, text_string: str, show_time: int = 1) -> None:
        Message.delayed_messages.append(Message.DelayedMessage(screen, text_string, show_time * FPS))

    def show_delayed(self) -> None:
        if len(Message.delayed_messages) >= Message.limit:
            del Message.delayed_messages[:-5]
        if len(Message.delayed_messages) != 0:
            self.put(display, "Information")
            self.indent()
            for message in Message.delayed_messages:
                self.put(message.surface, message.text)
                message.time -= 1
                if message.time <= 0:
                    Message.delayed_messages.remove(message)
            self.unindent()

    def reset(self) -> None:
        self.x = 10
        self.y = 10
        self.line_height = 18

    def indent(self) -> None:
        self.x += 15

    def unindent(self) -> None:
        self.x -= 15
        pygame.draw.line(display, DARK_GREY, (0, self.y), (Tab.width, self.y))
        self.y += 2


class File:
    def __init__(self, fname: str) -> None:
        self.fname = fname

    def get(self) -> None:
        try:
            with open(self.fname, "rb") as file:
                Func.family = pickle.load(file)
                Variable.family = pickle.load(file)
                # coordinates.scale_x = pickle.load(f)
                Coordinates.set_scale_x(pickle.load(file))
                # coordinates.scale_y = pickle.load(f)
                Coordinates.set_scale_y(pickle.load(file))
                # coordinates.origin = pickle.load(f)
                Coordinates.set_origin(pickle.load(file))
                # coordinates.axis_show = pickle.load(f)
                Coordinates.set_axis_show(pickle.load(file))
                # coordinates.grid_show = pickle.load(f)
                Coordinates.set_grid_show(pickle.load(file))
            if Func.family:
                Func.active = Func.family[Func._act_index]
            if Variable.family:
                for var in Variable.family:
                    var.exp = var.exp
                Variable.active = Variable.family[Variable._act_index]
            logger.info("File %s is properly loaded", self.fname)
        except Exception as e:
            message.put_delayed(display, "Error occured while loading data")
            logger.error("File %s is not properly loaded", self.fname)

    def put(self) -> None:
        try:
            with open(self.fname, "wb") as file:
                # Tab.visible = True # ????
                pickle.dump(Func.family, file)
                pickle.dump(Variable.family, file)
                # pickle.dump(coordinates.scale_x, f)
                pickle.dump(Coordinates.get_scale_x(), file)
                # pickle.dump(coordinates.scale_y, f)
                pickle.dump(Coordinates.get_scale_y(), file)
                # pickle.dump(coordinates.origin, f)
                pickle.dump(Coordinates.get_origin(), file)
                # pickle.dump(coordinates.axis_show, f)
                pickle.dump(Coordinates.get_axis_show(), file)
                # pickle.dump(coordinates.grid_show, f)
                pickle.dump(Coordinates.get_grid_show(), file)
            logger.info("File %s properly saved", self.fname)
        except Exception as e:
            message.put_delayed(display, "Error occured while saving data")
            logger.error("File %s not properly saved", self.fname)

    @staticmethod
    def screenshot() -> None:
        pygame.image.save(display, SCREENSHOT_PATH)


class Tab:
    width: typing.ClassVar[int] = 300

    def __init__(self) -> None:
        self._visible: int | bool | None = True

    @property
    def visible(self) -> int | bool | None:
        return self._visible

    @visible.setter
    def visible(self, value: int | bool | None) -> None:
        temp = self._visible
        self._visible = value
        if not tab._visible:
            # coordinates.move_origin(-Tab.width // 2, 0)
            Coordinates.move_origin(-Tab.width // 2, 0)
        elif not temp:
            # coordinates.move_origin(Tab.width // 2, 0)
            Coordinates.move_origin(Tab.width // 2, 0)

    def show_tab(self) -> None:
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

    def func_tab(self) -> None:
        pygame.draw.rect(display, LIGHT_BLUE, (0, 0, Tab.width, display_height))
        for func in Func.family:
            func.show()

    def var_tab(self) -> None:
        pygame.draw.rect(display, LIGHT_GREEN, (0, 0, Tab.width, display_height))
        for var in Variable.family:
            var.show()

    def view_tab(self) -> None:
        pygame.draw.rect(display, LIGHT_YELLOW, (0, 0, Tab.width, display_height))

    def resize_win(self, width: int, height: int) -> None:
        global display_width, display_height
        old_size = display.get_rect()
        old_w, old_h = old_size.right, old_size.bottom
        if width < 800:
            width = 800
            message.put_delayed(display, "minimal window width is 800")
        if height < 600:
            height = 600
            message.put_delayed(display, "minimal window height is 600")
        display_width, display_height = width, height
        pygame.display.set_mode((width, height), RESIZABLE)
        # coordinates.move_origin((w - old_w) // 2, (h - old_h) // 2)
        Coordinates.move_origin((width - old_w) // 2, (height - old_h) // 2)


class Coordinates:
    _stroke_width: typing.ClassVar[int] = 2
    _scale_x: typing.ClassVar[fractions.Fraction] = fractions.Fraction(SCALE_DX)
    _scale_y: typing.ClassVar[fractions.Fraction] = fractions.Fraction(SCALE_DY)
    _origin: typing.ClassVar[DisplayPoint] = DisplayPoint(display_width // 2 + Tab.width // 2, display_height // 2)
    _axis_show: typing.ClassVar[bool] = True
    _grid_show: typing.ClassVar[bool] = True

    def __init__(self) -> None:
        raise Exception("This class is not supposed to be instantiated")

    @staticmethod
    def get_scale_x() -> fractions.Fraction:
        return Coordinates._scale_x

    @staticmethod
    def set_scale_x(scale_x: fractions.Fraction) -> None:
        old_scale_x = Coordinates._scale_x
        mouse_x = pygame.mouse.get_pos()[0]
        Coordinates.move_origin((Coordinates._origin.x - mouse_x) // int(old_scale_x / (scale_x - old_scale_x)), 0)
        Coordinates._scale_x = scale_x

    @staticmethod
    def get_scale_y() -> fractions.Fraction:
        return Coordinates._scale_y

    @staticmethod
    def set_scale_y(value: fractions.Fraction) -> None:
        old_scale_y = Coordinates._scale_y
        mouse_y = pygame.mouse.get_pos()[1]
        Coordinates.move_origin(0, (Coordinates._origin.y - mouse_y) // int(old_scale_y / (value - old_scale_y)))
        Coordinates._scale_y = value

    @staticmethod
    def update_scale_x(value: fractions.Fraction) -> fractions.Fraction:
        # Updates only x and returns the new value
        Coordinates._scale_x *= value
        return Coordinates._scale_x

    @staticmethod
    def update_scale_y(value: fractions.Fraction) -> fractions.Fraction:
        # Updates only y and returns the new value
        Coordinates._scale_y *= value
        return Coordinates._scale_y

    @staticmethod
    def update_scale(value: fractions.Fraction) -> tuple[fractions.Fraction, fractions.Fraction]:
        # Updates both x and y and returns the new value
        Coordinates._scale_x *= value
        Coordinates._scale_y *= value
        return Coordinates._scale_x, Coordinates._scale_y

    @staticmethod
    def get_origin() -> DisplayPoint:
        return Coordinates._origin

    @staticmethod
    def set_origin(value: DisplayPoint) -> None:
        assert isinstance(value, DisplayPoint)
        Coordinates._origin = value

    @staticmethod
    def get_axis_show() -> bool:
        return Coordinates._axis_show

    @staticmethod
    def set_axis_show(value: bool) -> None:
        Coordinates._axis_show = value

    @staticmethod
    def toggle_axis_show() -> None:
        Coordinates._axis_show = not Coordinates._axis_show

    @staticmethod
    def get_grid_show() -> bool:
        return Coordinates._grid_show

    @staticmethod
    def set_grid_show(value: bool) -> None:
        Coordinates._grid_show = value

    @staticmethod
    def toggle_grid_show() -> None:
        Coordinates._grid_show = not Coordinates._grid_show

    @staticmethod
    def reset_origin(tab_visibility: bool) -> None:
        Coordinates._origin.x = display_width // 2 + Tab.width // 2 if tab_visibility else display_width // 2
        Coordinates._origin.y = display_height // 2

    @staticmethod
    def move_origin(x: int, y: int) -> None:
        Coordinates._origin.x += x
        Coordinates._origin.y += y

    @staticmethod
    def axis() -> None:
        if Coordinates._axis_show:
            pygame.draw.line(display, RED, (0, Coordinates._origin.y), (display_width, Coordinates._origin.y), Coordinates._stroke_width)
            pygame.draw.line(display, RED, (Coordinates._origin.x, 0), (Coordinates._origin.x, display_height), Coordinates._stroke_width)

    @staticmethod
    def grid() -> None:
        if not Coordinates._grid_show:
            return

        # initiate value
        # ori_x, ori_y = coordinates.origin.x, coordinates.origin.y
        gap_x, gap_y = SCALE_DX / Coordinates._scale_x, SCALE_DY / Coordinates._scale_y
        gap_px = int(gap_x * Coordinates._scale_x)
        gap_py = int(gap_y * Coordinates._scale_y)
        label_x, label_y = Coordinates._origin.x, Coordinates._origin.y
        left_lim = Tab.width if tab.visible else 0

        # draw grid
        for line_x in range((Coordinates._origin.x - left_lim) % gap_px + left_lim, display_width, gap_px):
            pygame.draw.line(display, GREY, (line_x, 0), (line_x, display_height), Coordinates._stroke_width)
            value = numpy.float128((line_x - Coordinates._origin.x) / Coordinates._scale_x)
            message.label(line_x, label_y, lable_number(value))
            # val: fractions.Fraction = (line_x - Coordinates._origin.x) / Coordinates._scale_x
            # if val != 0:
            #     message.label(line_x, label_y, str(sig_figure(val, 2)))
            # else:
            #     message.label(line_x, label_y, str(0))
        for line_y in range(Coordinates._origin.y % gap_py, display_height, gap_py):
            pygame.draw.line(display, GREY, (0, line_y), (display_width, line_y), Coordinates._stroke_width)
            val = numpy.float128((Coordinates._origin.y - line_y) / Coordinates._scale_y)
            if val != 0:
                message.label(label_x, line_y, lable_number(val))
                # message.label(label_x, line_y, str(sig_figure(val, 2)))


class Variable:
    class VariableLegality(enum.Enum):
        VARIBLE_EXPRESSION_ILLEGAL = 0
        VARIABLE_NAME_ILLEGAL = 1
        VARIABLE_VALUE_ILLEGAL = 2
        VARIABLE_LEGAL = 3

    limit = 8
    family: typing.ClassVar[list[typing.Self]] = []
    vars: dict[typing.Optional[str], typing.Optional[str]] = {}
    active: typing.ClassVar[typing.Optional[typing.Self]] = None
    _act_index: typing.ClassVar[int] = 0

    def __init__(self, expression: str = ""):
        if len(Variable.family) < Variable.limit:
            self._expression = ""
            self._variable_name: typing.Optional[str] = None
            self._value: typing.Optional[str] = None
            self.expression = expression
            self.cursor = len(expression)
            self.visible = True
            self.legality: Variable.VariableLegality = Variable.VariableLegality.VARIBLE_EXPRESSION_ILLEGAL
            Variable.family.append(self)
            Variable.set_active(len(Variable.family) - 1)
        else:
            message.put_delayed(display, "Maximum variable limit exceeded")

    @property
    def expression(self) -> str:
        return self._expression

    @expression.setter
    def expression(self, value: str) -> None:
        self._expression = value
        self.legal_check()
        if self.legality != Variable.VariableLegality.VARIABLE_LEGAL and self._variable_name in Variable.vars:
            del Variable.vars[self._variable_name]
        elif self.legality == Variable.VariableLegality.VARIABLE_LEGAL:
            Variable.vars[self._variable_name] = self._value

    @staticmethod
    def set_active(index: int | str) -> None:
        if index == "u":
            if Variable._act_index > 0:
                Variable._act_index -= 1
                Variable.active = Variable.family[Variable._act_index]
        elif index == "d":
            if Variable._act_index < len(Variable.family) - 1:
                Variable._act_index += 1
                Variable.active = Variable.family[Variable._act_index]
        elif Variable.family:
            assert isinstance(index, int)
            Variable.active = Variable.family[index]
            Variable._act_index = index
        else:
            Variable.active = None

    @staticmethod
    def remove() -> None:
        if Variable.family:
            assert Variable.active is not None
            index = Variable.family.index(Variable.active)
            Variable.family.remove(Variable.active)
            if index == len(Variable.family):
                Variable.set_active(index - 1)
            else:
                Variable.set_active(index)
        else:
            message.put_delayed(display, "No variable to remove")

    @staticmethod
    def move_cursor(move: int) -> None:
        var = Variable.active
        assert var is not None
        if move == -1:
            if var.cursor > 0:
                var.cursor -= 1
        elif move == 1:
            if var.cursor < len(var.expression):
                var.cursor += 1
        if move == -2:
            if var.cursor > 0:
                var.cursor = 0
        elif move == 2:
            if var.cursor < len(var.expression):
                var.cursor = len(var.expression)

    @staticmethod
    def insert(char: str) -> None:
        if not Variable.active:
            message.put_delayed(display, "No variable has been created")
            return
        var = Variable.active
        if len(var.expression) > 25:
            message.put_delayed(display, "Variable expression too long")
            return
        if char in CLOSE_PARENTHESIS:
            if var.cursor <= len(var.expression) - 1:
                if char == var.expression[var.cursor]:
                    var.cursor += 1
                    return
        var.expression = var.expression[0 : var.cursor] + char + var.expression[var.cursor :]
        var.cursor += len(char)
        if char in PARENTHESIS:
            close = PARENTHESIS[char]
            var.expression = var.expression[0 : var.cursor] + close + var.expression[var.cursor :]

    @staticmethod
    def delete() -> None:
        if not Variable.active:
            message.put_delayed(display, "No variable has been created")
            return
        var = Variable.active
        if var.cursor != 0:
            var.expression = var.expression[: var.cursor - 1] + var.expression[var.cursor :]
            var.cursor -= 1

    def legal_check(self) -> VariableLegality:
        # determine legality of a variable expression
        exp_match = re.match(VAR_EXP, self.expression)
        if not exp_match:
            self.legality = Variable.VariableLegality.VARIBLE_EXPRESSION_ILLEGAL
        else:
            self._variable_name = exp_match.group("vname")
            self._value = exp_match.group("value")
            if not valid_variable_name(self._variable_name):
                self.legality = Variable.VariableLegality.VARIABLE_NAME_ILLEGAL
            elif not is_int(self._value):
                self.legality = Variable.VariableLegality.VARIABLE_VALUE_ILLEGAL
            else:
                self.legality = Variable.VariableLegality.VARIABLE_LEGAL
        return self.legality

    def show(self) -> None:
        if Variable.active == self:
            message.put(display, "var: " + self.expression[: self.cursor] + "|" + self.expression[self.cursor :])
        else:
            message.put(display, "var: " + self.expression)
        match self.legality:
            case Variable.VariableLegality.VARIBLE_EXPRESSION_ILLEGAL:
                msg = "The variable expression is illegal"
            case Variable.VariableLegality.VARIABLE_NAME_ILLEGAL:
                msg = "The name of the variable is illegal"
            case Variable.VariableLegality.VARIABLE_VALUE_ILLEGAL:
                msg = "The value of the variable is illegal"
            case Variable.VariableLegality.VARIABLE_LEGAL:
                msg = "The variable is legal"
        message.indent()
        message.put(display, msg)
        message.unindent()

    def __del__(self) -> None:
        del Variable.vars[self._variable_name]


class Func:
    limit = 8
    family: typing.ClassVar[list[typing.Self]] = []
    active: typing.ClassVar[typing.Optional[typing.Self]] = None
    _act_index: typing.ClassVar[int] = 0
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
    def set_active(index: typing.Union[int, str]) -> None:
        if index == "u":
            if Func._act_index > 0:
                Func._act_index -= 1
                Func.active = Func.family[Func._act_index]
        elif index == "d":
            if Func._act_index < len(Func.family) - 1:
                Func._act_index += 1
                Func.active = Func.family[Func._act_index]
        elif Func.family:
            assert isinstance(index, int)
            Func.active = Func.family[index]
            Func._act_index = index
        else:
            Func.active = None

    @staticmethod
    def remove() -> None:
        if Func.family:
            assert Func.active is not None
            index = Func.family.index(Func.active)
            Func.family.remove(Func.active)
            if index == len(Func.family):
                Func.set_active(index - 1)
            else:
                Func.set_active(index)
        else:
            message.put_delayed(display, "No graph expression to remove")

    @staticmethod
    def move_cursor(move: int) -> None:
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
    def insert(char: str) -> None:
        if not Func.active:
            message.put_delayed(display, "No expression has been created")
            return
        func = Func.active
        if len(func.exp) > 25:
            message.put_delayed(display, "Expression too long")
            return
        if char in CLOSE_PARENTHESIS:
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
    def delete() -> None:
        if not Func.active:
            message.put_delayed(display, "No expression has been created")
            return
        func = Func.active
        if func.cursor != 0:
            func.exp = func.exp[: func.cursor - 1] + func.exp[func.cursor :]
            func.cursor -= 1

    def true_exp(self) -> typing.Union[str, tuple[str, str]]:
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

    def draw(self) -> None:
        true_exp = self.true_exp()
        if self.visible:
            if isinstance(true_exp, str):
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

    def graph(self, expression: str, domain: str = "True") -> None:
        self.drawability = 1

        # check if the expression is function or relation
        if len(expression.split("=")) != 2:
            self.drawability = 0
            return
        pairs = None
        if "y" in expression.split("=")[0:2]:
            expression = expression.split("=")[1] if "y" == expression.split("=")[0] else expression.split("=")[0]
            if "y" not in expression:
                # pairs = y_equals(exp, coordinates)
                pairs = y_equals(expression, Coordinates.get_origin(), Coordinates.get_scale_x(), Coordinates.get_scale_y())
        if not pairs:
            # pairs = xyre(exp, coordinates)
            pairs = xyre(expression, Coordinates.get_origin(), Coordinates.get_scale_x(), Coordinates.get_scale_y())

        # check for errors
        if pairs is None:
            return

        # loop through coordinate pairs
        for pair in pairs:
            a, b = pair

            # draw line
            pygame.draw.line(display, BLACK, a, b, Func._stroke_width)

        # return
        return

    def show(self) -> None:
        # display expression
        if pygame.key.get_pressed()[K_TAB]:
            message.put(display, "y = " + str(self.true_exp()))
        else:
            if Func.active == self:
                message.put(display, f"{self.exp[:self.cursor]}|{self.exp[self.cursor:]}")
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


data = File(os.path.join(ASSETS, "data.p"))
message = Message()
tab = Tab()


def is_int(string: str) -> bool:
    try:
        int(eval(string))
    except Exception as e:
        return False
    else:
        return True


def valid_variable_name(literal: str) -> bool:
    if literal in Variable.vars:
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


# Why would you do this
with open(os.path.join(ASSETS, "shortcuts.txt"), "r") as f:
    shortcuts = [line.replace("\n", "") for line in f.readlines()]


def main() -> None:
    global display_width, display_height, shortcuts

    data.get()
    with open(os.path.join(ASSETS, "shortcuts.txt"), "r") as f:
        shortcuts = [line.replace("\n", "") for line in f.readlines()]

    while True:

        # reset
        message.reset()
        func = Func.active
        var = Variable.active
        corner = pygame.Rect(display_width - 45, 0, 45, 36)

        # pygame event controls
        for event in pygame.event.get():
            logger.debug("event:{}".format(event))
            if event.type == QUIT:
                quit_all()
            modifier_keys = pygame.key.get_mods()

            # if key press
            if event.type == KEYDOWN:

                # cmd / ctrl + shift
                if (modifier_keys & KMOD_META and modifier_keys & KMOD_SHIFT) or (modifier_keys & KMOD_CTRL and modifier_keys & KMOD_SHIFT):
                    if event.key == K_MINUS:
                        # coordinates.scale_x /= SCALE_RATIO
                        # coordinates.scale_y /= SCALE_RATIO
                        Coordinates.update_scale(1 / SCALE_RATIO)
                    elif event.key == K_EQUALS:
                        # coordinates.scale_x *= SCALE_RATIO
                        # coordinates.scale_y *= SCALE_RATIO
                        Coordinates.update_scale(SCALE_RATIO)
                    elif event.key == K_c:
                        File.screenshot()

                # cmd / ctrl
                elif (modifier_keys & KMOD_META) or (modifier_keys & KMOD_CTRL):
                    if event.key == K_q:
                        quit_all()
                    elif event.key == K_m:
                        pygame.display.iconify()
                    elif event.key == K_MINUS:
                        # coordinates.scale_x /= 2
                        # coordinates.scale_y /= 2
                        Coordinates.update_scale(fractions.Fraction(1, 2))
                    elif event.key == K_EQUALS:
                        # coordinates.scale_x *= 2
                        # coordinates.scale_y *= 2
                        Coordinates.update_scale(fractions.Fraction(2))
                    elif event.key == K_0:
                        # coordinates.scale_x, coordinates.scale_y = SCALE_DX, SCALE_DY
                        Coordinates.set_scale_x(fractions.Fraction(SCALE_DX))
                        Coordinates.set_scale_y(fractions.Fraction(SCALE_DY))
                        # coordinates.reset_origin(bool(tab.visible))
                        Coordinates.reset_origin(bool(tab.visible))
                    elif event.key == K_9:
                        # ave = (coordinates.scale_x + coordinates.scale_y) / 2
                        # coordinates.scale_x, coordinates.scale_y = ave, ave
                        average = (Coordinates.get_scale_x() + Coordinates.get_scale_y()) / 2
                        Coordinates.set_scale_x(average)
                        Coordinates.set_scale_y(average)
                    elif event.key == K_8:
                        # coordinates.reset_origin(bool(tab.visible))
                        Coordinates.reset_origin(bool(tab.visible))
                    elif event.key == K_BACKSPACE:
                        if tab.visible == FUNC_TAB:
                            Func.remove()
                        if tab.visible == VAR_TAB:
                            Variable.remove()
                    elif event.key == K_RETURN:
                        if tab.visible == FUNC_TAB:
                            Func("")
                        elif tab.visible == VAR_TAB:
                            Variable("")
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
                        # coordinates.axis_show = not coordinates.axis_show
                        Coordinates.toggle_axis_show()
                    elif event.key == K_g:
                        # coordinates.grid_show = not coordinates.grid_show
                        Coordinates.toggle_grid_show()
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
                    if modifier_keys & KMOD_SHIFT:
                        for shift in SHIFTS:
                            if event.key == shift[0]:
                                Func.insert(shift[1])
                    # alt key alternatives
                    elif modifier_keys & KMOD_ALT:
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
                        if not modifier_keys and len(k_name) == 1:
                            Func.insert(pygame.key.name(event.key))
                elif tab.visible == VAR_TAB:
                    # shift key alternatives
                    if modifier_keys & KMOD_SHIFT:
                        for shift in SHIFTS:
                            if event.key == shift[0]:
                                Variable.insert(shift[1])
                    # alt key alternatives
                    elif modifier_keys & KMOD_ALT:
                        for alt in ALTS:
                            if event.key == alt[0]:
                                Variable.insert(alt[1])
                    # single key shortcuts
                    elif event.key == K_BACKSPACE:
                        if var:
                            Variable.delete()
                    elif event.key == K_LEFT:
                        Variable.move_cursor(-1)
                    elif event.key == K_RIGHT:
                        Variable.move_cursor(1)
                    elif event.key == K_UP:
                        Variable.set_active("u")
                    elif event.key == K_DOWN:
                        Variable.set_active("d")
                    elif event.key == K_RETURN:
                        if not Variable.active:
                            message.put_delayed(display, "No expression available")
                        else:
                            assert var is not None
                            var.visible = not var.visible
                    elif event.key == K_SPACE:
                        Variable.insert(" ")
                    # basic input
                    else:
                        k_name = pygame.key.name(event.key)
                        if not modifier_keys and len(k_name) == 1:
                            Variable.insert(pygame.key.name(event.key))
            elif event.type == MOUSEBUTTONDOWN:
                # if mods & KMOD_SHIFT:
                if event.button == 4:
                    # coordinates.scale_x //= SCALE_RATIO
                    # coordinates.scale_y //= SCALE_RATIO
                    Coordinates.update_scale(1 / SCALE_RATIO)
                elif event.button == 5:
                    # coordinates.scale_x *= SCALE_RATIO
                    # coordinates.scale_y *= SCALE_RATIO
                    Coordinates.update_scale(SCALE_RATIO)
            elif event.type == VIDEORESIZE:
                tab.resize_win(event.w, event.h)

        # mouse control
        modifier_keys = pygame.key.get_mods()
        mouse_press = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if (modifier_keys & KMOD_META) or (modifier_keys & KMOD_CTRL):
            # coordinates.move_origin(*pygame.mouse.get_rel())
            Coordinates.move_origin(*pygame.mouse.get_rel())
        elif mouse_press[0]:
            # coordinates.move_origin(*pygame.mouse.get_rel())
            Coordinates.move_origin(*pygame.mouse.get_rel())
        elif mouse_press[2]:
            mouse_move = pygame.mouse.get_rel()
            minimal = min(display_width, display_height)
            # coordinates.scale_x *= 1 + mouse_move[0] / -minimal
            # coordinates.scale_y *= 1 + mouse_move[1] / minimal
            Coordinates.update_scale(1 + fractions.Fraction(mouse_move[0], -minimal))
            Coordinates.update_scale(1 + fractions.Fraction(mouse_move[1], minimal))
        else:
            if corner.collidepoint(mouse_pos):
                show_shortcuts()
            # reset mouse release position
            pygame.mouse.get_rel()
            focus_x = mouse_pos[0]

        # display
        display.fill(WHITE)

        Coordinates.grid()
        Coordinates.axis()

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


def show_shortcuts() -> None:
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
        line_num = (display_height - 10) // message.line_height - 1
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


def sgn0(num: numpy.float128) -> numpy.float128:
    """Returns -1 if num is less than 0 else 1."""

    if num < 0:
        return numpy.float128(-1)
    return numpy.float128(1)


def sgn(num: numpy.float128) -> numpy.float128:
    """
    Return the sign of x.

    >>> sgn(0)
    0
    >>> sgn(1)
    1
    >>> sgn(-1)
    -1
    """
    if num > 0:
        return numpy.float128(1)
    if num < 0:
        return numpy.float128(-1)
    return numpy.float128(0)


def seval(string: str, **kwargs: typing.Any) -> numpy.float128:
    """
    given a function string, return the value
    """

    # extend kwargs with math functions
    kwargs.update(math.__dict__)
    # kwargs: dict[str, typing.Any] = kwargs

    # extend kwargs with sgn and sgn0 functions
    kwargs.update({"sgn": sgn, "sgn0": sgn0})

    # extend with numpy functions
    # kwargs.update(numpy.__dict__)

    return numpy.float128(eval(string, kwargs))

def sig_figure(x: fractions.Fraction | numpy.float128, fig: int) -> numpy.float128:
    if isinstance(x, numpy.floating):
        return round(x, fig - int(math.floor(math.log10(abs(x)))) - 1)
    try:
        return round(numpy.float128(x), fig - int(math.floor(math.log10(abs(x)))) - 1)
    except OverflowError:
        return sgn(numpy.float128(x.denominator)) * float("inf")

def lable_number(x: numpy.float128) -> str:
    """
    returns a string of a number in scientific notation with a maximum length of 10
    """
    if len(str(x)) <= 10:
        return str(x)
    else:
        return "{:.1e}".format(x)

# @functools.cache
def evaluate2(x: float, y: float, s: str, origin_x: int, origin_y: int, scale_x: fractions.Fraction, scale_y: fractions.Fraction) -> numpy.float128:
    x = (x - origin_x) / scale_x
    y = (origin_y - y) / scale_y
    return seval(s, x=x, y=y)


def y_equals(string: str, origin: DisplayPoint, scale_x: fractions.Fraction, scale_y: fractions.Fraction) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    """
    given a function string, return a tuple of line coordinate pairs
    """

    # create old tuple of coordinate pairs
    old_coordinates = None

    # create output list
    output: list[tuple[tuple[int, int], tuple[int, int]]] = []

    # loop through x values from x_min to x_max with DISPLAY_WIDTH increments
    for x_disp in range(DISPLAY_WIDTH):
        try:

            # calculate x value
            x = (x_disp - origin.x) / scale_x

            # calculate y value
            y = seval(string, x=x)

            # convert y value to display coordinates
            y_raw = origin.y - y * scale_y.numerator / scale_y.denominator

            # if this is the first coordinate pair
            if old_coordinates is None:

                # set old coordinate pair
                old_coordinates = (int(x_disp), int(y_raw))

            # if this is not the first coordinate pair
            else:

                # create new coordinate pair
                new_coord = (int(x_disp), int(y_raw))

                # add old and new coordinate pair to output list
                output.append((old_coordinates, new_coord))

                # set old coordinate pair
                old_coordinates = new_coord

        # if there is an error
        except Exception:

            # set old coordinate pair to None
            old_coordinates = None

    # return output tuple
    return tuple(output)


def xyre(string: str, origin: DisplayPoint, scale_x: fractions.Fraction, scale_y: fractions.Fraction) -> typing.Optional[tuple[tuple[tuple[int, int], tuple[int, int]], ...]]:
    """
    Given a string, return a tuple of line coordinate pairs
    """

    if list(string).count("=") != 1:
        return None

    # draw graph of the relation
    # initiate value
    ori_x, ori_y = origin.x, origin.y
    gap_x, gap_y = SCALE_DX / scale_x, SCALE_DY / scale_y
    # print(coor.origin)
    # gap_x = sig_figure(gap_x, 2)
    # gap_y = sig_figure(gap_y, 2)
    gap_px = int(gap_x * scale_x) // 5
    gap_py = int(gap_y * scale_y) // 5
    # left_lim = Tab.width if tab.visible else 0
    left_lim = 0

    # compute matrix
    try:
        # sanity check
        r = tuple(string.split("="))
        evaluate2(0, 0, r[0], ori_x, ori_y, scale_x, scale_y)
        evaluate2(0, 0, r[1], ori_x, ori_y, scale_x, scale_y)

        # compute matrix
        matrix: list[list[numpy.float128]] = []
        for x in range((ori_x - left_lim) % gap_px + left_lim, DISPLAY_WIDTH, gap_px):
            matrix.append([])
            for y in range(ori_y % gap_py, DISPLAY_HEIGHT, gap_py):
                matrix[-1].append(evaluate2(x, y, r[0], ori_x, ori_y, scale_x, scale_y) - evaluate2(x, y, r[1], ori_x, ori_y, scale_x, scale_y))
        # compute line segments
        line_segments: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for mx, x in enumerate(range((ori_x - left_lim) % gap_px + left_lim, DISPLAY_WIDTH - gap_px, gap_px)):
            for my, y in enumerate(range(ori_y % gap_py, DISPLAY_HEIGHT - gap_py, gap_py)):
                line_segment = []
                if sgn0(matrix[mx][my]) != sgn0(matrix[mx + 1][my]):
                    line_segment.append((int(x + gap_px * abs(matrix[mx][my]) / (abs(matrix[mx][my]) + abs(matrix[mx + 1][my]))), y))
                if sgn0(matrix[mx][my]) != sgn0(matrix[mx][my + 1]):
                    line_segment.append((x, int(y + gap_py * abs(matrix[mx][my]) / (abs(matrix[mx][my]) + abs(matrix[mx][my + 1])))))
                if sgn0(matrix[mx + 1][my]) != sgn0(matrix[mx + 1][my + 1]):
                    line_segment.append((x + gap_px, int(y + gap_py * abs(matrix[mx + 1][my]) / (abs(matrix[mx + 1][my]) + abs(matrix[mx + 1][my + 1])))))
                if sgn0(matrix[mx][my + 1]) != sgn0(matrix[mx + 1][my + 1]):
                    line_segment.append((int(x + gap_px * abs(matrix[mx][my + 1]) / (abs(matrix[mx][my + 1]) + abs(matrix[mx + 1][my + 1]))), y + gap_py))

                # if there are 2 points to draw
                if len(line_segment) == 2:
                    line_segments.append(((int(line_segment[0][0]), int(line_segment[0][1])), (int(line_segment[1][0]), int(line_segment[1][1]))))
                # TODO: add support for 4 points

        return tuple(line_segments)
    except Exception:
        return None


def quit_all(save: bool = True) -> None:
    if save:
        data.put()
    logger.debug("Quit all called by user")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc().replace(os.getcwd(), ""))
        print("Consider deleting assets/data.p")
