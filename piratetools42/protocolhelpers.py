#coding: utf8

from itertools import cycle, chain, tee, dropwhile, imap
import getpass
import logging
import re
import sys
import locale
from datetime import *
from dateutil.parser import *
from dateutil.rrule import *
from dateutil.relativedelta import *
from jinja2 import Template, Environment
import mwclient

from piratetools42.padhelpers import download_pad 

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())
logg = logging.getLogger(__name__)

OFFLINE_SESSION_TYPE = "Offline"
ONLINE_SESSION_TYPE = "Online(XMPP)"


##### jinja2 stuff

### custom filters

def de_dateformat(datelike_obj):
    return datelike_obj.strftime("%d.%m.%Y")


def reverse_date_format(datelike_obj):
    return datelike_obj.strftime("%Y-%m-%d")


ENV = Environment()
ENV.filters["de_dateformat"] = de_dateformat
ENV.filters["reverse_date_format"] = reverse_date_format


class SessionType(object):
    def __init__(self, wiki_protocol_uri, wiki_protocol_template, pad_name, pad_team, rrule_settings, **additional):
        self.wiki_protocol_uri = wiki_protocol_uri
        self.pad_name = pad_name
        self.pad_team = pad_team
        self.wiki_protocol_template = wiki_protocol_template
        self.rrule_settings = rrule_settings
        self.additional = additional


def make_session_types():
    weiden_protocol_template = ENV.from_string(
        "| {{date|de_dateformat}} || - || <!-- [[ {{url}} |hier ]] --> || -")
    wenterhaken_protocol_template = ENV.from_string(
        "| {{date|de_dateformat}} || {{session_type}} || - || <!-- [[ {{url}} |hier ]] --> || -")
    wenterhaken_url = "BY:Crew/WENterhaken/Protokolle/{date}"

    return {
        "wenterhaken_offline": SessionType(
            wenterhaken_url, 
            wenterhaken_protocol_template, 
            "WENterhakenProtokoll", 
            "weiden-neustadt",
            [
                dict(freq=MONTHLY, bymonthday=10, byhour=18, byminute=30)
            ],
            session_type="Offline"),

        "wenterhaken_online": SessionType(
            wenterhaken_url,
            wenterhaken_protocol_template,
            "OnlineSitzungWENterhaken",
            "weiden-neustadt",
            [
                dict(freq=DAILY, byweekday=WE, byhour=19, byminute=30),
                dict(freq=DAILY, byweekday=SU, byhour=19, byminute=30)
            ], 
            session_type="Online(XMPP)"),

        "stammtisch_weiden": SessionType(
            "BY:Weiden/Protokolle/{date}", 
            weiden_protocol_template,
            "ProtokollStammtisch",
            "weiden-neustadt",
            [
                dict(freq=MONTHLY, byweekday=TU, byhour=19, byminute=0, bysetpos=1), 
                dict(freq=MONTHLY, bymonthday=25, byhour=19, byminute=0)
            ]),

        "oberpfalz_vorstand": SessionType(
            "BY:Bezirksverband_Oberpfalz/Vorstandssitzung/{date}_-_Protokoll_Vorstandssitzung_Bezirksverband_Oberpfalz", 
            weiden_protocol_template,
            "Vorstandssitzung-{}",
            "oberpfalz",
            [
                dict(freq=DAILY, byweekday=MO, byhour=20, byminute=15), 
            ])
    }


SESSION_TYPES = make_session_types()


def interleave_rrules(*rrules):
    active = len(rrules)
    sorted_it = (iter(r) for r in sorted(rrules, key=lambda r: (r.count() and r[0]) or datetime.now()))
    cycle_it = cycle(sorted_it)
    while active > 0:
        try:
            current_elem = next(next(cycle_it))
        except StopIteration:
            active -= 1
        else:
            yield current_elem


