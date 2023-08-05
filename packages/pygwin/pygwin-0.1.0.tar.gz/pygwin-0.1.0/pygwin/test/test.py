#!/usr/bin/env python3

'''test module for pygwin.  provides function go that launches a
simple test application'''

import os
import sys
import logging
import string
import random
import pkg_resources
import pygame as pg

from pygwin import VERSION, WindowSystem, Panel, Label, Window, Animation
from pygwin import Checkbox, RadioboxGroup, InputText, Table, Rule, Style
from pygwin import Image, Media, Cursor, Menu, Gauge, TextBoard, Empty
from pygwin import ItemSelect, IntSelect, Box, Coord, Frame, Context
from pygwin import Radiobox, StyleClass, DefaultStyle, Button, Grid


def get_media_file(f):
    '''get the absolute path of a file in the media directory of pygwin.test'''
    return os.path.join(MEDIA_DIR, f)


FPS = 50
MEDIA_DIR = pkg_resources.resource_filename('pygwin.test', 'media')
MONSTERS = {
    'orc': (get_media_file('orc.png'), '10', '20', '0', '10'),
    'elf': (get_media_file('elf.png'), '5', '15', '30', '50'),
    'dragon': (get_media_file('dragon.png'), '70', '100', '50', '200')
}
CTX_MENU_CANDIDATE_POS = [
    (Coord.RELATIVE, ((Coord.RIGHT, 0), (Coord.BOTTOM, 0))),
    (Coord.RELATIVE, ((Coord.RIGHT, 0), (Coord.TOP, 0))),
    (Coord.RELATIVE, ((Coord.LEFT, 0), (Coord.BOTTOM, 0))),
    (Coord.RELATIVE, ((Coord.LEFT, 0), (Coord.TOP, 0)))
]
TOOLTIP_STYLE = {
    'border': 'color',
    'border-width': 4,
    'padding': 10,
    'orientation': 'vertical',
    'background': 'color',
    'color-background': (20, 20, 100)
}


def monster_table(m):
    '''create and return a table containing monster attributes'''
    result = Table()
    data = MONSTERS[m]
    result.new_row({0: Label('name'),
                    1: Label(m)})
    result.new_row({0: Label('health'),
                    1: Gauge(0, int(data[2]), int(data[1]))})
    result.new_row({0: Label('magic'),
                    1: Gauge(0, int(data[4]), int(data[3]))})
    return result


def basic_window(win_sys, title):
    '''test window'''
    box = Box('The window can be moved by',
              'drag and dropping its title.',
              'Escape closes the window.')
    return Window(win_sys, box, title=title)


def tables_window(win_sys, title):
    '''tables window'''
    center = {'halign': 'center'}
    right = {'halign': 'right'}
    tbl = Table()
    tbl.new_row({0: Label('monster', style=center),
                 2: Label('characteristics', style=center)},
                colspan={0: 2, 2: 4})
    tbl.new_row({2: Label('health', style=center),
                 4: Label('magic', style=center)},
                colspan={2: 2, 4: 2})
    tbl.new_row({2: Label('min'),
                 3: Label('max'),
                 4: Label('min'),
                 5: Label('max')})
    for m in MONSTERS:
        cells = {j + 2: Label(data, style=right)
                 for j, data in enumerate(MONSTERS[m][1:])}
        cells[0] = Label(m)
        cells[1] = Image(Media.get_image(MONSTERS[m][0]))
        tbl.new_row(cells)
    return Window(win_sys, tbl, title=title)


