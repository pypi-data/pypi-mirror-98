#!/usr/bin/env python3

'''@TODO@'''

from . import Draw, Node, Label


class Gauge(Node):
    '''@TODO@'''

    def __init__(self, min_val, max_val, val, **kwargs):
        '''@TODO@'''
        Node.__init__(self, **kwargs)
        self.__min = min_val
        self.__max = max_val
        self.__val = val
        self.__label = None
        self.__label_draw = kwargs.get('label_draw', True)
        self.__label_cls = kwargs.get('label_cls', None)
        self.__label_format = kwargs.get('label_format', None)
        self.__set_label()

    @property
    def value(self):
        '''@TODO@'''
        return self.__val

    def set_value(self, val):
        '''@TODO@'''
        self.__val = val
        self.__set_label()
        self.update_manager()

    def set_label_format(self, label_format):
        '''@TODO@'''
        self.__label_format = label_format
        self.__set_label()

    def __set_label(self):
        if not self.__label_draw:
            return
        if self.__label_format is None:
            txt = str(self.__val) + ' / ' + str(self.__max)
        else:
            txt = self.__label_format(self.__min, self.__val, self.__max)
        self.__label = Label(txt, style=self.__label_cls)
        self.__label.compute_size()

    def _compute_inner_size(self):
        self.__label.compute_size()
        return (200, 40)

    def __draw_bar(self, surface, pos):
        w, h = self.inner_size
        color = self.get_style('color')
        x, y = pos
        pts = int(self.__val * w / (self.__max - self.__min))
        rect = (x, y, pts, h)
        Draw.rectangle(surface, color, rect)

    def _position(self, pos):
        w, h = self.size
        lw, lh = self.__label.size
        x, y = pos
        x = x + int((w - lw) / 2)
        y = y + int((h - lh) / 2)
        self.__label.position((x, y))

    def _draw(self, surface):
        self.__draw_bar(surface, self.inner_pos)

    def _iter_tree(self):
        yield self.__label
