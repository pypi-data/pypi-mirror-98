#!/usr/bin/env python3

'''definition of class Draw'''

import pygame as pg

from . import Coord


class Draw:
    '''defines several drawing functions'''

    BLACK = (0, 0, 0, 0)

    @classmethod
    def rectangle(cls, surface, color, rect, width=0):
        '''draw rectangle rect on the surface with the given color and width'''
        x, y, w, h = rect
        if w == 0 or h == 0:
            return
        if width == 0 or width is None:
            pg.draw.rect(surface, color, rect, width)
        else:
            if width > 2 * w or width > 2 * h:
                msg = 'incorrect width for a ({}, {}) rectangle: {}'.format(
                    w, h, width)
                raise ValueError(msg)
            pg.draw.rect(surface, color, (x, y, w, width))
            pg.draw.rect(surface, color, (x, y, width, h))
            pg.draw.rect(surface, color, (x + w - width, y, width, h))
            pg.draw.rect(surface, color, (x, y + h - width, w, width))

    @classmethod
    def rectangle_rounded(cls, surface, color,  # pylint: disable=R0913
                          rect, radius, width=0):
        '''draw a rounded rectangle with corners having the given radius'''

        def draw_sub_rects():
            #  draw sub rectangles
            if width == 0 or width is None:
                rects = [
                    (x + radius, y, w - 2 * radius + 1, radius),
                    (x, y + radius, w, h - 2 * radius),
                    (x + radius, y + h - radius, w - 2 * radius + 1, radius)
                ]
            else:
                rects = [
                    (x + radius, y, w - 2 * radius + 1, width),
                    (x + radius, y + h - width, w - 2 * radius + 1, width),
                    (x, y + radius, width, h - 2 * radius),
                    (x + w - width, y + radius, width, h - 2 * radius)
                ]
            for r in rects:
                Draw.rectangle(surface, color, r)

        def draw_angles():
            #  draw rounded angles
            circle = pg.Surface((radius * 2, radius * 2)).convert_alpha()
            circle.fill(Draw.BLACK)
            pg.draw.circle(
                circle, color, (radius, radius), radius)
            if not (width == 0 or width is None):
                pg.draw.circle(
                    circle, Draw.BLACK, (radius, radius), radius - width)
            cs = (radius, radius)
            for pos, area in [
                    ((x, y), Coord.rect((0, 0), cs)),
                    ((x + w - radius, y), Coord.rect((radius, 0), cs)),
                    ((x, y + h - radius), Coord.rect((0, radius), cs)),
                    ((x + w - radius, y + h - radius), Coord.rect(cs, cs))
            ]:
                surface.blit(circle, pos, area=area)

        x, y, w, h = rect
        radius = min(radius, int(w / 2), int(h / 2))

        #  no radius => simple rectangle drawing
        if radius == 0 or radius is None:
            Draw.rectangle(surface, color, rect, width)
            return

        draw_sub_rects()
        draw_angles()

    @classmethod
    def circle(cls, surface, color,  # pylint: disable=R0913
               origin, radius, width=0):
        '''draw a circle'''
        if width == 0:
            pg.draw.circle(surface, color, origin, radius)
        else:
            circle = pg.Surface((radius * 2, radius * 2)).convert_alpha()
            circle.fill(Draw.BLACK)
            pg.draw.circle(
                circle, color, (radius, radius), radius)
            pg.draw.circle(
                circle, Draw.BLACK, (radius, radius), radius - width)
            surface.blit(circle, (origin[0] - radius, origin[1] - radius))