def controls_window(win_sys, title):
    '''controls window'''
    def check():
        tbl = Table()
        for i, ip in enumerate(ips):
            tbl.new_row({0: Label('text written {}'.format(i)),
                         1: Label(ip.value)})
        tbl.new_row({0: Label('checkbox checked'),
                     1: Label('yes' if cb.value else 'no')})
        tbl.new_row({0: Label('you are feeling'),
                     1: Label(str(grp.value))})
        tbl.new_row({0: Label('fruit selected'),
                     1: Label(str(fruits.value))})
        tbl.new_row({0: Label('your age'),
                     1: Label(str(ages.value))})
        Window(win_sys, tbl, title='results').open()
        return True

    def disable():
        if btn_disable.node.text == 'disable controls':
            btn_disable.node.set_text('enable controls')
            tbl.disable()
        else:
            btn_disable.node.set_text('disable controls')
            tbl.enable()
        btn_disable.enable()
        return True
    tbl = Table()
    ips = [
        InputText(place_holder='An input text'),
        InputText(place_holder='A larger input text',
                  style={'size': (300, None)}),
        InputText(place_holder='An input text occupying all space',
                  style={'size': ('100%', None)}),
        InputText(place_holder='An input text with a prompt',
                  prompt='prompt> ',
                  style={'size': ('100%', None)}),
        InputText(place_holder='4-digit',
                  allowed=string.digits,
                  max_size=4,
                  style={'size': (60, None)})
    ]
    cb = Checkbox(value=True)
    grp = RadioboxGroup()
    fruits = ItemSelect({fruit: fruit for fruit in [
        'apple', 'banana', 'chocolate', 'pear']})
    ages = IntSelect(0, 100, init=20, steps=[1, 5])
    btn_check = Button('check data', link=check)
    btn_disable = Button('disable controls', link=disable)
    tbl.new_row({0: Label('to navigate between controls: TAB or SHIFT+TAB')},
                colspan={0: 2})
    for ip in ips:
        tbl.new_row({0: ip}, colspan={0: 2})
    tbl.new_row({0: cb, 1: Label('a checkbox', label_for=cb)})
    tbl.new_row({0: Label('how are you?')},
                colspan={0: 2})
    for how in ['fine', 'ok', 'not great']:
        cb = Radiobox(grp, how)
        tbl.new_row({0: cb, 1: Label(how, label_for=cb)})
    tbl.new_row({0: Label('select a fruit (mousewheel can be used)')},
                colspan={0: 2})
    tbl.new_row({0: fruits},
                colspan={0: 2})
    tbl.new_row({0: Label('what\'s your age? (mousewheel can be used)')},
                colspan={0: 2})
    tbl.new_row({0: ages},
                colspan={0: 2})
    tbl.new_row({0: Box(btn_disable, btn_check,
                        style={'orientation': 'horizontal'})},
                colspan={0: 2})
    return Window(win_sys, tbl, title=title)


def fonts_window(win_sys, title):
    '''fonts window'''
    def change_name(_):
        lbl.set_style('font', name_select.value)
        return True

    def change_size(_):
        lbl.set_style('font-size', size_select.value)
        return True
    lbl = Label('hey, change my font!', style={'halign': 'center'})
    select = dict()
    select[Style.DEFAULT['font']] = 'default'
    for f in os.listdir(MEDIA_DIR):
        name, ext = os.path.splitext(f)
        abs_path = os.path.abspath(get_media_file(f))
        if ext == '.ttf':
            select[abs_path] = name
    tbl = Table(style={'halign': 'center'})
    name_select = ItemSelect(select)
    size_select = ItemSelect({s: s for s in range(8, 42, 2)}, value=24)
    name_select.add_processor('on-change', change_name)
    size_select.add_processor('on-change', change_size)
    tbl.new_row({0: Label('font name'), 1: name_select})
    tbl.new_row({0: Label('font size'), 1: size_select})
    box = Box(tbl, lbl, style={'expand': True, 'size': ('100%', '100%')})
    return Window(win_sys, box, title=title, style={'size': (500, 200)})


def sounds_window(win_sys, title):
    '''sounds window'''
    click_check_box = get_media_file('click_checkbox.wav')
    key_input_text = get_media_file('key_inputtext.wav')
    over_link = get_media_file('over_link.wav')

    tbl = Table()
    lbl = Label('label')
    lbl.set_style('sound', over_link, ctx='overed')
    tbl.new_row({0: lbl, 1: Label('move over the label to play sound')})
    cb = Checkbox()
    cb.set_style('sound', click_check_box, ctx='activated')
    it = InputText()
    it.set_style('sound', key_input_text, ctx='keyed')
    tbl.new_row({0: cb, 1: Label('check to play sound')})
    tbl.new_row({0: it, 1: Label('type key to play sound')})
    return Window(win_sys, tbl, title=title)


