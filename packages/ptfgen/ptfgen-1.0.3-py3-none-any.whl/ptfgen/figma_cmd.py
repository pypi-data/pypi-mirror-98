# coding=utf-8

import re
from jinja2 import Environment, PackageLoader
from .pb import pasteboard_write
from .command import Command
from .constants import DART_TYPES_DEFAULT_VALUES, DART_TYPES
from .str_helpers import upper_first_letter
import cssutils

class FigmaCommand(Command):
    def __init__(self, css_text):
        super(FigmaCommand, self).__init__()
        self.css_text = css_text

    def create_text(self, print_result):
        output = Figma(self.css_text).create_text()
        if print_result:
            print()
            print(output)
            print()
        pasteboard_write(output)
        print('The result has been copied to the pasteboard.')


class Figma(object):
    def __init__(self, css_text):
        super(Figma, self).__init__()
        self.css_text = "text { %s }" % (css_text)
    
    def create_text(self):
        format = "Text('', style: TextStyle( fontFamily: FontFamily.%s, fontStyle: FontStyle.%s, color: Color(0xff%s), fontSize: %s.sp, fontWeight: FontWeight.%s, height: 1), ),";
        print(self.css_text)
        dct = {}
        sheet = cssutils.parseString(self.css_text)
        for rule in sheet:
            styles = rule.style.cssText
            for property in rule.style:
                name = property.name    
                value = property.value
                dct[name] = value;
                print("%s - %s" % (name, value))
        font_family = dct["font-family"].lower()
        font_style = dct["font-style"].lower()
        font_weight = dct["font-weight"].lower()
        font_color = dct["color"].lower().replace("#", "")
        font_size = dct["font-size"].lower().replace("px", "")

        return format % (font_family, font_style, font_color, font_size, font_weight)

