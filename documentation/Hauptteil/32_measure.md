---
layout: default
title: 3.2 Messen
parent: 3. Hauptteil
nav_order: 5
---
# Messen (Measure) Phase

Die Measure-Phase ist der zweite Schritt in einem Six Sigma Projekt. Hier werden aktuelle Prozesse gemessen, um eine Basislinie zu erstellen. Dies umfasst die Sammlung und Analyse von Daten, um die aktuelle Leistung zu verstehen und Verbesserungspotenziale zu identifizieren. Ziel ist es, eine klare Darstellung des aktuellen Zustands zu erhalten.

![Measure](../../ressources/images/measure.png)

[Quelle](../Quellverzeichnis/index.md#measure-phase)

## Aktuelle Situation (Ist-Zustand)

Im aktuellen Prozess werden Microsoft-Lizenzen **nicht aktiv überwacht**. Es existiert kein automatisierter Mechanismus zur frühzeitigen Erkennung von Engpässen oder Erreichung von Kapazitätsgrenzen.

## Prozessbeschreibung (derzeitiger Ablauf)

1. **Benutzeranlage oder Kundenmeldung**  
    Eine Lizenzknappheit fällt erst auf, wenn:
    
    - ein neuer Benutzer erstellt wird und keine Lizenz zugewiesen werden kann,  
        **oder**
        
    - sich ein Kunde meldet, weil Benutzer keinen Zugriff auf Office-Dienste haben.

![Comicimage of client and user](../../ressources/images/error_licenses.png)

[Quelle](../Quellverzeichnis/index.md#prozessbeschreibung)

2. **Manuelle Eskalation**  
    Das Support-Team oder der/die zuständige IT-Mitarbeiter:in prüft manuell den Lizenzstatus im Microsoft-Admin-Center.
    
3. **Bestellung von Lizenzen**  
    Die zuständige Person bestellt neue Lizenzen beim Provider. Dabei kann der Prozess folgende Hürden beinhalten:
    
    - Genehmigungen
    - Budgetfreigaben
    - Kommunikation mit dem Lizenzanbieter
    
4. **Lieferzeit**  
    Vom Zeitpunkt der Bestellung bis zur effektiven Verfügbarkeit im Tenant vergehen bis zu 3 Werktage.
    
5. **Nachträgliche Lizenzzuweisung**  
    Erst nach Erhalt der Lizenzen wird dem betroffenen Benutzer die Lizenz manuell zugewiesen.
    

#### Risiken & Auswirkungen

- Verzögerungen beim Onboarding neuer Mitarbeitender
- Hoher manueller Aufwand & Fehleranfälligkeit
- Schlechte Kundenerfahrung durch unerwartete Funktionsausfälle
- Kein Überblick über Lizenzverfügbarkeit & -verbrauch

## Datenerhebung

Zur Analyse des aktuellen Lizenzprozesses wurden folgende Daten erhoben:

- **Zeitaufwand**: Durchschnittliche Zeit, die benötigt wird, um ein Lizenzproblem vom Auftreten bis zur vollständigen Behebung zu lösen.
    
- **Fehlerquote**: Häufigkeit von Problemen im Zusammenhang mit fehlenden, abgelaufenen oder falsch zugewiesenen Lizenzen sowie der Anteil von Nacharbeiten (z. B. durch manuelle Korrekturen).
    
- **Ressourceneinsatz**: Anzahl der Mitarbeitenden (z. B. IT-Support, Admins), die regelmässig in die Bearbeitung von Lizenzthemen involviert sind.    

Die Ergebnisse dieser Datenerhebung bilden die Grundlage für die nachfolgende [Analyse](33_analyze.md), in der Engpässe, Ineffizienzen und potenzielle Ursachen für Schwankungen im Prozessverlauf detailliert untersucht werden.






