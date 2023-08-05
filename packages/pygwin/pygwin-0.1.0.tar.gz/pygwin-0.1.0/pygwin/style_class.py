#!/usr/bin/env python3

'''@TODO@'''

import re
import inspect
import logging
import json

from . import Util, Context, ContextStyle


class StyleClass(dict):
    '''@TODO@'''

    CLASSES = {
    }

    __RE_CLS_NAME = re.compile(r'(\w+)(:\w+(,\w+)*)?')

    def __init__(self, name, register=True):
        self.__name = name
        dict.__init__(self)
        if register:
            StyleClass.CLASSES[name] = self

    @property
    def name(self):
        '''name of the class'''
        return self.__name

    def set_style(self, style, node_class=None):
        '''load all style classes from file json_file.  it is required that
        pygwin has been fully loaded as we have to import Node here'''
        if node_class is None:
            from pygwin import Node  # pylint: disable=C0415
            node_class = Node
        if not isinstance(style, ContextStyle):
            style = ContextStyle(style)
        self[node_class] = style

    def update(self, style, node_class=None, ctx=Context.BASE):
        '''update the style.  it is required that
        pygwin has been fully loaded as we have to import Node here'''
        if node_class is None:
            from pygwin import Node  # pylint: disable=C0415
            node_class = Node
        if node_class not in self:
            self[node_class] = ContextStyle()
        self[node_class].update(ctx, style)

    def set_attr(
            self, attr, value, node_class=None, ctx=Context.BASE, update=True):
        '''assign value to attribute attr.  it is required that
        pygwin has been fully loaded as we have to import Node here'''
        if node_class is None:
            from pygwin import Node  # pylint: disable=C0415
            node_class = Node
        if node_class not in self:
            self[node_class] = ContextStyle()
        return self[node_class].set_attr(attr, value, ctx=ctx, update=update)

    def get_attrs(self, node):
        '''yield triples (context, attr, value) for node'''
        for node_cls in list(inspect.getmro(type(node))[:-1]):
            if node_cls in self:
                for ctx, style in self[node_cls].items():
                    for attr, value in style.items():
                        yield ctx, attr, value

    @classmethod
    def exists(cls, name):
        '''check there is a registered class named name'''
        return name in StyleClass.CLASSES

    @classmethod
    def rem(cls, name):
        '''delete registered style class name'''
        if name not in StyleClass.CLASSES:
            logging.warning('style class does not exist: %s', name)
        else:
            del StyleClass.CLASSES[name]

    @classmethod
    def get(cls, name):
        '''get the registered class named name'''
        if name not in StyleClass.CLASSES:
            logging.warning('style class does not exist: %s', name)
            return None
        return StyleClass.CLASSES[name]

    @classmethod
    def load(cls, json_file):
        '''load all style classes from file json_file.  it is required that
        pygwin has been fully loaded as we have to import Node here'''
        from pygwin import Node  # pylint: disable=C0415

        def find_class(name):
            def find_class_rec(name, node_cls):
                if node_cls.__name__ == name:
                    result = node_cls
                else:
                    result = None
                    for sub_cls in node_cls.__subclasses__():
                        result = find_class_rec(name, sub_cls)
                        if result is not None:
                            break
                return result
            result = find_class_rec(name, Node)
            if result is None:
                raise ValueError()
            return result
        with open(json_file, 'r') as fd:
            try:
                data = json.loads(fd.read())
            except json.decoder.JSONDecodeError:
                logging.warning('error when loading json file %s', json_file)
                return
        loaded = set()
        for name, style in data.items():
            match = StyleClass.__RE_CLS_NAME.fullmatch(name)
            if match is None:
                logging.warning('invalid style class name: %s', name)
                continue
            grps = match.groups()
            name = grps[0]
            if grps[1] is None:
                classes = [Node]
            else:
                try:
                    names = match.groups()[1][1:]
                    classes = list(map(find_class, names.split(',')))
                except ValueError:
                    logging.warning('invalid node class: %s', names)
                    continue
            try:
                name = find_class(name)
            except ValueError:
                pass
            if not StyleClass.exists(name):
                c = StyleClass(name)
            elif name not in loaded:
                StyleClass.rem(name)
                c = StyleClass(name)
            c = StyleClass.get(name)
            for node_class in classes:
                Util.rec_merge_dicts(
                    {node_class: ContextStyle(style)},
                    target=c)
            loaded.add(name)
