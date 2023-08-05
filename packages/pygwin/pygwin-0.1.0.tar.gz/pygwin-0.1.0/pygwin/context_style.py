#!/usr/bin/env python3

'''definition of class ContextStyle'''

from . import Style, Context


class ContextStyle(dict):
    '''@TODO@'''

    def get_attr(self, ctx, attr):
        '''@TODO@'''
        if ctx in self and attr in self[ctx]:
            result = self[ctx][attr]
        else:
            result = None
        return result

    def set_attr(self, attr, value, ctx=Context.BASE, update=True):
        '''@TODO@'''
        if ctx not in self:
            self[ctx] = Style()
        result = update or attr not in self[ctx]
        if result:
            self[ctx][attr] = value
        return result

    def update(self, ctx, style):
        '''@TODO@'''
        if ctx not in self:
            self[ctx] = {**style}
        else:
            self[ctx] = {**self[ctx], **style}
