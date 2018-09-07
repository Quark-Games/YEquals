import pygame
from pygame.locals import *
from math import *
import re

pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()
fps = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

MODIFIERS = ("alt", "ctrl", "escape", "meta", "shift", "tab", "windows")

font = pygame.font.Font(None, 20)


def main():
    func = ""
    scale = 10
    holding = set()

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_all()
            if event.type == KEYDOWN:
                key_name = pygame.key.name(event.key)
                for modifier in MODIFIERS:
                    if modifier in key_name:
                        holding.add(modifier)
                        break
                else:
                    if "meta" in holding:
                        if event.key == K_q:
                            quit_all()
                    elif "shift" in holding:
                        if event.key == K_8:
                            func += '*'
                    elif event.key == K_BACKSPACE:
                        if func:
                            func = func[:-1]
                    elif event.key == K_SPACE:
                        func += ' '
                    else:
                        func += key_name
            if event.type == KEYUP:
                key_name = pygame.key.name(event.key)
                for modifier in MODIFIERS:
                    if modifier in key_name:
                        holding.remove(modifier)
                        break
                else:
                    pass

        display.fill(WHITE)

        bitmap = font.render(func, True, BLACK)
        display.blit(bitmap, (10, 10))

        pygame.draw.line(display,
                         RED,
                         (0, display_height / 2),
                         (display_width, display_height / 2))
        pygame.draw.line(display,
                         RED,
                         (display_width / 2, 0),
                         (display_width / 2, display_height))

        try:
            for pixel_x in range(0, display_width):
                x = (pixel_x - display_width / 2) / scale
                exec(func)
                pixel_y = int(display_height / 2 - y * scale)
                pygame.draw.rect(display,
                                 BLACK,
                                 (pixel_x, pixel_y, 1, 1))
        except:
            bitmap = font.render("Function not drawable!", True, BLACK)
            display.blit(bitmap, (10, 30))

        pygame.display.flip()

        clock.tick(fps)


def quit_all():
    pygame.quit()
    quit()


main()