def frames_window(win_sys, title):
    '''frames window'''
    def push():
        if ip.value != '':
            board.pack(Label(ip.value))
        return True
    centered = {'halign': 'center'}
    ip = InputText(place_holder='type something and validate...',
                   style={'size': (400, None), **centered})
    btn = Button('validate', link=push, style=centered)
    board = Box(
        'Enter text and validate.',
        'Text will be added below but the window won\'t grow.')
    frame = Frame(board, style={'expand': True, 'size': ('100%', '100%')})
    box = Box(
        ip, btn, frame,
        style={'expand': True, 'size': ('100%', '100%')})
    result = Window(win_sys, box, title=title, style={'size': (600, 400)})
    return result


def cursor_window(win_sys, title):
    '''cursor window'''
    def close():
        Cursor.deactivate()
        Window.close(result)
    file_elf = get_media_file('elf.png')
    file_cursor_base = get_media_file('cursor-base.png')
    file_cursor_clicked = get_media_file('cursor-clicked.png')
    file_cursor_overed = get_media_file('cursor-overed.png')
    Cursor.set_default(file_cursor_base, ctx=Context.BASE)
    Cursor.activate()

    elf = Image(Media.get_image(file_elf, scale=(128, 128)))
    elf.set_style('cursor', file_cursor_overed, ctx='overed')
    elf.set_style('cursor', file_cursor_clicked, ctx='clicked')
    box = Box(
        Label('move over/click the image to change the cursor'),
        elf)
    result = Window(win_sys, box, title=title)
    result.close = close
    return result


def menus_window(win_sys, title):
    '''menus window'''
    items = dict()
    for m in MONSTERS:
        items[Image(Media.get_image(MONSTERS[m][0], scale=(64, 64)))] = \
            monster_table(m)
    menu = Menu(items, style={'orientation': 'horizontal'})
    result = Window(win_sys, menu, title=title)
    return result


def tooltips_window(win_sys, title):
    '''tooltips window'''
    def new_label(lbl, pos):
        result = Label(lbl, style={'halign': 'center'})
        result.set_tooltip(tooltip, candidate_pos=[pos])
        return result
    tooltip = Box(style=TOOLTIP_STYLE)
    tooltip.pack(Label('this is the tooltip'))
    tooltip.pack(Image(Media.get_image(get_media_file('dragon.png'),
                                      scale=(64, 64))))
    tooltip.pack(Image(Media.get_image(get_media_file('elf.png'),
                                      scale=(64, 64))))
    vpos = [
        ('top', Coord.TOP),
        ('middle', Coord.MIDDLE),
        ('bottom', Coord.BOTTOM)
    ]
    hpos = [
        ('left', Coord.LEFT),
        ('middle', Coord.MIDDLE),
        ('right', Coord.RIGHT)
    ]
    coord_sys = [
        ('absolute', Coord.ABSOLUTE),
        ('relative', Coord.RELATIVE)
    ]

    tbl = Table(style={'halign': 'center'})
    tbl.new_row({0: Label('tooltips can pop when overing an item')},
                colspan={0: 3})
    for clbl, ct in coord_sys:
        tbl.new_row({0: Label('{} positioning'.format(clbl),
                              style={'halign': 'center'})},
                    colspan={0: 3})
        for vlbl, v in vpos:
            tbl.new_row({i: new_label('{} {}'.format(vlbl, hlbl),
                                      (ct, ((h, 0), (v, 0))))
                         for i, (hlbl, h) in enumerate(hpos)})
    return Window(win_sys, tbl, title=title, style={'size': (800, 600)})


