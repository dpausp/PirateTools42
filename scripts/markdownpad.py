#!/usr/bin/env python3

import sys
sys.path.append(".")
import logging as logg
import argparse

import pypandoc
from piratetools42.pad import PadTeam
import piratetools42.markdownpad as mdp

logg.basicConfig(level=logg.INFO)


def markdownpad(argv):
    ps = argparse.ArgumentParser("markdownpad")
    ps.add_argument("--pad")
    ps.add_argument("--team")
    ps.add_argument("--file")
    ps.add_argument("--out")
    ps.add_argument("--outpdf")
    ps.add_argument("--pandoc", action="store_true")
    args = ps.parse_args()

    if args.pad:
        padteam = PadTeam(args.team)
        #get pad content with wiki markup
        lines_gen = padteam.gen_pad_lines(args.pad, "markdown")
    elif args.file:
        with open(args.file) as wikifile:
            raw_lines = wikifile.readlines()

        lines_gen = mdp.gen_converted_lines(raw_lines)
    else:
        raise Exception("no argument given, use --pad and --team or --file")

    if args.out:
        with open(args.out, "w") as w_file:
            w_file.writelines(l + "\n" for l in lines_gen)
            logg.info("markdown output written to %s", args.out)

    # make complete latex file and run latex
    elif args.outpdf:
        pass

    else:
        logg.info("showing markdown output\n" + "-" * 80)
        text = "\n".join(lines_gen)
        if args.pandoc:
            text = pypandoc.convert_text(text, "markdown", "markdown")
        print(text)


if __name__ == '__main__':
    markdownpad(sys.argv)
