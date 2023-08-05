#!/usr/bin/env python3

'''definition of class Box'''

from . import Coord, Node, Label


class Box(Node):
    '''Box nodes are containers for other nodes'''

    def __init__(self, *nodes, **kwargs):
        '''create a Box node initialised with nodes'''
        Node.__init__(self, **kwargs)
        self.__children = list()
        for node in nodes:
            self.pack(node)

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        yield from self.children

    def __str__(self):
        return 'box(size={}, pos={}, {})'.format(
            self.size, self.pos, ",".join(map(str, self.__children)))

    def __getitem__(self, i):
        return self.__children[i]

    @property
    def children(self):
        '''@TODO@'''
        return self.__children

    def is_empty(self):
        '''check if box is empty'''
        return self.__children == []

    def empty(self):
        '''empty the box of all its children'''
        for child in self.__children:
            child.unref()
        self.__children = list()
        self.update_manager()
        self.reset_size()

    def pack(self, node):
        '''append node to the box children'''
        self.insert(len(self.__children), node)

    def remove(self, i):
        '''remove the ith child of the box'''
        self.replace(i, None)
        self.reset_size()
        self.update_manager()

    def remove_node(self, node):
        '''remove Node node from the box.  raise ValueError if node is not in
        the box'''
        idx = self.children.index(node)
        self.remove(idx)

    def replace(self, i, node):
        '''replace the ith child of the box'''
        lg = len(self.children)
        if i >= lg:
            raise ValueError(
                'tried to replace {}-th child of a {}-node box'.format(i, lg))
        old = self.__children[i]
        old.unref()
        self.__children.remove(old)
        if node is not None:
            self.insert(i, Label.node_of(node))
        self.reset_size()

    def insert(self, i, node):
        '''insert in the box at ith position'''
        node = Label.node_of(node)
        self.__children.insert(i, node)
        self.add_child(node)
        self.update_manager()
        self.reset_size()

    def __expanded_child_size(self, expanded, size):
        hspacing = self.get_style('hspacing')
        vspacing = self.get_style('vspacing')
        orientation = self.get_style('orientation')
        if orientation == 'vertical':
            hsum = (len(self.children) - 1) * vspacing
            for node in self.children:
                if node != expanded:
                    hsum += node.size[1]
            result = size[0], size[1] - hsum
        else:
            wsum = (len(self.children) - 1) * hspacing
            for node in self.children:
                if node != expanded:
                    wsum += node.size[0]
            result = size[0] - wsum, size[1]
        return result

    def _precompute_inner_size(self):
        sw, sh = (None, None) if self.size is None else self.size
        if sw is not None:
            sw -= self._inner_diff()[0]
        if sh is not None:
            sh -= self._inner_diff()[1]
        return sw, sh

    def _compute_inner_size(self):
        def compute_dim(sizes, sumed, maxed, spacing):
            m = max(sizes, key=lambda wh: wh[maxed], default=(0, 0))[maxed]
            s = sum(map(lambda wh: wh[sumed], sizes))
            if len(sizes) > 1:
                s += (len(sizes) - 1) * self.get_style(spacing)
            return m, s

        def compute_sizes():
            sizes = list(map(
                lambda child: child.compute_size(), self.children))
            if orientation == 'vertical':
                w, h = compute_dim(sizes, 1, 0, 'vspacing')
            else:
                h, w = compute_dim(sizes, 0, 1, 'hspacing')
            result = Coord.combine((sw, sh), (w, h))
            return sizes, result

        orientation = self.get_style('orientation')
        sw, sh = self._precompute_inner_size()
        sizes, result = compute_sizes()

        #  set the container sizes of all children
        expanded = next((child for child in self.__children
                         if child.get_style('expand')), None)
        for child, (cw, ch) in zip(self.__children, sizes):
            if child != expanded:
                csize = (result[0], ch) if orientation == 'vertical' \
                    else (cw, result[1])
            else:
                csize = self.__expanded_child_size(expanded, result)
            child.set_container_size(csize)

        #  we have to recompute self's inner size since the update of
        #  a child container size may have changed its size if it has
        #  a relative size and hence self's inner size
        _, result = compute_sizes()
        return result

    def _position(self, pos):
        orientation = self.get_style('orientation')
        if orientation == 'vertical':
            spacing = self.get_style('vspacing')
            for child in self.children:
                child.position(pos)
                pos = Coord.sum(pos, (0, spacing + child.size[1]))
        else:
            spacing = self.get_style('hspacing')
            for child in self.children:
                child.position(pos)
                pos = Coord.sum(pos, (spacing + child.size[0], 0))

    def _iter_tree(self):
        for child in self.children:
            yield from child.iter_tree()
