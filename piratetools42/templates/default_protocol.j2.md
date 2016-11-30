# Protokoll {{ title }}

Ort, Datum und Zeit
-------------------
* Ort: {{ Ort }}
* Datum: {{ due_date }}
* Zeit: {{ Startzeit }}

Anwesende
---------

### Vorstände
{%- for v in vorstaende %}
* {{ v }}
{%- endfor %}

### Beauftragte
*

### Gäste
*

# Tagesordnung


Aktivitäten Vorstände
---------------------

{%- for v in vorstaende %}
### v
*
{%- endfor %}

Aktivitäten der Beauftragten und der Kreise
-------------------------------------------

Aktuelle Kennzahlen
-------------------
<!-- Finanzen, Mitgliederzahlen, usw.) -->

* Kontostand:
  * davon frei verfügbar:
* Barkasse:


$Titel des 1. Tagesordnungspunkts
---------------------------------


$Titel des 2. Tagesordnungspunkts
---------------------------------


Anträge
-------

{%- for a in antraege %}

### #{{ a.id }}: {{ a.title }}

* Antragssteller: {{ a.Antragsteller }}
* Eingegangen am: {{ a.created_at }}

{{ a.description }}

{%- endfor %}

Umlaufbeschlüsse
----------------

{%- for u in umlaufbechluesse %}
* [{{ u.title }}](https://redmine.piratenpartei-bayern.de/issues/{{ u.id }})
{%- endfor %}


Sonstiges
---------
 
 
Nächstes Treffen
----------------

* Nächste Vorstandssitzung in 2 Wochen
* Ort: Mumble-Raum Oberpfalz->Vorstandssitzung
* Datum: ..14
* Zeit: 20:00
