#!/usr/bin/env python
"""html2text: Turn HTML into equivalent Markdown-structured text."""
__version__ = "3.200.3"
__author__ = "Aaron Swartz (me@aaronsw.com)"
__copyright__ = "(C) 2004-2008 Aaron Swartz. GNU GPL 3."
__contributors__ = ["Martin 'Joey' Schulze", "Ricardo Reyes", "Kevin Jay North"]

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urlparse
import sys
import argparse
import re

@dataclass(frozen=True)
class Config:
    unicode_snob: int
    escape_snob: int
    ignore_links: bool
    ignore_images: bool
    google_doc: bool
    dash_unordered_list: bool
    body_width: int
    google_list_indent: int
    hide_strikethrough: bool

default_config = Config(
    unicode_snob=0,
    escape_snob=0,
    ignore_links=False,
    ignore_images=False,
    google_doc=False,
    dash_unordered_list=False,
    body_width=78,
    google_list_indent=36,
    hide_strikethrough=False
)

unifiable = {
    'rsquo': "'", 'lsquo': "'", 'rdquo': '"', 'ldquo': '"',
    'copy': '(C)', 'mdash': '--', 'nbsp': ' ', 'rarr': '->',
    'larr': '<-', 'middot': '*', 'ndash': '-', 'oelig': 'oe',
    'aelig': 'ae', 'agrave': 'a', 'aacute': 'a', 'acirc': 'a',
    'atilde': 'a', 'auml': 'a', 'aring': 'a', 'egrave': 'e',
    'eacute': 'e', 'ecirc': 'e', 'euml': 'e', 'igrave': 'i',
    'iacute': 'i', 'icirc': 'i', 'iuml': 'i', 'ograve': 'o',
    'oacute': 'o', 'ocirc': 'o', 'otilde': 'o', 'ouml': 'o',
    'ugrave': 'u', 'uacute': 'u', 'ucirc': 'u', 'uuml': 'u',
    'lrm': '', 'rlm': ''
}

class HTML2Text(HTMLParser):
    def __init__(self, baseurl=''):
        super().__init__()
        self.baseurl = baseurl
        self.outtextlist = []
        self.current_output = ''
        self.stack = []
        self.absolute_url_matcher = re.compile(r'^[a-zA-Z+]+://')

    def handle(self, data):
        self.feed(data.replace("</script>", "</ignore>"))
        return ''.join(self.outtextlist)

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.stack:
            self.stack.remove(tag)

    def handle_data(self, data):
        self.outtextlist.append(data)

def parse_args():
    parser = argparse.ArgumentParser(description="Convert HTML to Markdown.")
    parser.add_argument("--ignore-links", action="store_true", help="Don't include any formatting for links")
    parser.add_argument("--ignore-images", action="store_true", help="Don't include any formatting for images")
    parser.add_argument("-g", "--google-doc", action="store_true", help="Convert an HTML-exported Google Document")
    parser.add_argument("-d", "--dash-unordered-list", action="store_true", help="Use dash for unordered list items")
    parser.add_argument("-b", "--body-width", type=int, help="Number of characters per output line")
    parser.add_argument("-i", "--google-list-indent", type=int, help="Pixels Google indents nested lists")
    parser.add_argument("-s", "--hide-strikethrough", action="store_true", help="Hide strike-through text")
    return parser.parse_args()

def config_from_args(args):
    return Config(
        unicode_snob=default_config.unicode_snob,
        escape_snob=default_config.escape_snob,
        ignore_links=args.ignore_links,
        ignore_images=args.ignore_images,
        google_doc=args.google_doc,
        dash_unordered_list=args.dash_unordered_list,
        body_width=args.body_width or default_config.body_width,
        google_list_indent=args.google_list_indent or default_config.google_list_indent,
        hide_strikethrough=args.hide_strikethrough
    )

def main():
    args = parse_args()
    config = config_from_args(args)
    html_data = sys.stdin.read()
    converter = HTML2Text()
    textmod = converter.handle(html_data)
    print(textmod)

if __name__ == "__main__":
    main()

