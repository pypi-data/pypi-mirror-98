'''
Date: 2020-12-01 08:59:33
LastEditors: Rustle Karl
LastEditTime: 2021-03-12 12:20:44
'''
import os

# 是否启用颜色
__enable_color = os.getenv("TERM_COLOR", "enable") != "disable"

# 中断颜色
__unset_color = "\033[0m"


class Color(object):
    Black = "black"
    Red = "red"
    Green = "green"
    Yellow = "yellow"
    Blue = "blue"
    Magenta = "magenta"
    Cyan = "cyan"
    White = "white"

    # 浅色粗体
    LightBlack = "light_black"
    LightRed = "light_red"
    LightGreen = "light_green"
    LightYellow = "light_yellow"
    LightBlue = "light_blue"
    LightMagenta = "light_magenta"
    LightCyan = "light_cyan"
    LightWhite = "light_white"

    # 背景色
    BgBlack = "bg_black"
    BgRed = "bg_red"
    BgGreen = "bg_green"
    BgYellow = "bg_yellow"
    BgBlue = "bg_blue"
    BgMagenta = "bg_magenta"
    BgCyan = "bg_cyan"
    BgWhite = "bg_white"

    # 浅背景色
    LightBgBlack = "light_bg_black"
    LightBgRed = "light_bg_red"
    LightBgGreen = "light_bg_green"
    LightBgYellow = "light_bg_yellow"
    LightBgBlue = "light_bg_blue"
    LightBgMagenta = "light_bg_magenta"
    LightBgCyan = "light_bg_cyan"
    LightBgWhite = "light_bg_white"


__color_dict = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",

    "light_black": "1;30",
    "light_red": "1;31",
    "light_green": "1;32",
    "light_yellow": "1;33",
    "light_blue": "1;34",
    "light_magenta": "1;35",
    "light_cyan": "1;36",
    "light_white": "1;37",

    "bg_black": "40",
    "bg_red": "41",
    "bg_green": "42",
    "bg_yellow": "43",
    "bg_blue": "44",
    "bg_magenta": "45",
    "bg_cyan": "46",
    "bg_white": "47",

    "light_bg_black": "100",
    "light_bg_red": "101",
    "light_bg_green": "102",
    "light_bg_yellow": "103",
    "light_bg_blue": "104",
    "light_bg_magenta": "105",
    "light_bg_cyan": "106",
    "light_bg_white": "107",
}

__red = "31"


def convert_color(color: str) -> str:
    return __color_dict.get(color, __red)


def set_color(color: str) -> str:
    if not __enable_color:
        return ""

    return "\033[%sm" % convert_color(color)


def unset_color(msg: str):
    if not __enable_color:
        return msg

    return msg + __unset_color


def scolorf(color: str, msg: str) -> str:
    if not __enable_color:
        return msg

    return "\033[%sm%s\033[0m" % (convert_color(color), msg)


def colorln(color: str, msg: str):
    print(scolorf(color, msg))


def sblackf(msg, light=False) -> str:
    return scolorf(Color.LightBlack if light else Color.Black, msg)


def blackln(msg, light=False):
    colorln(Color.LightBlack if light else Color.Black, msg)


def sredf(msg, light=False):
    return scolorf(Color.LightRed if light else Color.Red, msg)


def redln(msg, light=False):
    colorln(Color.LightRed if light else Color.Red, msg)


def sgreenf(msg, light=False):
    return scolorf(Color.LightGreen if light else Color.Green, msg)


def greenln(msg, light=False):
    colorln(Color.LightGreen if light else Color.Green, msg)


def syellowf(msg, light=False):
    return scolorf(Color.LightYellow if light else Color.Yellow, msg)


def yellowln(msg, light=False):
    colorln(Color.LightYellow if light else Color.Yellow, msg)


def sbluef(msg, light=False):
    return scolorf(Color.LightBlue if light else Color.Blue, msg)


def blueln(msg, light=False):
    colorln(Color.LightBlue if light else Color.Blue, msg)


def smagentaf(msg, light=False):
    return scolorf(Color.LightMagenta if light else Color.Magenta, msg)


def magentaln(msg, light=False):
    colorln(Color.LightMagenta if light else Color.Magenta, msg)


def scyanf(msg, light=False):
    return scolorf(Color.LightCyan if light else Color.Cyan, msg)


def cyanln(msg, light=False):
    colorln(Color.LightCyan if light else Color.Cyan, msg)


def swhitef(msg, light=False):
    return scolorf(Color.LightWhite if light else Color.White, msg)


def whiteln(msg, light=False):
    colorln(Color.LightWhite if light else Color.White, msg)


if __name__ == "__main__":
    blackln('come on')
    blackln('come on', True)

    redln('come on')
    redln('come on', True)

    greenln('come on')
    greenln('come on', True)

    yellowln('come on')
    yellowln('come on', True)

    blueln('come on')
    blueln('come on', True)

    magentaln('come on')
    magentaln('come on', True)

    cyanln('come on')
    cyanln('come on', True)

    whiteln('come on')
    whiteln('come on', True)
