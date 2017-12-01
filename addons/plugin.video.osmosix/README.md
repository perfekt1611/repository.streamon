# plugin.video.osmosix
Kodi add-on to add streams to library

This Version is only for use with a MySQL-Database-Server.
It will not work with the Kodi SQL-Video-Database.

For use with this Version you need a 
"advancedsettings.xml"

<videolibrary>
  <importwatchedstate>true</importwatchedstate>
  <importresumepoint>true</importresumepoint>
</videolibrary>

Info´s here:
http://kodi.wiki/view/advancedsettings.xml

Forum:
https://www.kodinerds.net/index.php/Thread/53307-Beta-osmosis-Streams-zur-DB-hinzuf%C3%BCgen/

Wenn man Musik neu hinzufügen will, muss man so vorgehen:
1. Hinzufügen der Musik durch Osmosis
2. Hinzufügen des Ordners zur Musikkategorie (falls noch nicht vorhanden)
3. Manuelles Scannen der Bibliothek -> Musik fliegt wieder aus der Bibliothek
4. Update der Musik durch Osmosis -> Musik bleibt ab sofort erhalten
