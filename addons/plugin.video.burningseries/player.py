# -*- coding: utf-8 -*-
import xbmc, xbmcaddon
from watched import *

addon = xbmcaddon.Addon()
addonname = "[BS Player]"
icon = addon.getAddonInfo('path') + "\\icon.png"

class bsPlayer(xbmc.Player):
	def __init__( self, *args, **kwargs ):
		xbmc.Player.__init__( self )

	def playStream(self, url, n, season, episode):
		print "[bs][player.py] playStream"
		self.play(url)
		name = n.decode('utf-8')
		done = False
		if readWatchedData(name.encode('utf-8')+"/"+season+"/"+episode):
			done = True
		xbmc.sleep(15000)
		print "[bs][player.py] pause ende"
		while (not xbmc.abortRequested and self.isPlaying()):
			totalTime = self.getTotalTime()
			tRemain =  totalTime - self.getTime()
			#print "[bs][Player.py] tRemain =" + str(tRemain)
			#print "[bs][Player.py] totalTime =" + str(totalTime)
			if totalTime<60:
				relativeWatched = 5
			else:
				relativeWatched = 10
			if tRemain<(totalTime/100*relativeWatched) and not done:
				print "[bs][player.py] marked as watched :"+name.encode('utf-8')+"/"+season+"/"+episode
				writeWatchedData((name+"/"+season+"/"+episode).encode('utf-8'))
				xbmc.executebuiltin('XBMC.Notification([BS Player],marked as watched,3000,' + icon + ')')
				done = True
			xbmc.sleep(6000)

	def onPlayBackStarted(self):
		print "[bs][bsPlayer] PLAYBACK STARTED"
    
	def onPlayBackEnded(self):
		print "[bs][bsPlayer] PLAYBACK ENDED"

	def onPlayBackStopped(self):
		print "[bs][bsPlayer] PLAYBACK STOPPED"