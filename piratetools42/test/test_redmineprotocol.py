import piratetools42.redmineprotocol as rp

def test_protocol_from_issue():
    antraege = [
      {
          "id": 42,
          "title": "Testantrag",
          "description": "Test",
          "Antragsteller": "Hans Wurst",
          "created_at": "20.3.2066",
      }
    ]
    issue = {
      "title": "Sitzung des Testvorstands Hinteröd 25.3.2066",
      "Adresse": "Langweilstraße 23, 91666 Hinteröd",
      "Ort": "Hinteröder Wirtshaus",
      "due_date": "25.3.2066",
      "Startzeit": "14:00",
      "vorstaende": ["Hans Wurst", "Depp vom Dienst"],
      "antraege": antraege
}
    generated = rp.protocol_from_issue(issue)
    print(generated)


if __name__ == "__main__":
    test_protocol_from_issue()
