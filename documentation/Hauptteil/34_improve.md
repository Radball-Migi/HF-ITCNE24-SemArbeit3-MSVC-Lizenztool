---
layout: default
title: 3.4 Verbessern
parent: 3. Hauptteil
nav_order: 7
---
#  Verbessern (Improve) Phase

Die Improve-Phase ist der vierte Schritt in einem Six Sigma Projekt. In dieser Phase werden die in der [Analyze-Phase](./33_analysieren.md) identifizierten Hauptursachen für Prozessabweichungen adressiert und Lösungen entwickelt, um diese zu beheben. Ziel ist es, durch gezielte Verbesserungsmassnahmen die Prozessleistung zu optimieren und die identifizierten Probleme nachhaltig zu lösen. Dies umfasst die Anwendung von Kreativitätstechniken, statistischen Methoden und Pilotprojekten, um die Wirksamkeit der vorgeschlagenen Lösungen zu testen und zu validieren.

![Verbessern](../../ressources/images/verbessern.png)

[Quelle](../Quellverzeichnis/index.md#improve-phase)

## Was ist MSVC?
MSVC, oder Microservices, ist ein Architekturstil für die Entwicklung von Anwendungen, bei dem eine Anwendung in eine Sammlung von kleinen, unabhängigen, und lose gekoppelten Diensten aufgeteilt wird. Jeder dieser Dienste, oder Microservices, hat seine eigene Codebasis und kann unabhängig voneinander entwickelt, bereitgestellt und skaliert werden.

### Was ist Flask API? 
Flask API ist ein leichtgewichtiges REST-Framework auf Basis von Python, das zur Implementierung von stateless Webservices genutzt wird. Es unterstützt HTTP-Methoden, JSON-Serialisierung und Middleware-Integration. Als Microservice fungiert es als Endpoint zur Datenverarbeitung oder Systemintegration.


## Umsetzung (Improve)

Wie in den vorherigen Schritten beschrieben, möchte ich einen Microservice erstellen, welcher von diversen Tenants den aktuellen Lizenzstand abfragt und im Falle dass keine Lizenz mehr übrig ist, sollte der Supporttechniker informiert werden, damit der Bestellprozess gestartet werden kann. 

Eine Umsetzung ist mir gelungen, wie ich Sie beschrieben habe. 
Als Endprodukt habe ich einen Microservice, welcher mittels FlaskAPI und dessen Templates ein Frontend anzeigen. Zusätzlich habe ich eine Integration im SharePoint, in der ich die Daten aus der Abfrage, in eine SharePoint Liste schreibe. Wenn die freien Lizenzen bei 0 stehen, dann wird mittels PowerAutomate ein Flow gestartet, welcher dies dem Supporttechniker meldet. 

Das *Know-how* habe ich mir durch meine aktive Teilnahme am MSVC-Unterricht bei Boris Langert sowie durch die YouTube-Tutorials  <a href="https://www.youtube.com/watch?v=QXeEoD0pB3E&list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3" target="_blank">Python for Beginners | Telusko</a> von <a href="https://www.youtube.com/@Telusko" target="_blank">Telusko</a>. 

> ⚠️ **Wichtig**<br>
> Die gesammte Umsetzung wird nur in einer lokalen Dockerumgebung aufgebaut. Da diese Semesterarbeit später auch in einer Produktiven umgebung in den Einsatz kommen kann, soll diese zuerst lokal funktionieren. 
> Zusätzlich, wäre die Produktivumgebung später auch auf einem Server und würde durch Dockerdesktop betrieben/gehostet werden. Dieser Server ist aber nur durch das interne Netzwerk der Firma erreichbar
> Somit ist das Szenario, lokal auf dem eigenen Notebook realistisch und fast 1:1 das gleiche.
> 
> Ein weiterer Punkt ist der Datenschutz. 
> Da wir diverse Daten zu den jeweiligen Tenants in diesem Service haben, darf das ganze nicht in die Cloud. (genaueres folgt später)
> 
> Als erster Aufbau werden zwei Testtenants der ISE AG verwendet. Diese Simulieren dann alle Tenants, welche später ggf. gemonitort werden. 

| Abschnitt                                           | Beschreibung                                                                     | GitHub-Issue                                                                                                                           |
| --------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Sichere Verbindung zur Graph API**                | Aufbau einer zertifikatsbasierten, sicheren Verbindung zu Microsoft Graph        | [#13 Establish secure connection](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/13)                     |
| **Lizenzdaten automatisch abrufen**                 | Microservice ruft die aktuellen Lizenzstände via Graph API automatisiert ab      | [#16 Implement license fetch via Graph](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/16)               |
| **Flask Microservice Architektur**                  | Aufbau des Services mit Flask, Docker, Blueprints und SQLite                     | [#12 Set up Flask microservice architecture](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/12)          |
| **Lizenzdaten in SharePoint speichern**             | Lizenzstatus wird pro Tenant in einer SharePoint-Liste persistiert               | [#14 Store license data in SharePoint list](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/14)           |
| **Automatische Benachrichtigung via PowerAutomate** | Wenn keine Lizenzen mehr verfügbar sind, wird der Support automatisch informiert | [#15 Create PowerAutomate-Flow for alerting](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/15)          |
| **Frontend zur Lizenzanzeige**                      | Darstellung aller Lizenzdaten in einer übersichtlichen Weboberfläche             | [#17 Create frontend to visualize license data](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/17)       |
| **REST API für Frontend-Integration**               | Bereitstellung von API-Endpunkten für das Frontend                               | [#18 Develop REST API for frontend](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/18)                   |
| **Benutzerauthentifizierung via Azure**             | Zugriff nur nach Login mit Firmen-Microsoft-Konto möglich                        | [#19 Implement authentication and access control](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/19)     |
| **SharePoint als zentrale Steuerung**               | Tenant-Aktivität und Monitoring-Status steuerbar über SharePoint                 | [#20 Create SharePoint List for License Data Storage](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/20) |
| **Monitoring im Frontend steuerbar**                | Möglichkeit, Monitoring pro Tenant direkt über das UI zu aktivieren/deaktivieren | [#22 Control PowerAutomate Monitoring via Frontend](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/22)   |
| **Zentrales Logging**                               | Logfile für Fehler, API-Aufrufe und Systemzustände mit Rotation                  | [#23 Logging](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/issues/23)                                         |

### Wie soll der MSVC ablauffen?

Folgendes Diagramm zeigt auf, wie der MSVC ablaufen soll. 


![Test Gif](../../ressources/images/scheduled_task_with_writedown.gif)

**Ablaufdiagramm der App**
- **Blauer Zyklus**: Der Scheduled Task ruft periodisch den Lizenzstatus ab.
- **Grüner Pfad**: Lizenzen verfügbar – Daten werden dokumentiert.
- **Roter Pfad**: Lizenzen = 0 – PowerAutomate wird getriggert.

___

> ⚠️ **Wichtig** <br>
> Nachfolgend werden die einzelnen Implementierungsschritte aufgezeigt, wie der MSVC aufgebaut wurde. 
> Über die obere Auflistung, kann zu den Sektionen oder zu den Issues mit Userstories gesprungen werden. 

___ 
### Grundgerüst des Microservices 

Zu beginn habe ich mit der App begonnen, dort habe ich mit der Vorlage aus dem Unterricht begonnen und auf dieser Aufgebaut. 
Da wir im Unterricht immer wieder ergänzugen gemacht haben, habe ich eigentlich von 0 begonnen und bis zum schritt alles vorbereitet, bis ich dort angelangt bin, bis dahin, wo ich auf der App aufbauen möchte. 

Die Struktur war schlicht und nur gerade das nötigste. 
- Docker / Compose Files
- Blueprint implementiert
- SQLite DB

Filestruktur mit dem Grundgerüst

Mit dieser Struktur, konnte bereits mittels ersten simulativen API Calls getestet werden, jedoch nur mit Einträgen, welche von Hand in die DB gemacht wurden. 


> Zu beginn wird die Datenbank zu testzwecken verwendet, um sicher zu sein, dass die API Calls funktionieren

#### Angaben zum Microsoervice

Technologie: FlaskAPI <br>
Scriptsprache: Python <br>
Endpunkt: http://localhost:5000/api/v1 <br>
Swagger-UI: http://localhost:5000/api/v1/docs <br>


Zusätzlich wurde auch ein Swagger eingerichtet, um die einzelnen Routen zu dokumentieren.
Der Swagger ist unter folgender URL zu erreichen (Nur wenn der Docker-Container aktiv ist)
[Lizenztool-Swagger-UI](http://localhost:5000/api/v1/docs)



### Grundgerüst des Microservices

Die Entwicklung des Lizenzüberwachungstools begann mit einem einfachen Grundgerüst, basierend auf der im Unterricht vermittelten Vorlage. Im Verlauf des Semesters wurde die Vorlage stetig erweitert. Da die Unterrichtseinheiten immer wieder neue Bausteine ergänzten, entschloss ich mich dazu, die App vollständig neu aufzubauen – modular, testbar und Docker-kompatibel.

Das initiale Setup konzentrierte sich auf eine schlanke, aber funktionale Struktur:

- **Docker-/Compose-Files** zur Containerisierung und einfachen Bereitstellung
- **Blueprints** zur sauberen Trennung von Funktionen und Routen
- **SQLite** als leichtgewichtiges Datenbanksystem für die Entwicklungsphase

#### Projektstruktur

```text
licensetool
├── app
│   ├── licenses
│   │    ├── __init.py
│   │    └── routes.py
│   ├── main
│   │    ├── __init.py
│   │    └── routes.py
│   ├── models
│   │    └── license.py
│   ├── __init__.py
│   └── extensions.py
├── app.db
├── compose.test.yaml
├── compose.yaml
├── config.py
├── dockerfile
├── dockerfile.test
└── requirements.txt
```

> _Die Struktur wurde so gewählt, dass spätere Erweiterungen (z. B. neue Blueprints oder externe Services) problemlos integriert werden können._

Bereits mit diesem Setup war es möglich, erste **simulative API-Calls** durchzuführen. In der Anfangsphase wurden Testdaten manuell in die Datenbank eingetragen, um die korrekte Funktion der API-Endpunkte zu validieren.

> ℹ️ **Information** <br>
>Die SQLite-Datenbank dient in der Entwicklungsphase primär zu Testzwecken.

#### Technische Eckdaten des Microservices

| Komponente       | Beschreibung                        |
| ---------------- | ----------------------------------- |
| **Technologie**  | Flask (Flask-RESTful)               |
| **Module**       | FlaskAPI                            |
| **Sprache**      | Python                              |
| **API-Endpunkt** | `http://localhost:5000/api/v1`      |
| **Swagger UI**   | `http://localhost:5000/api/v1/docs` |


Zusätzlich wurde ein **Swagger-Dokumentationsinterface** eingerichtet, um alle API-Routen übersichtlich darzustellen. Dies erleichtert nicht nur die Entwicklung, sondern auch die spätere Integration in andere Systeme.

👉 [Lizenztool Swagger UI (lokal)](http://localhost:5000/api/v1/docs) *(nur aktiv bei laufendem Docker-Container)*


### Implementierung: Lizenzabfrage bei anderen Tenants (via Microsoft Graph)

Nachdem das Grundgerüst des Microservices steht und die ersten API-Tests erfolgreich durchgeführt wurden, ging es im nächsten Schritt darum, **die Lizenzdaten automatisiert für verschiedene Microsoft-Tenants abzufragen** und für die spätere Weiterverarbeitung (z. B. Speicherung oder Eskalation) bereitzustellen.

Da es sich bei den zu überwachenden Tenants um Microsoft-365-Umgebungen handelt, bot sich die **Microsoft Graph API** als zentrale Schnittstelle an. Ich konnte hierfür auf bestehende Erfahrungen zurückgreifen, da ich eine ähnliche Funktion bereits in einem anderen Projekt implementiert hatte.

#### Sicherheit durch Config-Profile

In der ersten Version waren die Authentifizierungsdaten fest im Code hinterlegt – das war aus Sicherheits- und Wartungsgründen jedoch nicht ideal. Für die produktionsnahe Umsetzung habe ich mich deshalb für **dynamisch ladbare JSON-Konfigurationsprofile** entschieden. Diese enthalten alle nötigen Angaben (z. B. `tenant_id`, Zertifikatspfad, Ablaufdatum) und lassen sich bei Zertifikatserneuerung einfach austauschen.

> ℹ️ **Information** <br>
> Diese Abstraktion erlaubt eine saubere Trennung von Code und Konfiguration. Neue Tenants können künftig mit minimalem Aufwand eingebunden werden – es reicht ein neues Config-File und Zertifikat im jeweiligen Ordner.

##### Beispiel eines Config-Files:

```json
{
  "tenant_id": "<tenantid>",
  "tenant_name": "tenantname",
  "client_id": "<clientid>",
  "thumbprint": "<thumbprint>",
  "cert_path": "certs/<tenantname>/mycert_<tenantname>.pem",
  "expires": "2026-05-19"
}
```

#### Erweiterung der Struktur

Im Projekt wurden folgende Ordner ergänzt:

```text
licensetool
├── app
│   ├── modules
│   │   └── mggraph.py      # Graph-Modul zur Lizenzabfrage
├── certs
│   ├── *certfolder foreach tenant*
│   ├── *info folder foreach tenant*
│   └── certcreation.sh
├── config-profiles
│   └── *config-profile foreach tenant*
│...
```

### 📡 Lizenzabfrage via Microsoft Graph API

Die eigentliche Abfrage der Lizenzinformationen (`subscribedSkus`) erfolgt über das Modul [`mggraph.py`](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/tree/main/ressources/licensetool/app/modules/mggraph.py). Dort übernimmt die Klasse `GraphLicenseClient` die Authentifizierung sowie die API-Kommunikation.

```python
class GraphLicenseClient:
    def __init__(self, tenant_name: str):
        self.tenant_name = tenant_name
        self.config = self._load_config()
        self.token = self._authenticate()

    def _load_config(self):
        config_file = f"config-profiles/config-{self.tenant_name}-profile.json"
        with open(config_file, "r") as f:
            return json.load(f)

    def _authenticate(self):
        authority = f"https://login.microsoftonline.com/{self.config['tenant_id']}"
        app = ConfidentialClientApplication(
            client_id=self.config['client_id'],
            authority=authority,
            client_credential={
                "private_key": open(self.config['cert_path'], "r").read(),
                "thumbprint": self.config['thumbprint']
            }
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        if "access_token" not in result:
            raise Exception(f"Token acquisition failed: {result.get('error_description')}")
        return result["access_token"]

    def get_license_status(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(
            "https://graph.microsoft.com/v1.0/subscribedSkus",
            headers=headers,
            timeout=10
        )
        if response.status_code != 200:
            raise Exception(f"Graph API error: {response.status_code} - {response.text}")
        return response.json()
```

### Beispielhafte API-Antwort

Die `get_license_status()`-Methode liefert eine strukturierte JSON-Antwort mit allen abonnierten Lizenzen des Tenants:

```json
[
  {
    "available_units": 20,
    "consumed_units": 19,
    "free_units": 1,
    "skuid": "94763226-9b3c-4e75-a931-5c89701abe66",
    "skupartnumber": "STANDARDWOFFPACK_FACULTY"
  },
  {
    "available_units": 1,
    "consumed_units": 1,
    "free_units": 0,
    "skuid": "0e142028-345e-45da-8d92-8bfd4093bbb9",
    "skupartnumber": "PHONESYSTEM_VIRTUALUSER_FACULTY"
  },
  {
    "available_units": 12,
    "consumed_units": 10,
    "free_units": 2,
    "skuid": "d979703c-028d-4de5-acbf-7955566b69b9",
    "skupartnumber": "MCOEV_FACULTY"
  },
  {
    "available_units": 2000,
    "consumed_units": 1500,
    "free_units": 500,
    "skuid": "314c4481-f395-4525-be8b-2ec4bb1e9d91",
    "skupartnumber": "STANDARDWOFFPACK_STUDENT"
  },
  {
    "available_units": 100000,
    "consumed_units": 7,
    "free_units": 99930,
    "skuid": "f30db892-07e9-47e9-837c-80727f46fd3d",
    "skupartnumber": "FLOW_FREE"
  }
]
```

> ℹ️ **Hinweis zu Daten und Datenschutz**  <br>
> Die angezeigten Lizenzzahlen wurden zu Test- und Demonstrationszwecken **angepasst** und entsprechen **nicht den realen Werten** produktiver Microsoft-Tenants.  
> Zudem wurden sämtliche darstellbaren Informationen im Sinne des Datenschutzes **anonymisiert oder verfremdet**, um Rückschlüsse auf reale Kundendaten auszuschliessen.

Somit haben wir bereits einen wichtigen Schritt gemacht, indem wir die Lizenzen als JSON zurück erhalten.
Als nächstes, müssen wir die Daten aufwerten und bereitmachen für das Frontend. 

___

### Implementierung: Frontend zur Visualisierung der Lizenzdaten

Nachdem die Lizenzdaten erfolgreich über die Microsoft Graph API abgerufen und als JSON verarbeitet werden konnten, wurde im nächsten Schritt ein **benutzerfreundliches Frontend** entwickelt. Dieses dient allen Mitarbeitenden – unabhängig vom technischen Hintergrund – als zentrale Übersicht, um den aktuellen Lizenzstatus jederzeit auf einen Blick einsehen zu können.

Ziel war es, eine **intuitive und optisch ansprechende Oberfläche** bereitzustellen, die den aktuellen Zustand der Lizenzen klar darstellt, Filtermöglichkeiten bietet und potenzielle Engpässe direkt ersichtlich macht – ohne dass die Nutzer mit technischen Details wie API-Calls oder Datenbanken konfrontiert werden.

#### Verfügbare Ansichten im Frontend

Es wurden mehrere HTML-Seiten (Templates) implementiert, jeweils mit eigener CSS-Datei zur Gestaltung:

| Template-Datei    | Beschreibung                                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `statusall.html`  | Übersicht aller Lizenzen aus allen Tenants in einer zentralen Tabelle                                                    |
| `tenant.html`     | Einzelabfrage eines spezifischen Tenants (z. B. Detailansicht)                                                           |
| `mainpage.html`   | Startseite / Einstiegsseite ins Tool                                                                                     |
| `monitoring.html` | Verwaltungsansicht zur Steuerung ob ein Tenant aktiv ist oder ob Mitteilungen zu diesem Tenant versendet werden sollen.  |

```text
├── app
│   ├── static
│   │    ├── images
│   │	 │    └── frontend.css
│   │    ├── mainpage.css
│   │    ├── monitoring.css
│   │    ├── statusall.css
│   │    └── tenant.css
│   ├── templates
│   │    ├── mainpage.html
│   │    ├── monitoring.html
│   │    ├── statusall.html
│   │    └── tenant.html
│...
```

#### Routenbindung der Templates

Die Templates werden mit dem Flask-Modul `render_template()` in den jeweiligen Blueprints geladen.

```python
# Beispiel einer Template-Route 
@bp.get('/status/tenant')
def show_tenant():
    return render_template("tenant.html")
```

Ausschnitt aus [`app/licenses/routes.py`](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/blob/main/ressources/licensetool/app/licenses/routes.py)

#### Funktionen im Frontend

- **Tabellarische Darstellung** aller Lizenzdaten
- **Farbliche Hervorhebung** bei kritischem Lizenzstand
- **Such- und Filterfunktionen** über JavaScript
- **Anbindung an API-Endpoint** über `fetch()` zur Anzeige der aktuellen Daten
- **Trennung von HTML, CSS und Logik (JavaScript)** für bessere Wartbarkeit

#### Beispielhafte HTML-/JS-Integration (`statusall.html`)

```html
<input type="text" id="filterInput" placeholder="z. B. ISE School">
...
<table id="licenseTable">
  <thead>
    <tr>
      <th>Tenant</th>
      <th>SKU Part Number</th>
      <th>SKU ID</th>
      <th>Verfügbar</th>
      <th>Verbraucht</th>
      <th>Frei</th>
    </tr>
  </thead>
  <tbody id="licenseBody">
    <!-- Dynamischer Inhalt -->
  </tbody>
</table>

<script>
  let fullData = [];

  function renderTable(data) {
    const tbody = document.getElementById('licenseBody');
    tbody.innerHTML = '';
    data.forEach(item => {
      const row = document.createElement('tr');
      if (item.free_units <= 0) row.classList.add('low-license');
      row.innerHTML = `
        <td>${item.tenant}</td>
        <td>${item.skupartnumber}</td>
        <td>${item.skuid}</td>
        <td>${item.available_units}</td>
        <td>${item.consumed_units}</td>
        <td>${item.free_units}</td>
      `;
      tbody.appendChild(row);
    });
  }

  fetch('/api/v1/licenses/status')
    .then(response => response.json())
    .then(data => {
      fullData = data;
      renderTable(fullData);
    });

  document.getElementById("filterInput").addEventListener("keyup", () => {
    const query = document.getElementById("filterInput").value.toLowerCase();
    const filtered = fullData.filter(item =>
      item.tenant.toLowerCase().includes(query) ||
      item.skupartnumber.toLowerCase().includes(query)
    );
    renderTable(filtered);
  });
</script>
```

#### Ziel des Frontends

Das Frontend schafft eine klare Benutzeroberfläche, in der Lizenzdaten:

- **tabellarisch dargestellt** werden
- durch **Farben oder Filter** visuell hervorgehoben sind
- gezielt nach Tenants oder Lizenztypen **gefiltert** werden können
- **aktuell** bleiben dank direkter API-Anbindung

Damit kann jede Person schnell erfassen, ob **Handlungsbedarf** besteht – z. B. vollständigem Verbrauch.

___ 

### Implementierung: SharePoint-Einbindung

Da in unserem Unternehmen intensiv mit **SharePoint** gearbeitet wird, war von Beginn an vorgesehen, die Lizenzdaten und Konfigurationen dort zentral zu verwalten. Der Microservice kommuniziert über die **Microsoft Graph API** mit SharePoint – sowohl zur Datenablage als auch zur Steuerung der Lizenzüberwachung.

Ein zusätzlicher Grund für die SharePoint-Einbindung liegt in der geplanten **Alarmierung bei Lizenzengpässen über PowerAutomate**, die auf Felder in den SharePoint-Listen reagiert. PowerAutomate wird an anderer Stelle genauer erklärt – an dieser Stelle reicht es zu wissen, dass der SharePoint auch dafür als Trigger dient.

Für den Zugriff wurde eine eigene App-Registrierung erstellt, welche ausschliesslich die Berechtigungen für den SharePoint-Zugriff besitzt.

```text
├── config-profiles
│   ├── sharepoint
│   │    └── sp-config-<name>-profile.json
```


#### Übersicht der SharePoint-Listen und Felder

##### Parameterliste – Systemweite Konfigurationswerte

|Feldname|Typ|Beschreibung|
|---|---|---|
|`Parameter`|Textfeld|Der technische Name des Parameters (z. B. Mail-Adresse)|
|`Parameterwert`|Textfeld|Der zugehörige Wert (z. B. support@iseag.ch)|

> Wird verwendet für globale Konfigurationswerte wie Empfänger, Absender, Kommunikationskanal etc.


##### Tenantliste – Steuerung der zu überwachenden Tenants

|Feldname|Typ|Beschreibung|
|---|---|---|
|`Title`|Textfeld|Anzeigename / Name des Tenants|
|`enabled`|Ja/Nein|Ob der Tenant aktiv überwacht werden soll|
|`monitoring`|Ja/Nein|Ob bei Lizenzmangel eine Alarmierung (PowerAutomate) ausgelöst werden soll|
|`cert_expires`|Datum|Ablaufdatum des hinterlegten App-Zertifikats|

> Diese Liste ist für das Aktivieren/Deaktivieren einzelner Tenants zuständig und wird bei jeder Abfrage vor der Datenverarbeitung geprüft.


##### Lizenzstatusliste – Aktuelle Lizenzwerte pro Tenant

|Feldname|Typ|Beschreibung|
|---|---|---|
|`Lizenzname`|Textfeld|Name/Bezeichnung der Lizenz (z. B. STANDARDWOFFPACK_STUDENT)|
|`Verfügbar`|Zahl|Anzahl insgesamt verfügbarer Lizenzen|
|`Gebraucht`|Zahl|Anzahl aktuell verwendeter Lizenzen|
|`Frei`|Zahl|Differenz zwischen Verfügbar und Gebraucht|
|`tenant`|Textfeld|Name des zugehörigen Tenants|
|`trigger_inform_supporter`|Ja/Nein|Wird bei 0 freien Lizenzen gesetzt, um den Flow via PowerAutomate zu starten|
|`technician_informed`|Ja/Nein|Gibt an, ob der Support bereits informiert wurde|

> Diese Liste ist der zentrale Datenspeicher des Lizenzstatus und dient zugleich als Triggerquelle für PowerAutomate.


##### Technische Umsetzung im Code

Die Aktualisierung bzw. Erstellung der SharePoint-Einträge erfolgt im Modul `mggraph.py` innerhalb der Funktion `push_license_status_to_sharepoint()`.

Für jede Lizenz wird geprüft, ob ein Eintrag bereits existiert. Falls ja, wird dieser **aktualisiert** – andernfalls **neu erstellt**. Die Entscheidung, ob das Feld `trigger_inform_supporter` gesetzt wird, basiert auf folgender Logik:

```python
if free == 0 and not technician_informed:
    sp_fields[field_mapping["Infosup"]] = True
if free > 0 and technician_informed:
    sp_fields["technician_informed"] = False
```

- **Erklärung der Triggerlogik:**
    
    - Wenn **keine freien Lizenzen** mehr verfügbar sind (`free == 0`) und der Techniker **noch nicht informiert** wurde (`technician_informed = false`), wird `trigger_inform_supporter = true` gesetzt.  
        → Dies löst den PowerAutomate-Flow zur Benachrichtigung aus.
        
    - Sobald **wieder freie Lizenzen** verfügbar sind (`free > 0`) und `technician_informed = true`, wird dieses Feld **automatisch auf `false` zurückgesetzt**, um zukünftige Trigger zu ermöglichen.
        
##### Vollständiger Ablauf zur Verarbeitung eines Lizenz-Datensatzes

Der Ablauf zur Speicherung und Aktualisierung einer Lizenz im SharePoint umfasst folgende Schritte:

```python
# Schritt 1: Tenantprüfung – nur wenn aktiv & monitoring aktiv
tenant_list_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{tenant_list_id}/items?expand=fields"
tenant_list_resp = requests.get(tenant_list_url, headers=headers)
tenant_list_resp.raise_for_status()

tenant_items = tenant_list_resp.json().get("value", [])
matching_tenant = next((item for item in tenant_items if item["fields"].get("Title") == tenant_name), None)

if not matching_tenant:
    logger.warning(f"Tenant '{tenant_name}' NICHT in Tenantliste gefunden – Abbruch.")
    return

if not matching_tenant["fields"].get("enabled", True):
    logger.info(f"Tenant '{tenant_name}' ist inaktiv – Abbruch.")
    return

if not matching_tenant["fields"].get("monitoring", False):
    logger.info(f"Monitoring für Tenant '{tenant_name}' ist deaktiviert – Abbruch.")
    return
```

```python
# Schritt 2: Abfrage bestehender Lizenz-Einträge aus SharePoint
license_list_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{license_list_id}/items?expand=fields"
license_list_resp = requests.get(license_list_url, headers=headers)
license_list_resp.raise_for_status()
existing_items = license_list_resp.json().get("value", [])
```

```python
# Schritt 3: Verarbeitung jeder Lizenz
for lic in licenses:
    sku = lic.get("skupartnumber", "UNKNOWN")
    free = lic.get("free_units", 0)
    used = lic.get("consumed_units", 0)
    avail = lic.get("available_units", 0)

    match = next(
        (item for item in existing_items if
         item["fields"].get("Title") == sku and
         item["fields"].get(tenant_field) == tenant_name),
        None
    )

    sp_fields = {
        field_mapping["Frei"]: free,
        field_mapping["Gebraucht"]: used,
        field_mapping["Verfügbar"]: avail
    }

    if match:
        item_id = match["id"]
        technician_informed = match["fields"].get("technician_informed", False)

        # Triggerlogik: Engpass und Rücksetzung
        if free == 0 and not technician_informed:
            sp_fields[field_mapping["Infosup"]] = True
        if free > 0 and technician_informed:
            sp_fields["technician_informed"] = False

        # PATCH – Eintrag aktualisieren
        url_update = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{license_list_id}/items/{item_id}/fields"
        response = requests.patch(url_update, headers=headers, json=sp_fields)
        response.raise_for_status()
        logger.info(f"Lizenz '{sku}' für Tenant '{tenant_name}' wurde aktualisiert.")
    else:
        # POST – Neuer Eintrag
        sp_fields.update({
            field_mapping["Tenant"]: tenant_name,
            field_mapping["Lizenzname"]: sku
        })
        url_create = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{license_list_id}/items"
        response = requests.post(url_create, headers=headers, json={"fields": sp_fields})
        response.raise_for_status()
        logger.info(f"Neue Lizenz '{sku}' für Tenant '{tenant_name}' erstellt.")
```


#### Verwendete Microsoft Graph Endpunkte (SharePoint)

|Aktion|HTTP-Methode|Graph-Endpunkt|
|---|---|---|
|Tenantliste abrufen|`GET`|`/sites/{site_id}/lists/{tenant_list_id}/items?expand=fields`|
|Lizenzstatus abrufen|`GET`|`/sites/{site_id}/lists/{license_list_id}/items?expand=fields`|
|Lizenzstatus aktualisieren|`PATCH`|`/sites/{site_id}/lists/{license_list_id}/items/{item_id}/fields`|
|Lizenzstatus neu erstellen|`POST`|`/sites/{site_id}/lists/{license_list_id}/items`|


___ 

### Implementierung: PowerAutomate Flow

Damit bei einem Lizenzengpass nicht manuell geprüft werden muss, ob Handlungsbedarf besteht, wurde ein **PowerAutomate-Flow** eingerichtet, der bei bestimmten Bedingungen **automatisch eine Benachrichtigung an den Support** sendet.

#### Lizenzüberwachung – Trigger bei Engpass

Der Flow wird jedes Mal ausgelöst, wenn in der **Lizenzstatusliste** ein Eintrag **geändert** wird. Dabei prüft PowerAutomate, ob das Feld `trigger_inform_supporter` auf `true` gesetzt wurde.

Die Logik im Lizenz-Microservice sieht wie folgt aus:

- Wenn **`free_units = 0`** (also keine Lizenzen mehr verfügbar sind)  
    **und** der Techniker **noch nicht informiert** wurde (`technician_informed = false`),  
    wird `trigger_inform_supporter = true` gesetzt → Flow wird getriggert.
    
- Ist `technician_informed = true`, wird **kein neuer Trigger gesetzt**, um Mehrfachbenachrichtigungen zu vermeiden.
    

Der Flow sendet bei Auslösung eine E-Mail mit den relevanten Informationen an das Support-Team.

![PowerAutomate Flow Monitoringalert](../../ressources/images/powerautomate_flow_monitoring.png)

> _Ablauf des PowerAutomate-Flows bei Lizenzengpass_

> ℹ️ **Information**  <br>
> Der MSVC setzt automatisch das Feld `technician_informed` **zurück auf `false`**, sobald bei einem Lizenzprodukt **wieder freie Lizenzen verfügbar sind** (d. h. `free_units > 0`).  
> Dies stellt sicher, dass beim nächsten Engpass erneut eine Benachrichtigung über den PowerAutomate-Flow ausgelöst werden kann.  
> Das Rücksetzen erfolgt nur, wenn zuvor `technician_informed = true` war. Die gesamte Logik wird serverseitig im MSVC beim Schreiben in den SharePoint gesteuert.


#### Zertifikatsüberwachung – Ablaufwarnung

Ein zweiter Flow dient zur **Überwachung der Gültigkeit von App-Zertifikaten**, welche für die Authentifizierung via Microsoft Graph notwendig sind.

Er wird periodisch ausgeführt und überprüft das **Ablaufdatum (`cert_expires`)** in der Tenantliste. Sobald ein Zertifikat **in weniger als 7 Tagen** abläuft, wird automatisch eine Benachrichtigung verschickt.

![PowerAutomate Flow Zertifikat am ablaufen](../../ressources/images/powerautomate_flow_cert-expiration.png)

> _Ablauf des PowerAutomate-Flows zur Zertifikatsüberwachung_

> ℹ️ **Hinweis:**  <br>
> Beide Flows greifen direkt auf die **SharePoint-Listenstruktur** zu, welche vom Microservice gepflegt wird. Die Automatisierung sorgt dafür, dass **kritische Zustände (wie Lizenzmangel oder Zertifikatsablauf)** nicht unbemerkt bleiben.

___

### Implementierung: Authentifizierung

Damit nicht jede beliebige Person den Microservice nutzen kann, wurde eine Benutzerauthentifizierung via Microsoft eingebaut. Dabei kommt der **OAuth 2.0 Authorization Code Flow** zum Einsatz, welcher über **Microsofts Azure Active Directory** gesteuert wird. Ein Login ist Voraussetzung, um Zugriff auf API-Endpunkte oder das Frontend zu erhalten.

Ziel war es, keine eigene Benutzerdatenbank aufzubauen, sondern stattdessen bestehende Azure-Konten (Firmen-Accounts) zu nutzen.

#### Funktionsweise

Beim Aufruf geschützter Routen wird geprüft, ob ein gültiger Benutzer-Token vorhanden ist. Falls nicht, wird automatisch auf Microsofts Login-Seite weitergeleitet.

Nach erfolgreichem Login erhält der Microservice über einen Redirect den Access-Token sowie Benutzerinformationen zurück. Diese werden lokal in der **Session** gespeichert und für Folgeanfragen verwendet.

#### Technische Umsetzung

| Datei                   | Funktion                                                                |
| ----------------------- | ----------------------------------------------------------------------- |
| `routes.py`             | Regelt Login, Callback, Logout und optionalen Test-Login                |
| `utils.py`              | Enthält den `login_required`-Decorator zum Absichern von Routen         |
| `config-profiles/auth/` | Speichert Verbindungsdaten zur Azure App (Client ID, Secret, Tenant ID) |

Im Projekt wurden folgende Ordner ergänzt:

```text
├── app
│   └── Auth
│        ├── __init__.py
│        ├── routes.py
│        └── utils.py
│
├── config-profiles
│   └── auth
│        └── *Config-profile for auth-module*
│...
```

>🔐 **Wichtig:** <br>
>Ohne gültige Session wird der Zugriff verweigert – sowohl auf das **Frontend** als auch auf die **API-Endpunkte**.  
>**Ausnahme:** Die `mainpage.html` bleibt öffentlich zugänglich und ist **nicht geschützt**.

___

### Implementierung: Monitoring-Verwaltung

Falls es einmal Probleme mit einem Tenant gibt – oder ein neuer Tenant gerade erst erfasst wurde –, kann dessen **Aktivierung** sowie das **Monitoring-Verhalten** direkt über das Frontend gesteuert werden.

Dies erfolgt über den Bildschirm [`monitoring.html`](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/blob/main/ressources/licensetool/app/templates/monitoring.html), welcher eine Übersicht aller registrierten Tenants bietet.

![Bild Monitoring]()

> Über diesen Screen lassen sich **pro Tenant** sowohl die Option _Aktiv (enabled)_ als auch _Monitoring aktiv (monitoring)_ ein- oder ausschalten.

Die Änderungen wirken sich direkt auf die **SharePoint-Tenantliste** aus und bestimmen, ob ein Tenant vom Microservice berücksichtigt wird und ob eine Alarmierung via PowerAutomate erfolgen soll.

Mit dem Monitoring werden folgende Strukturanpassungen gemacht:

```text
licensetool
├── app
│   └── monitoring
│        ├── __init.py
│        └── routes.py
│...
```


___

### Implementierung: Logging & Testing

Um im Fehlerfall gezielt analysieren zu können, **wurde ein zentrales Logging** sowie eine dedizierte **Testumgebung** eingerichtet. Beide Komponenten dienen der Qualitätssicherung und sorgen dafür, dass die Anwendung erst bei stabilem Zustand produktiv eingesetzt wird.

#### Testumgebung & Pytest

Vor jedem produktiven Rollout wird der Container in einer **abgeschirmten Laborumgebung** getestet. Dabei simulieren vorbereitete Datensätze typische Szenarien und prüfen die API auf korrekte Funktion.

Die Tests werden mit **`pytest`** ausgeführt – einem flexiblen Framework für automatisiertes Testen in Python. Nur wenn ein definierter Prozentsatz der Tests erfolgreich ist, wird der Service live geschaltet.

#### Ergänzungen in der Projektstruktur

```Text
licensetool
├── app
│   └── modules
│        └── logging.py
├── logs
│   └── licensetool.log
├── test
│   ├── __init__.py
│   ├── conftest.py
│   ├── create_test_data.py
│   ├── test_auth.py
│   ├── test_license.py
│   ├── test_main.py
│   └── test_monitoring.py
├── compose.test.yaml
├── dockerfile.test
│...
```

#### Logging-Modul

Das Logging wurde über ein zentrales Modul `logging.py` umgesetzt. Dieses initialisiert sowohl **Datei-Logging** als auch **Konsolen-Ausgabe** mit Rotation:

```python
def setup_logging(log_file='logs/licensetool.log', level=logging.INFO):
    ...
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
    ...
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    ...
```

**Log-Ausgabe**:  
Alle Logs werden standardmäßig unter `logs/licensetool.log` gespeichert und bei 5 MB automatisch rotiert.

Beispielauszug aus dem Log:

```log
2025-06-19 11:22:03,699 [INFO] app.licenses.routes: Alle Lizenzstatus werden geladen (status/show)
2025-06-19 11:22:06,092 [INFO] app.licenses.routes: Lade Lizenzstatus für Tenant: ISE School 2013
2025-06-19 11:22:07,093 [INFO] werkzeug: 172.22.0.1 - - [19/Jun/2025 11:22:07] "GET /api/v1/licenses/status/show HTTP/1.1" 200 -
```

>ℹ️ **Hinweis:**  <br>
> Über `logger.info()` und `logger.error()` im gesamten Code lassen sich **zielgerichtet Debug-Informationen** schreiben – etwa bei Authentifizierungsproblemen oder SharePoint-Fehlern.


___ 
### Erweiterung: Lizenz-Produktnamen

Aktuell werden die Lizenzen technisch anhand ihrer **SKU Part Number** identifiziert – zum Beispiel `STANDARDWOFFPACK_STUDENT` oder `FLOW_FREE`. Diese Systemnamen sind jedoch nicht für alle Benutzer direkt verständlich.

Um die **Lesbarkeit und Benutzerfreundlichkeit** zu verbessern, wurde ein zusätzliches **Dictionary** eingeführt, das die **SKU Part Numbers** den entsprechenden **Display Names** (also Klartextnamen) zuordnet.

> Die SKU-Nummer bleibt weiterhin erhalten und wird im Datensatz mitgeführt – der Displayname dient ausschließlich zur besseren Darstellung im Frontend.

Beispielhafte Zuordnung im Dictionary:

```python
PRODUCT_DISPLAY_NAMES = {
    "STANDARDWOFFPACK_STUDENT": "Office 365 A1 for Students",
    "FLOW_FREE": "Power Automate Free",
    ...
}
```

> Das gesamte Mapping-File findet ihr unter [`sku_mappings.json`](https://github.com/Radball-Migi/HF-ITCNE24-SemArbeit3-MSVC-Lizenztool/blob/main/ressources/licensetool/config/sku_mappings.json)

___ 

### Optimierung / Erweiterung: Frontend-Datenbank

Wie zu Beginn erwähnt, war die SQLite-Datenbank ursprünglich **nur als temporärer Speicher für Testzwecke** vorgesehen. Während der Entwicklung zeigte sich jedoch, dass der **Microsoft Graph API-Aufruf** – insbesondere in Kombination mit der **SharePoint-Synchronisation** – zu **spürbaren Wartezeiten** im Frontend führte.

#### Performanceproblem durch Live-Abfrage

Die Verzögerung trat vor allem dann auf, wenn Lizenzdaten **live über Graph geladen und anschließend in SharePoint geschrieben** wurden. Da dieser Prozess je nach Tenant und Anzahl der Lizenzen mehrere Sekunden dauern kann, **wirkte das Frontend träge** und unresponsive.

#### Lösung: Beibehalten der SQLite-Datenbank

Um dem entgegenzuwirken, wurde entschieden, die **lokale SQLite-Datenbank weiterhin im System zu belassen** – nicht als primärer Datenspeicher, sondern **als Cache für das Frontend**.

Diese Optimierung bringt mehrere Vorteile:

- **Frontend-Zugriffe** auf Lizenzdaten erfolgen schnell und ohne API- oder Netzwerkaufruf
    
- **Benutzerinteraktionen** (z. B. Filterung, Monitoring-Umschaltung) bleiben performant
    
- Die **Live-Daten** via Microsoft Graph stehen weiterhin bei Bedarf zur Verfügung
    

#### Zwei Betriebsmodi im Frontend

Das System unterscheidet nun zwei Zugriffsarten:

|Modus|Beschreibung|
|---|---|
|**Nur Ansehen (Default)**|Zeigt die Lizenzdaten aus der SQLite-Datenbank (schnell, reiner Lesezugriff)|
|**Aktualisieren in SP**|Führt einen Live-API-Call durch, **speichert die Lizenzdaten zuerst lokal in die SQLite-DB** und überträgt sie danach **in den SharePoint**. Dabei kann auch der `trigger_inform_supporter` gesetzt werden|

> 📌 **Hinweis:**  <br>
> Die zweite Option sollte **nur bei Bedarf** genutzt werden – z. B. zur manuell angestoßenen Aktualisierung oder zur Prüfung, ob eine Alarmierung nötig ist.

#### Zielsetzung

Die **SQLite-Datenbank** dient in dieser Architektur als **lokaler Zwischenspeicher**, um die Performance und Reaktionszeit des Frontends deutlich zu verbessern – insbesondere bei umfangreichen Lizenzdaten oder mehreren Tenants.

Während alle **geschäftskritischen Prozesse** wie Monitoring, Benachrichtigungen oder die langfristige Datenspeicherung weiterhin über **SharePoint** und **Microsoft Graph** abgewickelt werden, sorgt die lokale DB dafür, dass das Frontend auch bei hohen Abfragefrequenzen **stabil und schnell** bleibt.

>  Dadurch bleibt die Anwendung auch bei wachsender Tenant-Anzahl und parallelen Zugriffen **leistungsfähig und nutzerfreundlich**.

Die Datenbankstruktur ist wie folgt aufgebaut:

```mermaid
classDiagram
    class LicenseModel {
        +Integer id
        +String name
        +Integer count
    }

    class LicenseIn {
        +String name
        +Integer count
    }

    class LicenseOut {
        +Integer id
        +String name
        +Integer count
    }

    class LicenseStatusOut {
        +String skuid
        +String skupartnumber
        +Integer consumed_units
        +Integer available_units
        +Integer free_units
    }

    class LicenseStatusAllOut {
        +String skuid
        +String skupartnumber
        +Integer consumed_units
        +Integer available_units
        +Integer free_units
        +String tenant
    }

    %% Beziehungen
    LicenseIn --|> LicenseModel
    LicenseOut --|> LicenseModel
    LicenseStatusAllOut --|> LicenseStatusOut
```


___ 

### Was wäre wenn: Cloud-Implementierung (CI/CD mit GitLab & AWS)

Theoretisch sollte ein solcher Microservice in einer **Cloud-Umgebung gehostet** werden – beispielsweise für Hochverfügbarkeit, Skalierbarkeit und zentrale Zugriffe.  
In diesem Projekt wurde jedoch bewusst auf eine lokale Lösung gesetzt, da **Lizenzdaten sensible Informationen enthalten**, deren Verarbeitung in externen Clouds **nicht DSGVO-konform** wäre.  
(Detaillierte Infos: [Datenschutz in diesem Microservice](#Datenschutz-in-diesem-Microservice))

#### Ziel dieser Sektion

Trotz der lokalen Umsetzung soll hier aufgezeigt werden, **wie ein Deployment in der Cloud** aussehen _würde_ – inklusive automatisiertem **Build** und **Deployment** mittels **CI/CD-Pipeline** (am Beispiel GitLab + AWS).

#### Voraussetzungen & Komponenten

|Komponente|Zweck|
|---|---|
|**AWS EC2**|Virtuelle Linux-Maschine als Cloud-Host|
|**Elastic IP**|Statische IP für externen Zugriff auf den Microservice|
|**GitLab Repo**|Source-Code-Management & CI/CD Pipeline|
|**Docker Desktop**|Für lokale Tests vor Deployment (nicht produktiv verwendet)|


#### Infrastruktur & CI/CD-Ablauf

#### Infrastruktur & CI/CD-Ablauf

1. **Code-Push auf GitLab**  
    Triggert die CI/CD-Pipeline automatisch.
    
2. **GitLab CI/CD Pipeline**
    
    - Führt Tests mit `pytest` durch
        
    - Erstellt ein Docker-Image
        
    - **Pusht das Image in die GitLab Container Registry**
        
3. **Deployment auf AWS EC2**  
    Das Docker-Image wird auf einer EC2-Instanz (z. B. Ubuntu) gestartet – zusammen mit einer MySQL-Datenbank.  
    **Gunicorn** fungiert als produktionsfähiger WSGI-Server.


>ℹ️ **Hinweis:**  <br>
>Die nachfolgenden Konfigurationsdateien sind **nicht Teil der aktuellen Projektstruktur**, da der Microservice bislang **nur lokal betrieben** wird. Sie zeigen exemplarisch, **wie eine Cloud-Integration mittels CI/CD** technisch umgesetzt werden könnte.


#### CI/CD-Pipeline-Konfiguration (GitLab)

**`.gitlab-ci.yml`** – Definiert das Build- und Testverhalten:

```yaml
stages:
  - test

test:
  stage: test
  image: python:3.10
  before_script:
    - pip install -r requirements.txt
    - pip install pytest
  script:
    - pytest app/test
    - pytest --cov=app app/test

```

#### Warum GitLab Container Registry?

Ein zentrales Element dieser CI/CD-Pipeline ist die Nutzung der **GitLab Container Registry**.  
Sie ermöglicht es, Docker-Images direkt beim Commit automatisiert zu bauen, zu versionieren und zentral im GitLab-Projekt zu speichern.

**Vorteile im Überblick:**

| Vorteil                             | Beschreibung                                                                               |
| ----------------------------------- | ------------------------------------------------------------------------------------------ |
| **Nahtlose GitLab-Integration**     | Kein externer Registry-Anbieter notwendig – alles innerhalb von GitLab verwaltet           |
| **Automatisierter Build & Tagging** | Images werden bei jedem Commit mit `:latest` und `:<commit>` getaggt – ideal für Rollbacks |
| **Zentraler Zugriffspunkt**         | EC2-Instanzen, Staging-Server oder andere Microservices können direkt darauf zugreifen     |
| **Sichere Authentifizierung**       | Kein manuelles Passworthandling – Zugriff über `CI_JOB_TOKEN`                              |
| **Skalierbar & übersichtlich**      | Jedes Projekt verwaltet seine Images isoliert und nachvollziehbar                          |

#### Produktionsumgebung (Docker Compose)

**`docker-compose.prod.yaml`** – Setzt API & DB auf:

```yaml
services:

  prod-hf-itcne24-semarbeit3-msvc-lizenztool-api:
    image: ${FLASK_BLUEPRINT_IMAGE}
    build:
      context: .
      dockerfile: 'Dockerfile.prod'
    container_name: prod-hf-itcne24-semarbeit3-msvc-lizenztool
    environment:
      - DATABASE_URI=mysql+mysqlconnector://root:root@prod-hf-itcne24-semarbeit3-msvc-lizenztool-db:3306/msvc-prod
    ports:
      - 5000:5000
    depends_on:
      prod-hf-itcne24-semarbeit3-msvc-lizenztool-db:
        condition: service_healthy

  msvc-bp-prod-db:
    image: mysql:8.4.4
    container_name: prod-hf-itcne24-semarbeit3-msvc-lizenztool-db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: msvc-prod
    healthcheck:
      test: mysqladmin ping -h localhost -uroot --password=$$MYSQL_ROOT_PASSWORD
      start_period: 2s
      interval: 5s
      timeout: 5s
      retries: 55
    ports:
      - 3306:3306
    volumes:
      - msvc-prod-db:/var/lib/mysql

volumes:
  prod-hf-itcne24-semarbeit3-msvc-lizenztool-db:

```

#### Produktions-Image mit Gunicorn

**`Dockerfile.prod`** – Für den produktiven Build:

```Dockerfile
FROM python:alpine3.21
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000
ADD . /app

CMD gunicorn -b 0.0.0.0:5000 wsgi:app

```

#### Zusammenfassung: Vorteile der CI/CD-Cloud-Pipeline

|Schritt|Beschreibung|
|---|---|
|**Automatisierter Build**|GitLab erzeugt Image bei jedem Commit|
|**Testdurchläufe**|Pytest validiert Code vor Deployment|
|**Cloud-Deployment**|EC2-Instanz erhält aktuelle Version automatisch|
|**Zugriff via IP**|Externe Anfragen via `http://<elastic-ip>:`|


___ 

## Datenschutz in diesem Microservice

Wie bereits in der Hinweisbox zu Beginn erwähnt, wird dieser Microservice **lokal in einem Docker-Container auf Docker Desktop** betrieben. Der Grund dafür ist der Schutz von Personendaten gemäss dem **revidierten Datenschutzgesetz (revDSG, SR 235.1)**. Eine Cloud-Verarbeitung wird vermieden, da die bearbeiteten Daten potenziell besonders schützenswert sein können und Risiken durch externe Verarbeitung reduziert werden sollen.

Gemäss **Artikel 7 revDSG** (_Datenschutz durch Technik und datenschutzfreundliche Voreinstellungen_) gilt:

> _„Der Verantwortliche trifft bereits bei der Planung der Bearbeitung sowie bei der Bearbeitung selbst geeignete technische und organisatorische Massnahmen, um die Datenschutzvorschriften einzuhalten, insbesondere die Grundsätze nach Artikel 6.“_

Obwohl der Zugriff über eine **Microsoft-Authentifizierung** abgesichert ist, besteht dennoch ein Restrisiko, dass Benutzerkonten kompromittiert werden könnten. Dies betrifft die Anforderungen zur **Datensicherheit** nach **Artikel 8 revDSG** (_Datensicherheit_), wo es heisst:

> _„Personendaten müssen durch geeignete technische und organisatorische Massnahmen gegen unbefugtes Bearbeiten geschützt werden.“_

### Sensitive Daten

Im Tool ist ersichtlich, welcher Tenant über welche und wie viele Microsoft-Lizenzen verfügt. Anhand dieser Lizenzinformationen – z. B. Lehrer- und Schülerlizenzen an einer Schule – lassen sich Rückschlüsse auf die Anzahl und Zusammensetzung der Benutzergruppen ziehen. Gemäss **Artikel 5 lit. a revDSG** sind Personendaten definiert als:

> _„alle Angaben, die sich auf eine bestimmte oder bestimmbare natürliche Person beziehen“._

Da bei Schul- oder KMU-Installationen oft klar ist, welche Gruppen (Lehrpersonen, Lernende, Mitarbeitende) mit welchen Lizenzen arbeiten, können diese Angaben als **bestimmbare Personendaten** gelten.

Zudem kann durch Premiumlizenzen indirekt erkannt werden, welche Tools oder Dienste verwendet werden. Diese Informationen erlauben möglicherweise Rückschlüsse auf interne Organisation oder Geschäftsstrategien. Je nach Kontext könnten solche Angaben unter die **besonders schützenswerten Personendaten** gemäss **Artikel 5 lit. c revDSG** fallen, insbesondere wenn sie Rückschlüsse auf berufliche Tätigkeiten, Gruppenzugehörigkeit oder Verhaltensmuster erlauben.

### Kurzgesagt:
Aus Datenschutzgründen wird der Microservice lokal im Docker-Container betrieben und nicht in der Cloud gehostet. Obwohl Microsoft Authentication verwendet wird, besteht bei kompromittierten Konten ein Restrisiko. Das Tool zeigt sensible Informationen wie Tenant-Daten, Lizenztypen und -anzahl. Daraus lassen sich Rückschlüsse auf Nutzergruppen (z. B. Schüler, Lehrpersonen) und eingesetzte Dienste ziehen – was datenschutzrechtlich heikel sein kann.

