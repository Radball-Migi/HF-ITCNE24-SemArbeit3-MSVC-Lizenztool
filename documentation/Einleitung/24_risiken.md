---
layout: default
title: 2.4 Risiken
parent: 2. Einleitung
nav_order: 6
---
# Risiken

Bei Projektarbeiten sind Risiken immer vorhanden. Diese Risiken können jedoch im Voraus identifiziert und geeignete Massnahmen getroffen werden. So wird sichergestellt, dass das Projekt planmässig verläuft und die festgelegten Ziele erreicht werden.

**Während der Arbeit rechne ich mit folgenden Risiken :** 

| Risiko                                                              | Eintritt | Auswirkung | Massnahme zur Vermeidung / Minderung                                         |
| ------------------------------------------------------------------- | -------- | ---------- | ---------------------------------------------------------------------------- |
| Zeitverzögerung durch technisches Debugging oder fehlendes Know-how | Hoch     | Mittel     | Zeitpuffer einplanen, Fokus auf MVP, Probleme frühzeitig angehen             |
| Fehlerhafte oder unvollständige API-Abfragen (Graph API)            | Mittel   | Hoch       | Ausgiebig mit Testdaten prüfen, Logging & Fehlerbehandlung implementieren    |
| SharePoint-Zugriffsprobleme (z. B. Berechtigungen, API-Limits)      | Mittel   | Mittel     | Rechte und Zugriff frühzeitig testen, Alternativlösung vorbereiten           |
| Power Automate Benachrichtigungen funktionieren nicht zuverlässig   | Niedrig  | Hoch       | Flows früh einrichten, mit Testfällen absichern, manuelle Kontrolle ergänzen |
| GitHub-Dokumentation wird nicht laufend gepflegt                    | Niedrig  | Niedrig    | Doku fix in Workflow einplanen, regelmässige Erinnerung im Taskboard         |

```mermaid
%%{init: {"quadrantChart": {"chartWidth": 500, "chartHeight": 500, "quadrantTextTopPadding": 100}, "themeVariables": {"quadrant1TextFill":"#808080", "quadrant2TextFill":"#808080", "quadrant3TextFill":"#808080", "quadrant4TextFill":"#808080"} }}%%

quadrantChart

  title Risikoanalyse: Eintrittswahrscheinlichkeit vs. Auswirkung
    x-axis Niedrig --> Hoch
    y-axis Gering --> Stark

	quadrant-1 Hoch riskant
    quadrant-2 Kritisch
    quadrant-3 Akzeptabel
    quadrant-4 Beobachten

"Debugging": [0.8, 0.5]
"Fehlerhafte API-Abfragen": [0.5, 0.9]
"SharePoint-Zugriffsprobleme": [0.5, 0.5]
"Power Automate": [0.2, 0.9]
"GitHub-Doku ungepflegt": [0.2, 0.2]
```
