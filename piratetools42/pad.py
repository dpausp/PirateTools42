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
from piratetools42.sessionurl import SessionUrl
import piratetools42.markdownpad as mdp


logg = logging.getLogger(__name__)

DOWNLOAD_URI = "/ep/pad/export/{}/latest?format={}"

IMPORT_TOKEN_RE = re.compile("'importSuccessful', '(\w{32})'")


class PadTeam(SessionUrl):

    def __init__(self, team, server="piratenpad.de", scheme="https", **default_kwargs):
        self.team = team
        url = "{}://{}.{}".format(scheme, team, server)
        super(PadTeam, self).__init__(url, **default_kwargs)
        self.new_session()


    def login(self, email, password):
        data = {"email": email, 
                "password": password}
        # etherpad does a strange redirect to set a cookie on the first request. 
        # We just have to do it twice to make it workk...
        res = self.post("/ep/account/sign-in", data=data)
        return self.post("/ep/account/sign-in", data=data)

    
    def secret_login(self, email):
        return self.login(email, getpass.getpass())


    def export_pad(self, pad_id, exportformat="wiki"):
        export_url = DOWNLOAD_URI.format(pad_id, exportformat)
        logg.info("getting pad %s, format %s", pad_id, exportformat)
        res = self.get(export_url)
        return res.text


    def gen_pad_lines(self, pad_id, output_format="wiki"):
        if output_format in ("markdown", "md"):
            text = self.export_pad(pad_id, "wiki")
            wiki_lines = text.split("\n")
            return mdp.gen_converted_lines(wiki_lines)
            
        else:
            text = self.export_pad(pad_id, output_format)
            lines = text.split("\n")
            return iter(lines)


    def create_pad(self, pad_id):
        data = {"padId": pad_id, 
                "button": "New pad"}
        return self.post("/ep/pad/create", data=data)


    def replace_pad_text(self, pad_id, text):
        data = {"padId": pad_id}
        tmp = tempfile.NamedTemporaryFile(suffix=".txt")
        tmp.write(text)
        tmp.seek(0)
        files = dict(file=tmp)
        res = self.post("/ep/pad/impexp/import", data=data, files=files)
        
        data = {"padId": "einTest",
                "token": IMPORT_TOKEN_RE.search(res.content).groups()[0]}

        return self.post("/ep/pad/impexp/import2", data=data)

