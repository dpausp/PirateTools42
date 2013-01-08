'''
Created on 19.07.2012

@author: tobixx0
'''
import os
import logging as logg
import argparse


logg.basicConfig(level=logg.DEBUG)


if __name__ == '__main__':
    ps = argparse.ArgumentParser("pad2beamer")
    ps.add_argument("--pad")
    ps.add_argument("--team")
    args = ps.parse_args()
    download_pad(args.team, args.pad)
