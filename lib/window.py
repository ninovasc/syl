# -*- coding: utf-8 -*-
"""modulo para o curses"""
import curses
from curses.textpad import Textbox, rectangle
import traceback


class Window(object):
    """Classe de parametrizacao e inicializacao do curses"""
    def __init__(self):

        try:
            self.std = curses.initscr()

            curses.start_color()
            curses.use_default_colors()

            gray = curses.COLOR_WHITE + 1
            curses.init_color(gray, 200, 200, 200)
            blue = gray + 1
            curses.init_color(blue, 400, 400, 1000)
            red = blue + 1
            curses.init_color(red, 1000, 400, 400)

            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
            self.text_color=curses.color_pair(1)

            curses.init_pair(2, curses.COLOR_GREEN, gray)
            self.header_color=curses.color_pair(2)

            curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
            self.input_color=curses.color_pair(3)

            curses.init_pair(4, blue, curses.COLOR_BLACK)
            self.server_color=curses.color_pair(4)

            curses.init_pair(5, red, curses.COLOR_BLACK)
            self.private_color=curses.color_pair(5)

            self.std.bkgdset(ord(' '), self.text_color)
            self.std.clear()
            self.std.refresh()

            curses.noecho()
            curses.cbreak()
            self.std.keypad(1)

            self.header = self.std.subwin(1, curses.COLS, 0, 0)
            self.header.bkgdset(ord(' '), self.header_color)
            self.header.clear()
            self.header.refresh()

            self.data = self.std.subwin(curses.LINES - 4, curses.COLS - 1, 1, 0)
            self.data.scrollok(True)

            self.prompt = curses.newwin(0, curses.COLS, curses.LINES - 1, 0)
            self.prompt.bkgdset(ord(' '), self.input_color)
            self.prompt.clear()
            self.prompt.refresh()

            #self.input_rectangle=self.std.subwin(2, curses.COLS - 1, curses.LINES - 2, 0)
            #self.input_rectangle.bkgdset(ord(' '), curses.color_pair(3))
            #self.input_rectangle.clear()
            #self.input_rectangle.refresh()
            #rectangle(self.input_retangle, curses.LINES - 3, 0, curses.LINES - 1, curses.COLS - 2)
            self.tex = Textbox(self.prompt)

            self.std.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

        except:

            self.std.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            traceback.print_exc()

    def close(self):
        """Metodo para finalizar o curses"""
        self.std.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def addstr_header(self, _str):
        self.header.addstr(_str, self.header_color)
        self.header.refresh()

    def addstr_data(self, _str, _type):
        if _type == "server":
            self.data.addstr(_str, self.server_color)
        elif _type == "private":
            self.data.addstr(_str, self.private_color)
        else:
            self.data.addstr(_str, self.text_color)
        self.data.refresh()

    def clear_header(self):
        self.header.clear()
        self.data.refresh()

    def clear_data(self):
        self.data.clear()
        self.data.refresh()


