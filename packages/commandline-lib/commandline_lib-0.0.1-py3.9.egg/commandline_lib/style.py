"""
Colorful Style File
"""
from commandline_lib import colorful
from os import system
from sys import stdout, stdin
import time


EMPTY = ""


class BaseStyle:
    """
    Base Style Define
    """
    fore = EMPTY
    back = EMPTY
    typewriter = False
    input_stream = stdin
    output_stream = stdout
    typewriter_inv = 0

    def how_to_print(self, data) -> None:
        """
        Rewritable function!
        Say to the Base Style How to print some data

        Parameters
        ----------
        data: str
            String will be print

        Returns
        -------
        None

        """
        self.output_stream.write(data)

    def how_to_clear(self) -> None:
        """
        Rewritable function!
        Say to the Base Style How to clear all the data

        Returns
        -------
        None

        """
        system("cls")

    def how_to_input(self) -> str:
        """
        Rewritable function!
        Say to the Base Style How to input some data

        Returns
        -------
        Input Answer(Includes line breaks at the end of the line)

        """
        return self.input_stream.readline()

    def input(self):
        return self.how_to_input()

    def clear(self):
        return self.how_to_clear()

    def echo(self, value):
        """
        Echo Function

        Parameters
        ----------
        value:str
            Data will be print.

        Returns
        -------
        None
        """
        self.output_stream.write(self.fore)
        self.output_stream.write(self.back)
        if self.typewriter:
            for i in str(value):
                self.output_stream.write(i)
                time.sleep(self.typewriter_inv)
        else:
            self.output_stream.write(str(value))

        self.output_stream.write(colorful.get_back_reset())
        self.output_stream.write(colorful.get_fore_reset())


class BlackRedStyle(BaseStyle):
    """
    A Example Style
    Fore is red
    Back is black
    Like a slow typewriter.
    """
    fore = colorful.get_fore_color("red")
    back = colorful.get_back_color("black")
    typewriter = True
    typewriter_inv = 1



