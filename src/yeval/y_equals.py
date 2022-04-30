"""
y_equals.py

includes y_equals
"""

import math
from ..common import DISPLAY_WIDTH


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
