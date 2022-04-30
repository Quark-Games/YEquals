"""
yeval.py

includes various methods for calculating what to draw.
"""

import functools
from inspect import trace
import traceback
from math import *
from .common import DISPLAY_WIDTH, DISPLAY_HEIGHT, SCALE_DX, SCALE_DY
from .extlib import sgn0


def sig_figure(x, fig):
    return round(x, fig - int(floor(log10(abs(x)))) - 1)


@functools.cache
def evaluate2(x, y, s, ori_x, ori_y, scalex, scaley):
    if e:
        x = (x - ori_x) / scalex
        y = (ori_y - y) / scaley
    return eval(s)


def y_equals(s:str, coor) -> tuple:
    """
    given a function string, return a tuple of line coordinate pairs
    """

    # create old tuple of coordinate pairs
    old_coord = None

    # create output list
    output = []

    # loop through x values from x_min to x_max with DISPLAY_WIDTH increments
    for x_disp in range(DISPLAY_WIDTH):
        try:

            # calculate x value
            x = (x_disp - coor.origin[0]) / coor.scalex

            # calculate y value
            y = eval(s)

            # convert y value to display coordinates
            y_raw = coor.origin[1] - y * coor.scaley

            # if this is the first coordinate pair
            if old_coord is None:

                # set old coordinate pair
                old_coord = (x_disp, y_raw)

            # if this is not the first coordinate pair
            else:

                # create new coordinate pair
                new_coord = (x_disp, y_raw)

                # add old and new coordinate pair to output list
                output.append((old_coord, new_coord))

                # set old coordinate pair
                old_coord = new_coord

        # if there is an error
        except Exception:

            # set old coordinate pair to None
            old_coord = None

    # return output tuple
    return tuple(output)


def xyre(s:str, coor) -> tuple:

    if list(s).count("=") != 1:
        return None

    # draw graph of the relation
    # initiate value
    ori_x, ori_y = map(int, coor.origin)
    gap_x, gap_y = SCALE_DX / coor.scalex, SCALE_DY / coor.scaley
    # print(coor.origin)
    gap_x = sig_figure(gap_x, 2)
    gap_y = sig_figure(gap_y, 2)
    gap_px = int(gap_x * coor.scalex) // 5
    gap_py = int(gap_y * coor.scaley) // 5
    # left_lim = Tab.width if tab.visible else 0
    left_lim = 0

    # compute matrix
    try:
        # sanity check
        r = tuple(s.split("="))
        evaluate2(0, 0, r[0], ori_x, ori_y, coor.scalex, coor.scaley)
        evaluate2(0, 0, r[1], ori_x, ori_y, coor.scalex, coor.scaley)

        # compute matrix
        matrix = []
        for x in range((ori_x - left_lim) % gap_px + left_lim, DISPLAY_WIDTH, gap_px):
            matrix.append([])
            for y in range(ori_y % gap_py, DISPLAY_HEIGHT, gap_py):
                matrix[-1].append(
                    evaluate2(x, y, r[0], ori_x, ori_y, coor.scalex, coor.scaley) -
                    evaluate2(x, y, r[1], ori_x, ori_y, coor.scalex, coor.scaley)
                )
        # compute
        points = []
        for mx, x in enumerate(range((ori_x - left_lim) % gap_px + left_lim, DISPLAY_WIDTH - gap_px, gap_px)):
            for my, y in enumerate(range(ori_y % gap_py, DISPLAY_HEIGHT - gap_py, gap_py)):
                temp = []
                if sgn0(matrix[mx][my]) != sgn0(matrix[mx+1][my]):
                    temp.append((
                        x + gap_px * abs(matrix[mx][my]) / (abs(matrix[mx][my]) + abs(matrix[mx+1][my])),
                        y,
                    ))
                if sgn0(matrix[mx][my]) != sgn0(matrix[mx][my+1]):
                    temp.append((
                        x,
                        y + gap_py * abs(matrix[mx][my]) / (abs(matrix[mx][my]) + abs(matrix[mx][my+1])),
                    ))
                if sgn0(matrix[mx+1][my]) != sgn0(matrix[mx+1][my+1]):
                    temp.append((
                        x + gap_px,
                        y + gap_py * abs(matrix[mx+1][my]) / (abs(matrix[mx+1][my]) + abs(matrix[mx+1][my+1])),
                    ))
                if sgn0(matrix[mx][my+1]) != sgn0(matrix[mx+1][my+1]):
                    temp.append((
                        x + gap_px * abs(matrix[mx][my+1]) / (abs(matrix[mx][my+1]) + abs(matrix[mx+1][my+1])),
                        y + gap_py,
                    ))
                if len(temp) == 2:
                    points.append(((int(temp[0][0]), int(temp[0][1])), (int(temp[1][0]), int(temp[1][1]))))

        return points
    except Exception as e:
        # print(traceback.format_exc())
        pass
