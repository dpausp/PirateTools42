#!/usr/bin/env python
'''
Created on 19.07.2012

@author: tobixx0
'''

import sys
import re
import logging as logg
import argparse
import hashlib
import os.path
import urllib.parse
import requests
from itertools import dropwhile

sys.path.append("/usr/lib/python2.7/site-packages/wiki2beamer")

import wiki2beamer

from piratetools42.padhelpers import download_pad

logg.basicConfig(level=logg.DEBUG)

# dir where images and other static stuff are stored
STATIC_DIR = "_static"

# regexes
MEDIAWIKI_HYPERLINK = re.compile("\[((?:http|ftp)[s]?://[^ ]+) (.+)\]")
SECTION_OR_FRAME_HEADER = re.compile("={2,4}[^=]+={2,4}")
GRAPHIC_URL = re.compile("<<<\[((?:http|ftp)[s]?://[^ ]+) (?:.+)\],?(.*)>>>")

SPECIAL_TRANS_TABLE = {
"&nbsp;": "",
"%": "\\%",
"&lt;": "<",
"&gt;": ">",
"\"": '\\dq{}'
}

SPECIAL_TRANS_TABLE_LINKS = {
"#": "\\#",
"_": "\\_",
"%": "\\%",
"$": "\\$",
"}": "\\}",
"{": "\\{",
"&": "\\&",
#"\\": "$\\backslash$"
}


def add_space_after_symbols(symbol, string):
    stripped = string.lstrip(symbol)
    num_symbols = len(string) - len(stripped)
    return symbol * num_symbols + " " + stripped


def replace_special_chars(line):
    for orig, replacement in SPECIAL_TRANS_TABLE.items():
        line = line.replace(orig, replacement)
    return line


def replace_special_chars_links(text):
    for orig, replacement in SPECIAL_TRANS_TABLE_LINKS.items():
        text = text.replace(orig, replacement)
    return text


def convert_mediawiki_link_to_latex(match_obj):
    link = replace_special_chars_links(match_obj.group(1))
    linktext = replace_special_chars_links(match_obj.group(2))
    if not linktext:
        linktext = link

    link_color = "cyan"
    colored_linktext = "\\textcolor{{{0}}}{{{1}}}".format(link_color, linktext)
    return "\\href{{{0}}}{{{1}}}".format(link, colored_linktext)


def replace_links(line):
    return MEDIAWIKI_HYPERLINK.subn(convert_mediawiki_link_to_latex, line)[0]


def correct_enumeration(line):
    if line.startswith("*"):
        return add_space_after_symbols("*", line)
    elif line.startswith("#"):
        return add_space_after_symbols("#", line)
    else:
        return line


def correct_bold_headings(line):
    if SECTION_OR_FRAME_HEADER.search(line) is not None:
        return line.replace("'''", "")
    else:
        return line


def handle_graphics(line):
    m = GRAPHIC_URL.match(line)
    if m is not None:
        # download image if not already present
        img_uri = m.group(1)
        image_name = hashlib.sha512(img_uri).hexdigest() + ".jpg"
        image_path = os.path.join(STATIC_DIR, image_name)
        if not os.path.exists(image_path):
            logg.info("downloading image from {}".format(img_uri))
            # unquote the string in case it is quoted...
            # HACK: needed?
            r = requests.get(urllib.parse.unquote(img_uri))
            if r.status_code == 200:
                pass
            with open(image_path, "wb") as wf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk: # filter out keep-alive new chunks
                        wf.write(chunk)
        graphic_options = m.group(2)
        graphics_base = "<<<{0},{1}>>>"
        return graphics_base.format(image_path, graphic_options)
    else:
        return line


def expand_newline(line):
    return [l + "\n" for l in line.split("\n") if l.strip()]


def correct_wikilines(raw_lines):
    lines = []
    # run all "cleanup" functions for each line
    for line in raw_lines:
        line_corrected = replace_links(handle_graphics(correct_bold_headings(replace_special_chars(correct_enumeration(line.strip())))))
        lines.extend(expand_newline(line_corrected))

    return lines


def runpad2beamer(argv):
    ps = argparse.ArgumentParser("pad2beamer")
    ps.add_argument("--pad")
    ps.add_argument("--team")
    ps.add_argument("--file")
    ps.add_argument("--out")
    ps.add_argument("--outpdf")
    args = ps.parse_args()

    if args.pad:
        #get pad content with wiki markup
        raw_lines = download_pad(args.team, args.pad)
    else:
        with open(args.file) as wikifile:
            raw_lines = wikifile.readlines()

    pad_it = dropwhile(lambda s: "= Präsentation ab hier =" not in s, raw_lines)
    next(pad_it)
    # leere Zeilen wegwerfen
    pad_it = dropwhile(lambda s: not s.strip(), pad_it)
    lines = correct_wikilines(pad_it)
    logg.debug("showing input for convert2beamer\n" + "-" * 80)
    for line in lines:
        logg.debug(line)

    # do it
    logg.debug("running wiki2beamer...")
    result = wiki2beamer.convert2beamer(lines)

    # write resulting latex code to file or stdout
    if args.out:
        with open(args.out, "w") as w_file:
            w_file.writelines(result)

    # make complete latex file and run latex
    elif args.outpdf:
        pass


    else:
        logg.info("showing result latex code\n" + "-" * 80)
        for line in result[1:]:
            print(line)
        logg.info("finished")

if __name__ == '__main__':
    runpad2beamer(sys.argv)
