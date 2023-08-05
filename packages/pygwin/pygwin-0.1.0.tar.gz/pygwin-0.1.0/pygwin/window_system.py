#!/usr/bin/env python3

'''definition of class WindowSystem'''

import pygame as pg

from . import Animation, Coord, Cursor, Util, Context


class WindowSystem:  # pylint: disable=R0902
    '''@TODO@'''

    def __init__(self, screen):
        '''initialize a window system in the given screen surface, e.g., the
        result of pygame.display.set_mode(...)'''
        self.__surface = pg.Surface(screen.get_size())
        self.__screen = screen
        self.__windows = list()
        self.__panels = set()
        self.__updated = list()
        self.__redraw_all = True
        self.__redraw_cursor = True
        self.__closed = False

    @property
    def screen(self):
        '''get the screen surface this window system is attached to'''
        return self.__screen

    @property
    def closed(self):
        '''check if the window system is closed'''
        return self.__closed

    def set_closed(self, closed):
        '''@TODO@'''
        self.__closed = closed

    def top_window(self):
        '''get the top window of the system (i.e., the last opened window) or
        None if no window is currently opened'''
        if self.__windows == []:
            result = None
        else:
            result = self.__windows[0]
        return result

    def center_window(self, win):
        '''center window object win in the window system'''
        sw, sh = self.__surface.get_size()
        win.compute_size()
        w, h = win.size
        win.set_absolute_pos((int((sw - w) / 2), int((sh - h) / 2)))

    def open_window(self, win, pos=None):
        '''open Window win in the window system.  win is position at position
        pos if not None or otherwise centered'''
        self.__windows.insert(0, win)
        if pos is None:
            self.center_window(win)
        else:
            win.set_absolute_pos(pos)

    def window_opened(self, win):
        '''check if window win has been opened in the window system'''
        return win in self.__windows or win in self.__panels

    def close_window(self, win):
        '''close window win in the window system.  if win is None, the top
        window is closed'''
        if win is None:
            if self.__windows == []:
                return
            win = self.__windows[0]
        if win in self.__windows:
            self.__windows = list(filter(lambda w: w != win, self.__windows))

    def close_all_windows(self):
        '''close all the windows of the system'''
        self.__windows = []

    def center_all_windows(self):
        '''center all windows of the system'''
        for win in self.__windows:
            self.center_window(win)

    def open_panel(self, panel, pos):
        '''open panel in the window system at position pos'''
        self.__panels.add(panel)
        panel.set_absolute_pos(pos)

    def close_panel(self, panel):
        '''close panel in the window system'''
        if panel in self.__panels:
            self.__panels.remove(panel)

    def process_pg_event(self, pgevt):
        '''process pygame event pgevt.  return True if the event has been
        processed, False otherwise'''
        def dispatch():
            result = False
            for win in self.__windows + list(self.__panels):
                result = win.process_pg_event(pgevt)
                if result or win.modal:
                    break
            return result

        #  update the cursor image
        if pgevt.type == pg.MOUSEBUTTONDOWN:
            if pgevt.button == Util.MOUSEBUTTON_LEFT:
                Cursor.set_context(Context.CLICKED)
        elif pgevt.type == pg.MOUSEBUTTONUP:
            if pgevt.button == Util.MOUSEBUTTON_LEFT:
                Cursor.unset_context(Context.CLICKED)

        result = dispatch()
        self.__redraw_all = self.__redraw_all or result
        self.__redraw_cursor = self.__redraw_cursor or \
            (Cursor.activated() and pgevt.type in [
                pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.MOUSEMOTION])
        return result

    def draw(self, update=False):
        '''draw the window system (i.e., all opened windows and panels) in its
        screen surface.  call pygame.display.update if update=True'''
        if self.__redraw_all:
            self.__surface.fill((0, 0, 0))
            for win in list(self.__panels) + self.__windows[::-1]:
                win.blit(self.__surface)
            self.__screen.blit(self.__surface, (0, 0))
            self.__draw_cursor()
            if update:
                pg.display.update()
        elif self.__redraw_cursor:
            self.__screen.blit(self.__surface, (0, 0))
            self.__draw_cursor()
            pg.display.update()
        self.__redraw_all = False
        self.__redraw_cursor = False

    def update_window(self, win, surface, rect, update):
        '''@TODO@'''
        x, y, w, h = rect
        pt = Coord.sum((x, y), win.absolute_pos)
        pt = x, y
        self.__surface.blit(surface, pt, area=(0, 0, w, h))
        self.__updated.append(rect)
        if update:
            self.update_display()

    def update_display(self):
        '''@TODO@'''
        self.__draw_cursor()
        self.__screen.blit(self.__surface, (0, 0))
        pg.display.update(self.__updated)
        self.__updated = list()

    def set_surface(self, screen):
        '''@TODO@'''
        self.__screen = screen
        self.__surface = pg.Surface(screen.get_size())

    def run_animations(self):
        '''@TODO@'''
        self.__redraw_all = Animation.run_all() or self.__redraw_all

    def __draw_cursor(self):
        if Cursor.activated():
            Cursor.draw(self.__screen, pg.mouse.get_pos())
