'''
Created on 19.07.2012

@author: tobixx0
'''
import getpass
import logging
import os
import re
import tempfile
import urllib
import requests
from urllib.parse import urljoin
from pyquery import PyQuery as Pq
import piratetools42.markdownpad as mdp
from piratetools42.sessionurl import SessionUrl


logg = logging.getLogger(__name__)

DOWNLOAD_URI = "/ep/pad/export/{}/latest?format={}"

IMPORT_TOKEN_RE = re.compile("'importSuccessful', '(\w{32})'")


def fix_pad_html_export(html):
    from lxml.html import tostring, fromstring
    etree = fromstring(html)
    list_elements = etree.cssselect("li")
    for li in list_elements:
        print("li before:", tostring(li))
        removed_break = None
        children = li.getchildren()
        for child in children:
            if child.tag == "br":
                li.remove(child)
                removed_break = child
        if removed_break is not None:
            parent = li.getparent()
            idx = parent.index(li) + 1
            parent.insert(idx, removed_break)

            print("li after:", tostring(li))
            print("parent after:", tostring(parent))

    html = tostring(etree, encoding="unicode")
    return html


class PadTeam(SessionUrl):

    def __init__(self, team, server="piratenpad.de", scheme="https", **default_kwargs):
        self.team = team
        if "url" in default_kwargs:
            url = default_kwargs["url"]
            del default_kwargs["url"]
        else:
            url = "{}://{}.{}/".format(scheme, team, server)

        super(PadTeam, self).__init__(url, **default_kwargs)
        self.new_session()

    def login(self, email, password):
        params = {"cont": self.url}
        data = {"email": email,
                "password": password}
        # XXX: strange, we have to login twice to get the desired logged in state...
        # curl has the same problem, has to do with cookies
        self.post("/ep/account/sign-in", params=params, data=data)
        return self.post("/ep/account/sign-in", params=params, data=data)

    def secret_login(self, email):
        return self.login(getpass.getpass())

    def export_pad(self, pad_id, output_format="wiki", use_plain_links=False):
        if output_format in ("markdown", "md"):
            text = self.export_pad(pad_id, "wiki")
            wiki_lines = text.split("\n")
            return "\n".join(mdp.gen_converted_lines(wiki_lines, use_plain_links))
        else:
            export_url = DOWNLOAD_URI.format(pad_id, output_format)
            logg.info("getting pad %s, format %s", pad_id, output_format)
            res = self.get(export_url)
            text = res.text

        if output_format == "html":
            text = fix_pad_html_export(text)

        return text

    def gen_pad_lines(self, pad_id, output_format="wiki", use_plain_links=False):
        if output_format in ("markdown", "md"):
            text = self.export_pad(pad_id, "wiki")
            wiki_lines = text.split("\n")
            return mdp.gen_converted_lines(wiki_lines, use_plain_links)
        else:
            text = self.export_pad(pad_id, output_format, use_plain_links)
            lines = text.split("\n")
            return iter(lines)

    def create_pad(self, pad_id):
        data = {"padId": pad_id,
                "button": "New pad"}
        return self.post("/ep/pad/create", data=data)

    def replace_pad_content(self, pad_id, text, input_format="txt"):
        data = {"padId": pad_id}
        tmp = tempfile.NamedTemporaryFile(mode="r+", encoding="utf8", suffix="." + input_format)
        tmp.write(text)
        tmp.seek(0)
        files = dict(file=tmp)
        res = self.post("/ep/pad/impexp/import", data=data, files=files)

        data = {"padId": pad_id,
                "token": IMPORT_TOKEN_RE.search(res.text).groups()[0]}

        return self.post("/ep/pad/impexp/import2", data=data)

    @property
    def pad_names(self):
        res = self.get("/ep/padlist/all-pads")
        pq = Pq(res.content)
        pad_link_elements = pq(".title.first").children("a")
        pad_names = [p.attrib["href"][1:] for p in pad_link_elements]
        return pad_names

    def get_pad_link(self, pad_name):
        return urljoin(self.url, pad_name)