def ctx_menus_window(win_sys, title):
    '''contextual menus window'''
    def delete(m):
        def do():
            box.window.clear_popped()
            box.remove(monsters.index(m) + 1)
            monsters.remove(m)
            return True
        return do

    def show(m):
        def do():
            box.window.clear_popped()
            Window(win_sys, monster_table(m), title=m).open()
            return True
        return do
    box = Box()
    box.pack(Label('right-click on a monster to open a contextual menu'))
    monsters = list()
    for m in MONSTERS:
        monsters.append(m)
        menu = Box(style=TOOLTIP_STYLE)
        menu.pack(Label(
            'menu',
            style={'halign': 'center'}))
        menu.pack(Button(
            'delete {}'.format(m),
            link=delete(m),
            style={'halign': 'center'}))
        menu.pack(Button(
            'show {}'.format(m),
            link=show(m),
            style={'halign': 'center'}))
        img = Image(Media.get_image(MONSTERS[m][0], scale=(128, 128)))
        img.set_ctx_menu(menu, candidate_pos=CTX_MENU_CANDIDATE_POS)
        box.pack(img)
    return Window(win_sys, box, title=title)


def maximised_window(win_sys, title):
    '''maximised window'''
    board = TextBoard(style={'size': ('100%', None)})
    with open(get_media_file('lorem_ipsum.txt')) as f:
        text = f.read()
    for paragraph in text.split('\n\n'):
        board.push_text(paragraph)
        board.pack(Empty())
    result = Window(
        win_sys,
        Frame(board, style={'expand': True, 'size': ('100%', '100%')}),
        title=title,
        style={'size': ('100%', '100%')})
    return result


def maximised_menu(win_sys, title):
    '''maximised menu'''
    items = dict()
    boards = {m: TextBoard(style={'size': ('100%', None)}) for m in MONSTERS}
    for m in MONSTERS:
        box = Box(monster_table(m), boards[m], style={'size': ('100%', None)})
        frame = Frame(box,
                      style={'expand': True, 'size': ('100%', '100%')})
        items[Image(Media.get_image(MONSTERS[m][0], scale=(64, 64)))] = frame
    for m in MONSTERS:
        with open(get_media_file('lorem_ipsum.txt')) as f:
            text = f.read()
        for paragraph in text.split('\n\n'):
            boards[m].push_text(paragraph)
            boards[m].pack(Empty())
    node = Menu(items, style={'expand': True, 'size': ('100%', '100%')})
    result = Window(
        win_sys,
        node,
        title=title,
        style={'size': ('100%', '100%')})
    return result


def animations_window(win_sys, title):
    '''animations window'''
    def handler(bound, update):
        def fun(prog):
            g.set_value(prog)
            return prog + update if prog != bound else None
        return fun

    def back():
        stop()
        animations_window.anim = Animation(g.value, 100, handler(0, -1))
        animations_window.anim.start()

    def start():
        stop()
        animations_window.anim = Animation(g.value, 100, handler(100, 1))
        animations_window.anim.start()

    def stop():
        if animations_window.anim is not None:
            animations_window.anim.stop()
            animations_window.anim = None

    g = Gauge(0, 100, 0, style={'halign': 'center'})
    animations_window.anim = Animation(g.value, 100, handler(100, 1))

    buttons = Box(style={'orientation': 'horizontal'})
    buttons.pack(Button('back', link=back))
    buttons.pack(Button('stop', link=stop))
    buttons.pack(Button('go', link=start))

    box = Box()
    box.pack(g)
    box.pack(buttons)
    return Window(win_sys, box, title=title)


