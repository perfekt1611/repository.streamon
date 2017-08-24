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
print "[bs]import started"
if not os.path.exists(dataUrlpath):								#wenn nicht orginalpfad existiert
	os.makedirs(dataUrlpath)									#mach den pfad
if not os.path.exists(watchedFile):								#wenn nicht watched.data existiert
	if os.path.exists(oldWatchedPath+SEP+"watched.data"):		#wenn neue watched.data existiert
		print "[bs]import copy data to:"
		print watchedFile
		shutil.copy(oldWatchedPath+SEP+"watched.data",watchedFile)			#kopiere neue watched.data nach orginalpfad
		xbmc.executebuiltin('XBMC.Notification([BS],erfolgreich importiert,2000,' + icon + ')')
	else:
		print "[bs][watched] creating:"
		print watchedFile
		file = open(watchedFile, 'w+')
else:
	yesnowindow = xbmcgui.Dialog().yesno("Import watched.data","watched.data überschreiben?")
	if yesnowindow:
		shutil.copy(oldWatchedPath+SEP+"watched.data",watchedFile)			#kopiere neue watched.data nach orginalpfad
		xbmc.executebuiltin('XBMC.Notification([BS],erfolgreich importiert,2000,' + icon + ')')
	else:
		xbmc.executebuiltin('XBMC.Notification([BS],importieren abgebrochen,2000,' + icon + ')')