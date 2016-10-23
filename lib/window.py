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
            curses.noecho()
            curses.cbreak()
            self.std.keypad(1)

            self.data = self.std.subwin(curses.LINES - 4, curses.COLS - 1, 1, 0)
            self.data.scrollok(True)
            self.prompt = curses.newwin(1, curses.COLS - 3, curses.LINES - 2, 1)
            rectangle(self.std, curses.LINES - 3, 0, curses.LINES - 1, curses.COLS - 2)
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