def absolute_positioning_window(win_sys, title):
    '''absolute positioning window'''
    def handler(directions):
        size = win.size
        result = []
        for i, img in enumerate(imgs):
            direction = directions[i]
            pos = (Coord.sum(img.pos, direction))
            pos = ('left', pos[0]), ('top', pos[1])
            win.set_floating_node_pos(img, pos)
            next_pos = (Coord.sum(img.pos, direction))
            if next_pos[1] + img.size[1] > size[1] or next_pos[1] < 0:
                direction = (direction[0], -direction[1])
            if next_pos[0] + img.size[0] > size[0] or next_pos[0] < 0:
                direction = (-direction[0], direction[1])
            result.append(direction)
        return result

    def start_or_stop():
        if btn.node.text == 'stop':
            anim.pause()
            btn.node.set_text('start')
        else:
            anim.start()
            btn.node.set_text('stop')
    btn = Button(
        'start',
        link=start_or_stop,
        style={'expand': True, 'halign': 'center', 'valign': 'center'})
    box = Box(btn, style={'expand': True, 'size': ('100%', '100%')})
    win = Window(win_sys, box, title=title, style={'size': (600, 400)})
    result = win
    img_size = 128
    imgs = [
        Image(Media.get_image(MONSTERS[m][0], scale=(img_size, img_size)))
        for m in MONSTERS
    ]
    directions = []
    for img in imgs:
        pos = (('left', random.randint(0, 400 - img_size)),
               ('top', random.randint(0, 400 - img_size)))
        directions.append((random.choice([5, -5]), random.choice([5, -5])))
        result.add_floating_node(img, pos)
    anim = Animation(directions, 10, handler)
    return result


def text_boards_window(win_sys, title):
    '''text boards window'''
    board = TextBoard(style={'size': (400, None)})
    board.push_text('''Text boards can be used to draw long texts that should
not exceed a specific width. Here the text board width has been set to 400
and the board has been put inside a 150-height frame.''')
    board.push_text('''Text boards and labels can contain
<color rgb="200,50,50">colored text</color>. You can do this by putting color
tags in your text.  For instance, this has been generated by the following
code:''')
    board.push_text('''&lt;color rgb="200,50,50"&gt;colored
text&lt;/color&gt;.''')
    frame = Frame(board, style={'expand': True, 'size': (None, 150)})
    return Window(win_sys, frame, title=title)


