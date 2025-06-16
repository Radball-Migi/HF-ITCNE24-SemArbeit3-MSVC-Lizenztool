---
layout: default
title: 3.1 Definieren
parent: 3. Hauptteil
nav_order: 4
---
# Definieren (Define) Phase

Die Define-Phase ist der erste Schritt in einem Six Sigma Projekt. In dieser Phase wird das Projekt klar definiert, um sicherzustellen, dass alle Beteiligten ein gemeinsames Verständnis der Ziele und des Umfangs haben. Ein wesentlicher Bestandteil dieser Phase ist die Identifizierung und Beschreibung des zu lösenden Problems oder der zu verbessernden Prozesse.

![Define](../../ressources/images/define.png)

[Quelle](../Quellverzeichnis/index.md#define-phase)

## Zielvorstellung

Am Ende der Semesterarbeit soll ein praxistaugliches Tool für die ISE AG entstehen, das eine automatisierte und zentralisierte Lizenzüberwachung ermöglicht. Kern des Systems ist ein Microservice, der regelmäßig Lizenzinformationen aus vordefinierten Microsoft 365 Tenants über die Microsoft Graph API abruft. Die erfassten Daten werden strukturiert in einer SharePoint Online Liste gespeichert, um nahtlos in bestehende Workflows der ISE AG integrierbar zu sein.

Auf dieser Basis können anschliessend automatisierte Prozesse – insbesondere über Power Automate – eingerichtet werden, die bei kritischen Lizenzständen Benachrichtigungen auslösen und so ein frühzeitiges Handeln ermöglichen. Das Tool soll sowohl intern nutzbar als auch erweiterbar sein und einen nachhaltigen Mehrwert für den operativen Betrieb im Lizenzmanagement schaffen.

## Ressourceneinsatz 

Für die Umsetzung der Semesterarbeit stehen folgende Ressourcen zur Verfügung:

- **Microsoft 365 Test-Tenant**  
  Zugriff auf Lizenzdaten über die Microsoft Graph API.

- **SharePoint Online**  
  Speicherung der abgerufenen Lizenzinformationen.

- **Flask Microservice (Docker-basiert)**  
  Lokale Entwicklung und Ausführung in isolierter Umgebung.

- **Visual Studio Code & GitHub**  
  Entwicklung, Quellcodeverwaltung und Dokumentation.

- **Power Automate**  
  Automatisierte Benachrichtigungen bei kritischen Lizenzständen.



## Warum wird die Zielvorstellung aktuell nicht erreicht?

Die bisherige Lizenzüberwachung erfolgt manuell und reaktiv. Probleme werden meist erst erkannt, wenn bereits Störungen beim Kunden auftreten. Ein automatisiertes und proaktives Monitoring ist mit den bestehenden Mitteln nicht möglich.

Um die angestrebte Zielvorstellung zu erreichen, müssen folgende neue technische Komponenten entwickelt werden:

- Ein **Microservice**, der Lizenzdaten automatisiert über die Microsoft Graph API abruft.
- Eine **strukturierte SharePoint-Liste** zur zentralen und weiterverarbeitbaren Speicherung der Daten.
- Ein **Power Automate-Flow**, der bei kritischen Lizenzständen automatische Benachrichtigungen versendet.

Diese Komponenten sind erforderlich, da bestehende Tools die benötigten Funktionen nicht vollständig und integriert bereitstellen. Ziel ist es, unseren Kunden eine gleichbleibend hohe Qualität zu gewährleisten und Betriebsunterbrechungen auf ein Minimum zu reduzieren.

