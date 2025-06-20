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

MSVC steht für **M**icro **S**ervices ...

### Was ist Flask API?

Flask API ist ein MSVC Dienst, mit dem man Eine API schreiben kann, welche dann verwendet werden kann. 



## Umsetzung (Improve)

Wie in den vorherigen Schritten beschrieben, möchte ich einen Microservice erstellen, welcher von diversen Tenants den aktuellen Lizenzstand abfragt und im Falle dass keine Lizenz mehr übrig ist, sollte der Supporttechniker informiert werden, damit der Bestellprozess gestartet werden kann. 

Eine Umsetzung ist mir gelungen, wie ich Sie beschrieben habe. 
Als Endprodukt habe ich einen Microservice, welcher mittels FlaskAPI und dessen Templates ein Frontend anzeigen. Zusätzlich habe ich eine Integration im SharePoint, in der ich die Daten aus der Abfrage, in eine SharePoint Liste schreibe. Wenn die freien Lizenzen bei 0 stehen, dann wird mittels PowerAutomate ein Flow gestartet, welcher dies dem Supporttechniker meldet. 

Das *Know-how* habe ich mir durch meine aktive Teilnahme am MSVC-Unterricht bei Boris Langert sowie durch die YouTube-Tutorials:  <a href="https://www.youtube.com/watch?v=QXeEoD0pB3E&list=PLsyeobzWxl7poL9JTVyndKe62ieoN-MZ3" target="_blank">Python for Beginners | Telusko</a> von <a href="[#0 Python for Beginners | Programming Tutorial](https://www.youtube.com/@Telusko)" target="_blank">Telusko</a>. 

Zu beginn habe ich mit der App begonnen, dort habe ich mit der Vorlage aus dem Unterricht begonnen und auf dieser Aufgebaut. 
Die Struktur war schlicht und nur gerade das nötigste. 