# -*- coding: utf-8 -*-
from piratetools42.padhelpers import PadTeam
from pytest import fixture

PAD_PW = "kfKj6TIKs"

@fixture
def pad_team():
    team = PadTeam("oberpfalz")
    team.login("tobias.stenzel@piraten-oberpfalz.de", PAD_PW)
    return team


def test_export_pad_markdown(pad_team):
    content = pad_team.export_pad("VorstandssitzungVorlage", "markdown")
    assert content
    assert "{start_time}" in content
    assert "##" in content


def test_export_pad_html(pad_team):
    content = pad_team.export_pad("VorstandssitzungVorlage", "html")
    assert content
    assert "{start_time}" in content
    assert "</html>" in content
    
    
content = """
<html>
<li>a</li>
<li>b</li>
<li>c</li>
</html>
"""
    

def test_replace_pad_html(pad_team):
    content = pad_team.export_pad("VorstandssitzungVorlage", "html")
    pad_team.replace_pad_content("Protokolltest2", content, "html")
    new_content = pad_team.export_pad("VorstandssitzungVorlage", "html")
#     assert "<li>" in new_content