---
layout: default
title: 5.1 Erreichte Ziele
parent: 5. Abschluss
nav_order: 3
---

# Wurden sämtliche Zielsetzungen erfüllt?



![Reached Goals](../../ressources/images/reached-goals.png)

[Quelle](../Quellverzeichnis/index.md#erreichte-ziele) 


Um die angestrebten Ziele der Semesterarbeit zu rekapitulieren, möchte ich diese im Folgenden nochmals zusammenfassen:


| Titel                               | Beschreibung                                                                                                                       | Abgehakt |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------- |
| Automatisierte Lizenzdatenerfassung | Entwicklung eines Microservices, der Lizenzinformationen selbstständig aus Kundensystemen via Microsoft Graph API abruft.          | ✅        |
| Zentrale Datenhaltung               | Speicherung der gesammelten Lizenzdaten in einer SharePoint-Liste zur einfachen Integration in die bestehende ISE-Umgebung.        | ⚠️✅      |
| Visuelle Darstellung im Frontend    | Bereitstellung eines benutzerfreundlichen Frontends, das eine schnelle und übersichtliche Einsicht in den Lizenzstatus ermöglicht. | ✅        |
| Automatisierte Benachrichtigungen   | Implementierung einer automatischen Alarmierung bei kritischen Zuständen mittels Power Automate.                                   | ✅        |
| Mehrwert für den Betrieb schaffen   | Schaffung eines Tools, das real im ISE-Alltag eingesetzt werden kann und Effizienz sowie Qualität im Lizenzmanagement erhöht.      | ✅        |

Die meisten der definierten Ziele konnten im Rahmen der Semesterarbeit erfolgreich umgesetzt und dokumentiert werden. Dennoch war es nicht möglich, sämtliche ursprünglichen Anforderungen vollständig zu realisieren, weshalb im Laufe der Entwicklung einzelne Anpassungen erforderlich waren.

Ein zentrales Ziel bestand darin, SharePoint als primäre Datenablage („Datenbank“) zu verwenden. Während der Umsetzung stellte sich jedoch heraus, dass die Verarbeitung und Darstellung der Daten über SharePoint – insbesondere in Verbindung mit dem Frontend – zu erheblichen Verzögerungen führte. Aus diesem Grund wurde zusätzlich eine SQLite-Datenbank integriert, um Zwischenergebnisse lokal zu cachen. Diese Massnahme führte zu einer signifikanten Verbesserung der Performance im Frontend.

Darüber hinaus wurde anstelle einer herkömmlichen Authentifizierung direkt auf die Microsoft 365-Authentifizierung gesetzt. Diese Entscheidung verbessert die Benutzererfahrung erheblich, da dadurch Single Sign-On (SSO) für Endnutzer möglich ist. Auch sicherheitstechnisch bietet dieser Ansatz Vorteile: Die Integration einer Multi-Faktor-Authentifizierung (MFA) ist problemlos umsetzbar, wodurch ein höheres Schutzniveau gegenüber klassischer Authentifizierung gewährleistet werden kann.
## Wie wurden die Ziele erreicht?

Um während der gesamten Semesterarbeit den Überblick zu behalten und einen klaren Leitfaden zu haben, habe ich mit GitHub Projects gearbeitet. Durch ein strukturiertes Projektmanagement konnte ich die einzelnen Ziele in Form von Meilensteinen definieren. Dies ermöglichte mir jederzeit einen klaren Überblick darüber, welche Ziele bereits erreicht wurden und welche noch offenstanden.

Das Projektmanagement kann hier nochmals eingesehen werden:
- Projektmanagement:
  <a href="https://github.com/users/Radball-Migi/projects/6/views/4" target="_blank">Roadmap · HF ITCNE24 - 3. Semarbeit MSVC - Projectplan</a>

- Licensetool release:
  <a href="https://github.com/users/Radball-Migi/projects/7/views/1" target="_blank">HF ITCNE24 - 3. Semarbeit MSVC - License Tool Release</a>


