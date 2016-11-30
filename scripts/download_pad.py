'''
Created on 19.07.2012

@author: tobixx0
'''
import os
import logging as logg
import argparse

from piratetools42.pad import PadTeam


logg.basicConfig(level=logg.DEBUG)


if __name__ == '__main__':
    ps = argparse.ArgumentParser("download_pad")
    ps.add_argument("--pad", help="pad name")
    ps.add_argument("--team", help="pad team to use")
    ps.add_argument("--outformat", default="wiki", help="output format, wiki or markdown")
    ps.add_argument("--out", "-o", default="-", help="output file, - for stdout")
    ps.add_argument("--login", help="login mail address")
    ps.add_argument("--password", help="login password, ask if not given")
    args = ps.parse_args()
    padteam = PadTeam(args.team)

    if args.login:
        if args.password:
            padteam.login(args.login, args.password)
        else:
            padteam.secret_login(args.login)

    lines = padteam.gen_pad_lines(args.pad, args.outformat)

    if args.out == "-":
        for line in lines:
            print(line)
    else:
        with open(args.out, "w") as wf:
            wf.writelines(l + "\n" for l in lines)