def user_controls_window(win_sys, title):
    '''user controls window'''
    def close():
        StyleClass.rem('window')
        StyleClass.rem('frame')
        StyleClass.rem('item-select')
        StyleClass.rem('int-select')
        StyleClass.rem('checkbox')
        StyleClass.rem('radiobox')
        StyleClass.rem('img-button')
        StyleClass.rem('input-text')
        Window.close(result)
        DefaultStyle.load()

    def get_imgs(prefix):
        return tuple(map(imgs.get, filter(
            lambda img: img.startswith(prefix + '-'), imgs)))

    ctxs = ['base', 'overed', 'disabled']
    imgs = [
        *['button-' + ctx for ctx in ctxs + ['clicked']],
        *['item-select-' + direct + '-' + ctx
          for direct in ['prev', 'next'] for ctx in ctxs],
        *['int-select-' + direct + '-' + ctx
          for direct in ['prev', 'next'] for ctx in ctxs],
        *['checkbox-' + value + '-' + ctx
          for value in ['true', 'false']
          for ctx in ctxs],
        *['radiobox-' + value + '-' + ctx
          for value in ['true', 'false']
          for ctx in ctxs],
        *['frame-vscroll-' + which + '-' + where
          for which in ['container', 'bar']
          for where in ['top', 'unit', 'bottom']],
        *['hrule-' + where
          for where in ['left', 'unit', 'right']],
        *['vrule-' + where
          for where in ['top', 'unit', 'bottom']],
        *['window-border-' + where
          for where in ['top-left', 'top-right', 'bottom-right', 'bottom-left',
                        'horizontal', 'vertical']],
        'window-cross',
        'input-text'
    ]
    imgs = {
        name: get_media_file(name + '.png') for name in imgs
    }

    #  class for rules
    StyleClass.get(Rule).set_style({
        'base': {
            'image-hrule': get_imgs('hrule'),
            'image-vrule': get_imgs('vrule'),
            'orientation': 'horizontal'
        }
    })

    #  class for windows
    StyleClass('window').set_style({
        'base': {
            'padding': 10,
            'border': 'image',
            'image-border': get_imgs('window-border'),
            'background': 'color',
            'corner': 0,
            'color-background': (10, 10, 0),
            'image-window-cross': imgs['window-cross']
        }
    })

    #  class for frames
    StyleClass('frame').set_style({
        'base': {
            'padding': 10,
            'image-frame-vscroll-container':
            tuple(map(imgs.get, filter(
                lambda img: img.startswith(
                    'frame-vscroll-container-'), imgs))),
            'image-frame-vscroll-bar':
            tuple(map(imgs.get, filter(
                lambda img: img.startswith(
                    'frame-vscroll-bar-'), imgs))),
            'border': 'image',
            'image-border': get_imgs('window-border')
        }
    })

    #  class for selects
    StyleClass('item-select').set_style({
        ctx: {
            'border': None,
            'padding': 0,
            'image-select': tuple([imgs['item-select-' + d + '-' + ctx]
                                   for d in ['prev', 'next']])
        } for ctx in ctxs
    })

    #  class for int-selects
    StyleClass('int-select').set_style({
        ctx: {
            'border': None,
            'padding': 0,
            'image-select': tuple([imgs['int-select-' + d + '-' + ctx]
                                   for d in ['prev', 'next']])
        } for ctx in ctxs
    })

    #  class for checkboxes
    StyleClass('checkbox').set_style({
        ctx: {
            'border': None,
            'padding': 0,
            'image-checkbox': tuple([imgs['checkbox-' + d + '-' + ctx]
                                     for d in ['false', 'true']])
        } for ctx in ctxs
    })

    #  class for radioboxes
    StyleClass('radiobox').set_style({
        ctx: {
            'border': None,
            'padding': 0,
            'image-checkbox': tuple([imgs['radiobox-' + d + '-' + ctx]
                                     for d in ['false', 'true']])
        } for ctx in ctxs
    })

    #  class for buttons
    StyleClass('img-button').set_style({
        ctx: {
            'border': None,
            'padding': 0,
            'background': 'image',
            'image-background': imgs['button-' + ctx]
        } for ctx in ctxs + ['clicked']
    })

    #  class for input texts
    StyleClass('input-text').set_style({
        'base': {
            'border': None,
            'background': 'image',
            'padding': (10, 0),
            'image-background': imgs['input-text']
        },
        'overed': {
            'color': (100, 100, 0)
        },
        'focus': {
            'color': (233, 233, 0)
        }
    })

    tbl = Table()

    #  name input text
    ctrl = InputText(cls=['input-text'])
    tbl.new_row({0: Label('name'), 1: ctrl})
    tbl.new_row({1: Rule()})

    #  class radioboxes
    class_grp = RadioboxGroup()
    ctrl = {
        c: Box(
            Radiobox(class_grp, c, value=c == 'warrior', cls=['radiobox']),
            Label(c),
            style={'orientation': 'horizontal'})
        for c in ['warrior', 'wizard', 'thief']
    }
    tbl.new_row({0: Label('class'), 1: ctrl['warrior']})
    tbl.new_row({1: ctrl['wizard']})
    tbl.new_row({1: ctrl['thief']})
    tbl.new_row({1: Rule()})

    #  level int-select
    ctrl = IntSelect(1, 10, cls=['int-select'])
    tbl.new_row({0: Label('level'), 1: ctrl})
    tbl.new_row({1: Rule()})

    #  weapon select
    ctrl = ItemSelect(
        {weapon: weapon for weapon in ['sword', 'axe', 'bow', 'staff']},
        cls=['item-select'])
    tbl.new_row({0: Label('weapon'), 1: ctrl})
    tbl.new_row({1: Rule()})

    #  skill checkboxes
    ctrl = {skill: Box(Checkbox(cls=['checkbox'], style={'valign': 'center'}),
                       Label(skill, style={'valign': 'center'}),
                       style={'orientation': 'horizontal'})
            for skill in ['long sword', 'axe', 'bow', 'magic', 'dodge',
                          'lockpicking', 'cartography', 'kung-fu', 'yoyo',
                          'gaming']}
    box = Box(*ctrl.values())
    tbl.new_row({0: Label('skills', style={'valign': 'top'}),
                 1: Frame(box, cls=['frame'], style={'size': (300, 200)})})

    #  button
    ctrl = Button('start', cls=['img-button'], style={'halign': 'center'})
    tbl.new_row({0: ctrl}, colspan={0: 2})

    result = Window(
        win_sys, tbl,
        title=title,
        cls=['window'])
    result.close = close
    return result


