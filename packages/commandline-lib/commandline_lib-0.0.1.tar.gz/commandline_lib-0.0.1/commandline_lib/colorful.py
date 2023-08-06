"""
Command Line Library Colorful File
This function depends on the colorama library! Please be careful to upgrade!
"""

import colorama


def get_fore_color(string="black"):
    """
    Get the fore color placeholder or reset placeholder use 'colorama' module

    Parameters
    ----------
    string: str
        Case - insensitive color names

    Returns
    -------
    Fore color placeholder( Don't Print it')

    Examples
    --------

    >>> from commandline_lib import colorful
    >>> print(repr(colorful.get_fore_color("red")))
    '\\x1b[31m'



    """
    string = string.upper()
    try:
        return str(eval("colorama.Fore." + string))
    except:
        raise ValueError("Can't find this color <" + string + ">.")


def get_fore_reset():
    """
    get_fore_color Reset mode encapsulation

    Returns
    -------
    Reset Mode Placeholder

    """
    return get_fore_color("reset")


def foreground_replace(text="Hello World", color="red"):
    """
    Fore quick Settings, for the print function in the Python standard library

    Parameters
    ----------
    text: str
        The Text with no color.
    color: str
        Color Name

    Returns
    -------
    Colored Text
    """
    return get_fore_color(color) + text + get_fore_reset()


def get_back_color(string="white"):
    """
    Get the back color placeholder or reset placeholder use 'colorama' module

    Parameters
    ----------
    string: str
        Case - insensitive color names

    Returns
    -------
    Back color placeholder( Don't Print it)

    """
    string = string.upper()
    try:
        return str(eval("colorama.Back." + string))
    except:
        raise ValueError("Can't find this color <" + string + ">.")


def get_back_reset():
    """
    get_back_color Reset mode encapsulation

    Returns
    -------
        Reset Mode Placeholder

    """
    return get_back_color("reset")


def background_replace(text="Hello World", color="red"):
    """
        Back quick Settings, for the print function in the Python standard library

    Parameters
    ----------
        text: str
            The Text with no color.
        color: str
            Color Name

    Returns
    -------
        Colored Text
    """
    return get_back_color(color) + text + get_back_reset()


def colorful(text="Hello World", fore="red", back="black"):
    """
    Colorful Text

    Parameters
    ----------
    text: str
        Text with no color
    fore: str
        fore color name
    back: str
        back color name

    Returns
    -------
    Colored Text
    """
    return get_fore_color(fore) + get_back_color(back) + text + get_back_reset() + get_fore_reset()


