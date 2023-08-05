#!/usr/bin/env python3

'''definition of class Grid'''

from pygwin import Box, Coord


class Grid(Box):
    '''@TODO@'''

    def __init__(self, *nodes, **kwargs):
        '''@TODO@'''
        Box.__init__(self, *nodes, **kwargs)
        if self.get_style('orientation') == 'horizontal':
            raise ValueError('unimplemented feature: horizontal grids')

    def _compute_inner_size(self):
        def get_result_height():
            if result_height is None:
                return rh
            return result_height + vspacing + rh

        w, h = self._precompute_inner_size()
        sizes = list(map(
            lambda child: child.compute_size(), self.children))
        if w is not None and h is not None:
            return w, h

        orientation = self.get_style('orientation')
        hspacing = self.get_style('hspacing')
        vspacing = self.get_style('vspacing')

        #  check that the size of component grids could have been
        #  computed
        for size in sizes:
            try:
                cw, ch = size
                ex = cw is None or ch is None
            except TypeError:
                ex = True
            if ex:
                raise ValueError('cannot determine size of a grid component')

        rw = None  # row width
        rh = None  # row height

        result_height = None
        for cw, ch in sizes:
            if orientation == 'vertical':
                if w is not None and rw is not None and rw + cw > w:
                    result_height = get_result_height()
                    rw = None
                if rw is None:
                    rw = cw
                    rh = ch
                else:
                    rw += hspacing + cw
                    rh = max(rh, ch)
        result_height = 0 if rw is None else get_result_height()

        if orientation == 'vertical':
            w, h = Coord.combine((w, h), (rw, result_height))
        return w, h

    def _position(self, pos):
        width, height = self.inner_size
        hspacing = self.get_style('hspacing')
        vspacing = self.get_style('vspacing')
        orientation = self.get_style('orientation')
        w = 0
        h = 0
        rw = 0
        rh = 0
        for child in self.children:
            cw, ch = child.size
            if orientation == 'vertical':
                if w + cw > width:
                    h += vspacing + ch
                    w = 0
                    rh = 0
                rh = max(rh, ch)
            else:
                if h + ch > height:
                    w += hspacing + cw
                    h = 0
                    rw = 0
                rw = max(rw, cw)
            child.position(Coord.sum(pos, (w, h)))
            if orientation == 'vertical':
                w += vspacing + cw
            else:
                h += hspacing + ch
