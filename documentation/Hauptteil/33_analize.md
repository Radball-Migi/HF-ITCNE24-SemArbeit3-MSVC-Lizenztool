---
layout: default
title: 3.3 Analysieren
parent: 3. Hauptteil
nav_order: 6
---
# Analysieren (Analyze) Phase

Die Analyze-Phase ist der dritte Schritt in einem Six Sigma Projekt. Hier werden die in der [Measure-Phase](./32_measure.md) gesammelten Daten analysiert, um die Ursachen von Problemen zu identifizieren. Ziel ist es, die Hauptursachen für Prozessabweichungen zu bestimmen und Hypothesen für Verbesserungen zu entwickeln. Dies umfasst die Nutzung statistischer Methoden und Werkzeuge, um Muster und Zusammenhänge in den Daten zu erkennen.


![Analyze](../../ressources/images/analyze.png)

[Quelle](../Quellverzeichnis/index.md#analyze-phase)

## Zusammenfassung der Datenerhebung

Die [Measure-Phase](./32_measure.md) hat gezeigt, dass der aktuelle Prozess der Lizenzverwaltung bei der ISE AG aus Kundensicht eher suboptimal läuft und bei Problemen eine schnelle Lösung nicht gefunden wird. 
Es besteht ein hoher Bedarf, dies zu verbessern, um die Antwort/Lösungszeiten zu verkürzen. 
#### 1. **Lange Lösungszeiten**

Die Behebung von Lizenzproblemen dauert im bestehenden Ablauf oft mehrere Tage. Die wichtigsten Ursachen:

- **Manuelle Bearbeitung über mehrere Stationen**: Ein Ticket muss gesichtet, zugewiesen und bearbeitet werden – jeder Schritt kostet Zeit.
    
- **Hohe Auslastung des IT-Supports**: Neue Anfragen bleiben bei grösserem Ticketvolumen oft zunächst unbearbeitet.
    
- **Kundenfreigabe notwendig**: Bevor eine Lizenz bestellt werden kann, muss der Kunde die Kosten und Massnahme schriftlich freigeben. Diese Zustimmung wird manuell über Outlook/Ticketsystem eingeholt – das kann zusätzliche Zeit in Anspruch nehmen.
    
- **Externe Abhängigkeit von Microsoft**: Nach Freigabe und Bestellung benötigt Microsoft (bzw. der Lizenzdistributor) bis zu drei Arbeitstage für die Lizenzbereitstellung. Teilweise kann es auch länger wie eine Woche andauern. 
    
- **Keine automatisierte Statusverfolgung**: Der aktuelle Prozess bietet keine Transparenz darüber, in welchem Schritt sich die Anfrage befindet.

#### 2. **Fehlerquoten**

Die Fehleranalyse zeigt, dass durch den manuellen Ablauf regelmäßig Probleme entstehen:

- **Doppelte Bearbeitung** bei unzureichender Nachverfolgung
- **Falsche Lizenztypen bestellt** aufgrund ungenauer Kommunikation
- **Fehlende Standardisierung**, etwa bei der Ticketbeschreibung oder der Freigabeanfrage

#### 3. **Hoher Ressourceneinsatz**

Der Prozess ist stark personalabhängig und bindet viel Zeit:

- IT-Support, Fachverantwortliche und ggf. Einkauf sind involviert
- Kommunikation mit dem Kunden erfolgt manuell über E-Mail
- Rückfragen und Nachbesserungen führen zu Mehraufwand, der vermieden werden könnte    

#### 4. **Fehlende Transparenz und Prozesskontrolle**

- Es gibt **keine zentrale Übersicht**, welche Lizenzen bestellt oder zugewiesen wurden
- **Dokumentation erfolgt verteilt** über verschiedene Systeme (z. B. Tickets, Outlook, Excel)
- Der Prozess ist **nicht klar definiert oder standardisiert**, was zu unterschiedlichen Abläufen bei verschiedenen Mitarbeitenden führt

---

#### **Fazit der Analyse:**  
Der bestehende Prozess zur Lizenzvergabe ist durch manuelle Freigaben, fehlende Standardisierung und externe Abhängigkeiten geprägt. Die notwendige Kundenfreigabe per Outlook verzögert den Ablauf zusätzlich, da keine systemgestützte Rückmeldung oder Eskalation existiert. Die Analyse zeigt, dass ein integriertes Tool mit standardisierten Eingaben, Freigabeprozessen und transparenter Statusverfolgung eine deutliche Effizienzsteigerung ermöglichen kann.

## Wie könnte dies gelöst werden

Was sicher feststeht, dass wir nur unsere internen Prozesse anpassen können, jedoch auch nicht alle auf einen Schlag. 

Es können folgende Lösungen verfolgt werden. 
Mittels Microsoft Graph API kann auf den aktuellen Stand der Lizenzen in einem Tenant zugegriffen werden. 
Wenn man dann ein Monitoring System anhängen würde, dann könnte der Support bereits bei einem Triggerpunkt alarmiert werden. 
Damit nicht jeder sich auf eine SharePoint-Site oder ein Excel durchklicken muss, würde noch ein Frontend eingebaut werden, welches den Stand aller konfigurierten Tenants oder auch einzelne abfragt. 
Eine Alarmierung bei niedrigem Lizenzstand, würde dann an den Support gehen, welcher dann die Einwilligung des Kunden einholt, sobald dies gemacht wurde, wird über das Frontend die Bestellung bei den Verantwortlichen ausgelöst. 



