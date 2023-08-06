from textwrap import wrap

from django import template

register = template.Library()


def hex_notation(value, arg=":"):
    if arg.lower() == "no":
        "".join(wrap(hex(value).split('x')[1], 2))
    if arg == "-":
        "-".join(wrap(hex(value).split('x')[1], 2))
    return ":".join(wrap(hex(value).split('x')[1], 2))


register.filter('hex_notation', hex_notation)
