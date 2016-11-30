import sys
import re
import logging as logg
import argparse


# dir where images and other static stuff are stored

# regexes
MEDIAWIKI_HYPERLINK = re.compile("\[((?:http|ftp)[s]?://[^ ]+) (.+)\]")
SECTION_OR_FRAME_HEADER = re.compile("={2,4}[^=]+={2,4}")
GRAPHIC_URL = re.compile("<<<\[((?:http|ftp)[s]?://[^ ]+) (?:.+)\],?(.*)>>>")

SPECIAL_TRANS_TABLE = {
"&nbsp;": "",
"&lt;": "<",
"&gt;": ">",
re.compile("<s>\s*"): "~~",
re.compile("\s*</s>"): "~~"
}

SPECIAL_TRANS_TABLE_LINKS = {
"_": "\_"
}


def replace_special_chars(line):
    for orig, replacement in SPECIAL_TRANS_TABLE.items():
        if isinstance(orig, str):
            line = line.replace(orig, replacement)
        else:
            line = orig.sub(replacement, line)
    return line


def replace_special_chars_links(text):
    for orig, replacement in SPECIAL_TRANS_TABLE_LINKS.items():
        text = text.replace(orig, replacement)
    return text


def convert_mediawiki_link_to_markdown(match_obj):
    link = replace_special_chars_links(match_obj.group(1))
    linktext = replace_special_chars_links(match_obj.group(2))
    if not linktext:
        linktext = link

    return "[{}]({})".format(linktext, link)


def replace_links(line):
    return MEDIAWIKI_HYPERLINK.subn(convert_mediawiki_link_to_markdown, line)[0]


def detect_indentation(symbol, line):
    level = 0
    pos = 1
    for c in line[1:]:
        if c == "*":
            level += 1
        elif c == " ":
            pass
        else:
            break
        pos += 1
    return level, pos


def fix_enumeration(line):
    sym = None
    if line.startswith("*"):
        sym = "*"
    if sym:
        level, pos = detect_indentation(sym, line)
    else:
        return line

    if sym == "*":
        prefix = " " * level * 4 + "* "

    return prefix + line[pos:]


def fix_bold_headings(line):
    if SECTION_OR_FRAME_HEADER.search(line) is not None:
        return line.replace("'''", "")
    else:
        return line


def expand_newline(line):
    return [l + "\n" for l in line.split("\n")]


def gen_converted_lines(raw_lines):
    # run all conversion / cleanup functions for each line
    for line in raw_lines:
        yield replace_links(replace_special_chars(fix_enumeration(line.strip())))