def grids_window(win_sys, title):
    '''grids window'''
    def add(img):
        def fun():
            def link():
                new.set_selected(not new.is_selected())
                return True
            new = Image(img.surface, link=link)
            grid.insert(0, new)
            return True
        return fun

    def delete():
        to_del = [img for img in grid if img.is_selected()]
        for node in to_del:
            grid.remove_node(node)
        return True
    size = 64, 64
    imgs = [
        Image(Media.get_image(get_media_file(f), scale=size))
        for f in ['elf.png', 'orc.png', 'dragon.png']
    ]
    for img in imgs:
        img.set_link(add(img))
    grid = Grid(style={'size': ('100%', None)})
    board = TextBoard(style={'size': ('100%', None)})
    board.push_text('''Click on an image to add it in the frame.  You can then
select images in the frame and click on delete to remove them from the frame.
The box in the frame will not hold more than 5 images per row.  Deletion will
automatically rearrange the box.''')
    box_main = Box(
        board,
        Box(*imgs,
            Label('delete', link=delete, style={'valign': 'center'}),
            style={'orientation': 'horizontal', 'halign': 'center'}),
        Frame(grid, style={'size': (400, 400)}))
    return Window(win_sys, box_main, title=title)


def go():
    '''launch the test'''

    #  configure logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s;%(module)s;%(message)s')
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    def top_panel():
        def open_win(fun, title):
            return lambda: fun(win_sys, title).open()

        def quit_test():
            win_sys.set_closed(True)
        tbl = Table()
        buttons = [
            ('basic window', basic_window),
            ('tables', tables_window),
            ('controls', controls_window),
            ('fonts', fonts_window),
            ('sounds', sounds_window),
            ('cursor', cursor_window),
            ('frames', frames_window),
            ('menus', menus_window),
            ('tooltips', tooltips_window),
            ('text boards', text_boards_window),
            ('maximised window', maximised_window),
            ('maximised menu', maximised_menu),
            ('contextual menus', ctx_menus_window),
            ('animations', animations_window),
            ('absolute positioning', absolute_positioning_window),
            ('user controls', user_controls_window),
            ('grids', grids_window)
        ]
        row = dict()
        for title, fun in buttons:
            row[len(row)] = Button(title, link=open_win(fun, title))
            if len(row) == 5:
                tbl.new_row(row)
                row = dict()
        row[len(row)] = Button('quit', link=quit_test)
        tbl.new_row(row)
        return Panel(
            win_sys, Frame(tbl, style={'expand': True,
                                       'border': None,
                                       'size': ('100%', '100%')}),
            style={'size': ('100%', '100%')})

    pg.init()
    pg.mixer.init()
    pg.font.init()
    screen = pg.display.set_mode((1200, 800))
    pg.display.set_caption('pygwin v{} - test application'.format(VERSION))
    DefaultStyle.load()
    win_sys = WindowSystem(screen)
    p = top_panel()
    p.open(pos=(0, 0))
    pg.key.set_repeat(100, 50)

    clock = pg.time.Clock()
    win_sys.draw(update=True)

    #  main loop
    while not win_sys.closed:
        win_sys.run_animations()
        for pgevt in pg.event.get():
            if pgevt.type == pg.QUIT:
                win_sys.set_closed(True)
            win_sys.process_pg_event(pgevt)
        win_sys.draw(update=True)
        clock.tick(FPS)

    pg.quit()
    sys.exit(0)


if __name__ == '__main__':
    go()