def generate_wenterhaken_protocol_entries(start_dt=None):
    """Generiert Einträge fürs Protokoll bis zur nächsten Offline-Crewsitzung"""
    if start_dt is None:
        start_dt = date.today()
    start_dt += relativedelta(hour=18, minute=30)
    offline_dt = start_dt + relativedelta(day=10)
    offline_dt = offline_dt if offline_dt > start_dt else offline_dt + relativedelta(months=1)

    session_online = SESSION_TYPES["wenterhaken_online"]
    session_offline = SESSION_TYPES["wenterhaken_offline"]

    # 2 Iteratoren erstellen die richtig sortiert über alle Termine für alle Wiederholungsregeln (rrules) laufen
    online_session_rrules, online_session_rrules_2 = tee(interleave_rrules(*[
        rrule(dtstart=start_dt, until=offline_dt, **s) for s in session_online.rrule_settings]))

    logg.debug("\n" + "-"*80)
    logg.debug("Nächste Online-Crewsitzungen\n%s", 
                "\n".join(d.strftime("%c") for d in online_session_rrules_2))
    logg.debug("Nächste Offline-Crewsitzung am \n%s", offline_dt.strftime("%c"))

    print("\nfürs Wiki:\n")

    # Eintrag für Offline-Sitzung erzeugen
    print("|-")
    print(session_offline.wiki_protocol_template.render(
        date=offline_dt, 
        session_type=session_offline.additional["session_type"], 
        url=session_offline.wiki_protocol_uri.format(date=reverse_date_format(offline_dt))))

    # Einträge für Online-Sitzungen erzeugen
    for dt in reversed(list(online_session_rrules)):
        print("|-")
        print(session_online.wiki_protocol_template.render(
            date=dt, 
            session_type=session_online.additional["session_type"], 
            url=session_online.wiki_protocol_uri.format(date=reverse_date_format(dt))))


def generate_stammtisch_protocol_entries(start_dt=None, end_dt=None):
    """Generiert Einträge fürs Stammtisch-Protokoll"""
    if start_dt is None:
        start_dt = date.today()
    if end_dt is None:
        end_dt = start_dt + relativedelta(months=+3)

    session = SESSION_TYPES["stammtisch_weiden"]
    # 2 Iteratoren erstellen die richtig sortiert über alle Termine für alle Wiederholungsregeln (rrules) laufen
    session_rrules, session_rrules_2 = tee(interleave_rrules(*[
        rrule(dtstart=start_dt, until=end_dt, **s) for s in session.rrule_settings]))

    logg.debug("\n" + "-"*80)
    logg.debug("Nächste Stammtischtermine:\n%s", 
                "\n".join(d.strftime("%c") for d in session_rrules_2))

    print("\nfürs Wiki:\n")

    for dt in reversed(list(session_rrules)):
        print("|-")
        print(session.wiki_protocol_template.render(date=dt, url=session.wiki_protocol_uri.format(date=reverse_date_format(dt))))


def move_protocol_to_wiki(session, pad_name_addon=None):
    if pad_name_addon:
        pad_name = session.pad_name.format(pad_name_addon)
    else:
        pad_name = session.pad_name
    pad_lines = download_pad(session.pad_team, pad_name)
    logg.debug("downloaded pad for %s", pad_name)
    #vorspann wegwerfen
    pad_it = dropwhile(lambda s: "= Protokoll ab hier =" not in s, pad_lines)
    next(pad_it)
    # leere Zeilen wegwerfen
    pad_it = dropwhile(lambda s: not s.strip(), pad_it)
    header = next(pad_it)
    match = re.search(r"(\d+)\.(\d+)\.(\d\d+)", header)
    if not match:
        raise Exception("Mit dem Protokoll-Anfang stimmt was nicht, Datum konnte nicht erkannt werden: {}".format(header))
    day, month, year = [int(e) for e in match.groups()]
    if year < 100:
        year += 2000 
    session_date = date(year=year, month=month, day=day)
    reversed_date = reverse_date_format(session_date)
    unquote_func = lambda s: s.replace("&gt;", ">").replace("&lt;", "<") 
    edit_uri = "http://wiki.piratenpartei.de/wiki//index.php?title={}&action=edit"
    logg.debug("Header ist:\n%s, Protokoll-Datum %s", header, reversed_date)
    print("Inhalt:")
    print("-" * 80)
    print(header + "".join(imap(unquote_func, pad_it)))
    print("-" * 80)
    print("Seiten-URI fürs Protokoll:")
    print(edit_uri.format(session.wiki_protocol_uri.format(date=reversed_date)))
    # geht nicht wegen API restriction (solche Deppen...)
    #page_uri = "{}/Protokolle/{}".format(session.wiki_protocol_uri, reversed_date)
    #w = mwclient.Site("wiki.piratenpartei.de", "/wiki/")
    #user = raw_input("Wiki-Username: ")
    #user = "escaP"
    #pas = getpass.getpass()
    #w.login(user, pas)
    #page = w.Pages[page_uri]
    #logg.info("page %s exists? %s", page_uri, page.exists)
    #text = page.edit()
    #page.save(pad_it, summary="tools test")