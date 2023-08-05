#!/usr/bin/env python3

'''@TODO@'''

import logging
import pygame as pg

from . import StaticDict


class Style(StaticDict):
    '''@TODO@'''

    DEFAULT = {
        'background': None,
        'bold': False,
        'border': 'color',
        'border-width': 0,
        'color': (255, 255, 255),
        'color-background': (0, 0, 0),
        'color-border': (100, 100, 100),
        'color-frame-bar': (150, 150, 150, 150),
        'color-frame-bar-container': (100, 100, 100, 150),
        'corner': None,
        'cursor': None,
        'expand': False,
        'font': pg.font.get_default_font(),
        'font-size': 16,
        'frame-bar-width': 8,
        'frame-bar-corner': 4,
        'halign': 'left',
        'hspacing': 10,
        'image-background': None,
        'image-border': None,
        'image-checkbox': None,
        'image-frame-vscroll-bar': None,
        'image-frame-vscroll-container': None,
        'image-hrule': None,
        'image-select': None,
        'image-vrule': None,
        'image-window-cross': None,
        'italic': False,
        'orientation': 'vertical',
        'padding': 0,
        'size': None,
        'sound': None,
        'underline': False,
        'valign': 'top',
        'vspacing': 10,
        'width': None
    }

    INHERITED = {
        'color',
        'font',
        'font-size',
        'hspacing',
        'vspacing'
    }

    def __init__(self, d=None):
        '''@TODO@'''
        StaticDict.__init__(self, d)

    def __setitem__(self, key, value):
        try:
            StaticDict.__setitem__(self, key, value)
        except KeyError:
            logging.warning('undefined style: %s', key)

    def __getitem__(self, key):
        try:
            return StaticDict.__getitem__(self, key)
        except KeyError:
            logging.warning('undefined style: %s', key)
            return None
