#!/usr/bin/env python3

'''definition of class Label'''

import functools

from . import Node, Util


class Label(Node):
    '''Label nodes are used to draw texts.'''

    def __init__(self, text, **kwargs):
        '''create a label with the given text.

        if not None, kwarg label_for must be a Node object.  if the
        label is clicked, then the this node is activated.'''
        def click():
            if self.is_clicked():
                label_for.activate()
                return True
            return False
        Node.__init__(self, **kwargs)
        self.__text = None
        label_for = kwargs.get('label_for')
        if label_for is not None:
            Util.check_type(label_for, Node, name='label_for')
            self.set_link(click)
        self.set_text(text)

    def __str__(self):
        return 'label(size={}, pos={}, {})'.format(
            self.size, self.pos, self.text)

    @property
    def text(self):
        '''text of the label'''
        return self.__text

    def set_text(self, text):
        '''change the text of the label'''
        self.__text = text
        self.update_manager()
        self.reset_size()

    @classmethod
    def node_of(cls, value, **kwargs):
        '''return value if it is a Node object or a Label containing
        str(value) otherwise'''
        if isinstance(value, Node):
            result = value
        else:
            result = Label(str(value), **kwargs)
        return result

    @classmethod
    @functools.lru_cache(maxsize=10000)
    def __render_cache(cls, text, font, color, **kwargs):
        font.set_bold(kwargs.get('bold', False))
        font.set_underline(kwargs.get('underline', False))
        font.set_italic(kwargs.get('italic', False))
        result = next(Util.split_lines(text, font, color))
        font.set_bold(False)
        font.set_italic(False)
        font.set_underline(False)
        return result

    @classmethod
    def __render(cls, text, font, color, **kwargs):
        return cls.__render_cache(text, font, tuple(color), **kwargs)

    def __redraw(self):
        return Label.__render(
            self.__text, self.get_font(), self.get_style('color'),
            underline=self.get_style('underline'),
            italic=self.get_style('italic'),
            bold=self.get_style('bold'))

    def _compute_inner_size(self):
        return self.__redraw().get_size()

    def _draw(self, surface):
        surface.blit(self.__redraw(), self.inner_pos)
