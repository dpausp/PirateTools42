'''
Created on 19.07.2012

@author: tobixx0
'''
import os
import logging
import cookielib
import urllib2

logg = logging.getLogger(__name__)

COOKIEFILE = "cookies-pad.lwp"

cj = cookielib.LWPCookieJar()
if os.path.isfile(COOKIEFILE):
    cj.load(COOKIEFILE)

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)


def download_pad(team, pad):
    #get pad content with wiki markup
    base_uri = "https://{team}.piratenpad.de/ep/pad/export/{pad}/latest?format=wiki"
    uri = base_uri.format(**locals())
    logg.info("getting pad from %s", uri)
    url = urllib2.urlopen(uri)
    lines = url.readlines()
    logg.info("showing raw input from pad with %s lines\n%s", len(lines), "-" * 80)
    for line in lines:
        logg.debug(line)
    return lines
