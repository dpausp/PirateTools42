#/usr/bin/python3
#coding: utf8

"""
Read JSON antrag files ("Antragsbücher") from pirat.ly/spicker and write content to the wikiarguments DB 
STATUS: works, some antraege need custom fixes for strange unicode chars (see BAD_ANTRAEGE_FIXES below)
"""

import difflib
import json
import sys
import re
import time
from pprint import pformat

import piratetools42.logconfig
logg = piratetools42.logconfig.configure_logging("wikiarguments-spickerrr-import.log")
from piratetools42.wikiargumentsdb import create_additional_data, session, Question, Tag

sys.path.append("../../")

# config

WIKI_BASE_URI = "http://wiki.piratenpartei.de/"


HTML_ANTRAGS_TMPL = """\
<h2>Wiki</h2>
<a href="{info_url}">{info_url}</a>
<h2>Pirate Feedback</h2>
<a href="{lqfb_url}">{lqfb_url}</a>
<h2>Antragsteller</h2>
{owner}
<h2>Antragstext</h2>
{text}
<h2>Begründung</h2>
{motivation}
<h2>Letzte Änderung</h2>
{changed}
"""

CODE_RE = re.compile("(\w+)(\d\d\d)")

# we have to apply fixes for some 'antraege' when inserting into the DB
BAD_ANTRAEGE_FIXES = {
"PP047": lambda s: s.replace("\u2191", "^"), 
"PP092": lambda s: s.replace("\u2029", " ")}

# special codes for the LPT. Map BPT codes to LPT codes.
CODE_TRANSLATION = {
"X": "SA",
"P": "PP"}


def translate_antrags_code(antrag):
    code, number = CODE_RE.match(antrag["id"]).groups()
    translated = CODE_TRANSLATION.get(code, code)
    antrag["id"] = translated + number   
    return antrag


def antrag_details_prepare_html(antrag):
    antrag["text"] = antrag["text"].rstrip("</p> </div> <p><br /> </p>")
    antrag.setdefault("lqfb_url", "-")
    antrag.setdefault("motivation", "-")
    antrag.setdefault("owner", "-")
    html = HTML_ANTRAGS_TMPL.format(**antrag)
    fix = BAD_ANTRAEGE_FIXES.get(antrag["id"])
    if fix:
        html = fix(html)
    return html


def insert_antrag(antrag_json):
    js = antrag_json
    details = antrag_details_prepare_html(js)
    id_ = js["id"]
    tags = [id_, "LPT13.1", js["kind"]]
    additional = create_additional_data(tags)
    title = id_ + ":" + js["title"]
    if len(title) > 100:
        # shorten title because wikiarguments supports only 100 chars
        # add full title to details
        details = "<h2>Voller Titel</h2><br />{}<br />{}".format(title, details)
        title = title[:97] + "..."
    question = Question(title=title, url=id_, details=details, dateAdded=time.time(), 
                        score=0, scoreTrending=0, scoreTop=0, userId=2, additionalData=additional)
    session.add(question)
    session.commit()
    # insert title words in Tag table because this table is used for question searches
    title_words = js["title"].split()
    for tag in tags + title_words:
        tag_obj = Tag(tag=tag, questionId=question.questionId)
        session.add(tag_obj)
    session.commit()
    return question


def update_antrag(antrag):
    id_ = antrag["id"]
    question = session.query(Question).filter_by(url=id_).first()
    if question:
        logg.info("Antrag %s existiert schon", id_)
        # update details if changed. Other fields must not change and are ignored
        details = antrag_details_prepare_html(antrag)
        if question.details != details:
            diff = list(difflib.Differ().compare(question.details.split("\n"), details.split("\n")))
            logg.info("Antragsdetails von %s haben sich verändert, Unterschiede:\n %s", id_, pformat(diff))
            question.details = details
            session.commit()
            return diff
    else:
        logg.info("Antrag ist neu: '%s'", id_)
        insert_antrag(antrag)
        return "Neuer Antrag"


def update_antragsbuch(filename):
    logg.info("---- Antragsbuch-Update gestartet ----")
    updated = {}
    failed = {}
    with open(filename) as f:
        antragsbuch = json.load(f)
    for antrag in antragsbuch:
        try:
            diff = update_antrag(translate_antrags_code(antrag))
        except Exception as e:
            logg.error("error inserting antrag '%s', error '%s'", antrag["id"], e)
            failed[antrag["id"]] = e
            session.rollback()
        if diff:
            updated[antrag["id"]] = diff
            
    logg.info("---- Antragsbuch-Update beendet ----")
    if updated:
        logg.info("Geänderte Anträge:\n%s", pformat(updated))
    if failed:
        logg.warn("Es traten Fehler auf:\n%s", pformat(failed))
    return updated, failed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("kein Dateiname angegeben!")
    do_it = input("Update durchführen? (j/n) ")
    if do_it.lower() == "j":
        update_antragsbuch(sys.argv[1])