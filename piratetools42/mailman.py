import csv
import getpass
from urllib.parse import unquote
from collections import namedtuple
from bs4 import BeautifulSoup
from sessionurl import SessionUrl


MLMember = namedtuple('MLMember', ['email', 'hide', 'realname', 'ack', 'notmetoo', 'plain', 'digest', 'nodupes', 'nomail', 'mod'])


def get_input_value(input_element):
    typ = input_element["type"]
    val = input_element["value"]
    if typ == "CHECKBOX":
        return True if val == "on" else False
    elif typ == "TEXT":
        return val


def get_member_attrs_from_field(username_field):
    quoted_email = username_field["value"]
    user_inputs = username_field.parent.parent.find_all("input")
    member_attrs = { e["name"].rsplit("_", 1)[1]: get_input_value(e) for e in user_inputs if e["type"] != "HIDDEN" }
    del member_attrs["unsub"]
    member_attrs["email"] = unquote(quoted_email)
    return member_attrs
    

def get_username_fields_from_page(page_content):
    sp = BeautifulSoup(page_content)
    username_fields = sp.find_all("input", type="HIDDEN", attrs=dict(name="user"))
    return username_fields


class MailmanClient(SessionUrl):
    
    def login(self, password):
        data = {
            "adminpw": password,
            "admlogin": u"Sesam, öffne dich..."
        }
        return self.post("/", data=data)
    
    def secret_login(self):
        return self.login(getpass.getpass())

    def logout(self):
        return self.get("logout")
    
    def remove_members(self, usernames):
        data = {
            "send_unsub_notifications_to_list_owner": 0,
            "send_unsub_ack_to_this_batch": 1,
            "setmemberopts_btn": u"Änderungen speichern",
            "unsubscribees": u"\n".join(usernames)
        }
        return self.post("members/remove", data=data)
        
    def add_members(self, usernames):
        data = {
            "subscribe_or_invite": 0,
            "send_welcome_msg_to_this_batch": 1,
            "send_notifications_to_list_owner": 0,
            "setmemberopts_btn": u"Änderungen speichern",
            "subscribees": u"\n".join(usernames)
        }
        return self.post("members/add", data=data)    
    
    @property
    def members(self):
        members_page = self.get("members")
        username_fields = get_username_fields_from_page(members_page.content)
        return (MLMember(**get_member_attrs_from_field(f)) for f in username_fields)
    
    @property
    def subscribed_addresses(self):
        members_page = self.get("members")
        username_fields = get_username_fields_from_page(members_page.content)
        return (unquote(f["value"]) for f in username_fields)


def write_members_csv(filepath, members, csv_options={}):
    with open(filepath, "w") as wf:
        writer = csv.writer(wf, **csv_options)
        writer.writerow(MLMember._fields)
        for m in members:
            writer.writerow(m)

