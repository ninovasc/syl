# -*- coding: utf-8 -*-
"""
Control terminal window in client using Curses
"""
import curses
from curses.textpad import Textbox, rectangle
import traceback


class Window(object):
    """
    @brief      Class for window control using Curses.
    """
    def __init__(self):
        """
        @brief      Constructs the object.

        @param      self   The object
        """
        curses.wrapper(self.start)

    def start(self,std):
        """
        @brief      Start all Curses windows: a standard window, a header
                    window, a data window and a input window.

        @param      self  The object
        @param      std   The standard window

        @return     Only create windows to client.
        """
        try:
            self.std=std

            gray = curses.COLOR_WHITE + 1
            curses.init_color(gray, 200, 200, 200)
            blue = gray + 1
            curses.init_color(blue, 400, 400, 1000)
            red = blue + 1
            curses.init_color(red, 1000, 400, 400)
            max_red = red + 1
            curses.init_color(red, 1000, 0, 0)

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

            curses.init_pair(6, red, curses.COLOR_BLACK)
            self.error_color=curses.color_pair(6)

            self.std.bkgdset(ord(' '), self.text_color)
            self.std.clear()
            self.std.refresh()

            self.header = self.std.subwin(1, curses.COLS, 0, 0)
            self.header.bkgdset(ord(' '), self.header_color)
            self.header.clear()
            self.header.refresh()

            self.data = self.std.subwin(curses.LINES - 2, curses.COLS - 1, 1, 0)
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

        except:

            self.std.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            traceback.print_exc()

    def close(self):
        """
        @brief      { function_description }

        @param      self  The object

        @return     { description_of_the_return_value }
        """

        #self.std.keypad(0)
        #curses.echo()
        #curses.nocbreak()
        curses.endwin()

    def addstr_header(self, _str):
        """
        @brief      Add text to header window.

        @param      self  The object
        @param      _str  The string

        @return     void method.
        """
        self.header.addstr(_str, self.header_color)
        self.header.refresh()

    def addstr_data(self, _str, _type):
        """
        @brief      Add text to data window, depending of type, the color is
                    different.

        @param      self   The object
        @param      _str   The string
        @param      _type  The type

        @return     void method.
        """
        if _type == "server":
            self.data.addstr(_str, self.server_color)
        elif _type == "private":
            self.data.addstr(_str, self.private_color)
        elif _type == "error":
            self.data.addstr(_str, self.error_color)
        else:
            self.data.addstr(_str, self.text_color)
        self.data.refresh()

    def clear_header(self):
        """
        @brief      Clear header window.

        @param      self  The object

        @return     void method.
        """
        self.header.clear()
        self.data.refresh()

    def clear_data(self):
        """
        @brief      clear data window.

        @param      self  The object

        @return     void method.
        """
        self.data.clear()
        self.data.refresh()


