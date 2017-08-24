# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, xbmcvfs
import os, sys, shutil

SEP = os.sep
addonInfo = xbmcaddon.Addon('plugin.video.burningseries')
dataUrlpath = xbmc.translatePath(addonInfo.getAddonInfo('profile'))
oldWatchedPath = addonInfo.getSetting('oldwatchedfile')
watchedFile = dataUrlpath+SEP+"watched.data"
icon = addonInfo.getAddonInfo('path') + "\\icon.png"

dataUrlpath,watchedFile,oldWatchedPath,SEP
print "[bs]export started"
if os.path.exists(watchedFile) and os.path.exists(oldWatchedPath):								#wenn watched.data existiert  und pfad vorhanden ist
	if not os.path.exists(oldWatchedPath+SEP+"watched.data"):		#wenn neue watched.data nicht existiert
		print "[bs]export migrating copy to:"
		print oldWatchedPath+SEP+"watched.data"
		shutil.copy(watchedFile,oldWatchedPath+SEP+"watched.data")			#kopiere watched.data nach neu
		xbmc.executebuiltin('XBMC.Notification([BS],erfolgreich exportiert,2000,' + icon + ')')
	else:
		yesnowindow = xbmcgui.Dialog().yesno("export watched.data","watched.data überschreiben?")
	if yesnowindow:
		shutil.copy(watchedFile,oldWatchedPath+SEP+"watched.data")			#kopiere neue watched.data nach orginalpfad
		xbmc.executebuiltin('XBMC.Notification([BS],erfolgreich exportiert,2000,' + icon + ')')
	else:
		xbmc.executebuiltin('XBMC.Notification([BS],exportieren abgebrochen,2000,' + icon + ')')
else:
	xbmc.executebuiltin('XBMC.Notification([BS],importieren abgebrochen: keine datei vorhanden,2000,' + icon + ')')