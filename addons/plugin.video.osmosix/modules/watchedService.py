# Copyright (C) 2016 stereodruid(J.G.) Mail: stereodruid@gmail.com
#
#
# This file is part of osmosix
#
# osmosix is free software: you can redistribute it. 
# You can modify it for private use only.
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# osmosix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

class Service(xbmc.Player):
    def __init__(self, *args, **kwargs):
        xbmc.Player.__init__(self, *args, **kwargs)
        self.reset()
  
        self.last_run = 0
        self.DB = ''
        xbmc.log('PrimeWire: Service starting...')
  
  
    def reset(self):
        xbmc.log('PrimeWire: Service: Resetting...')
        win = xbmcgui.Window(10000)
        win.clearProperty('1ch.playing.title')
        win.clearProperty('1ch.playing.year')
        win.clearProperty('1ch.playing.imdb')
        win.clearProperty('1ch.playing.season')
        win.clearProperty('1ch.playing.episode')
  
        self._totalTime = 999999
        self._lastPos = 0
        self._sought = False
        self.tracking = False
        self.video_type = ''
        self.win = xbmcgui.Window(10000)
        self.win.setProperty('1ch.playing', '')
        self.meta = ''
  
  
    def onPlayBackStarted(self):
        xbmc.log('PrimeWire: Service: Playback started')
        meta = self.win.getProperty('1ch.playing')
        if meta: #Playback is ours
            xbmc.log('PrimeWire: Service: tracking progress...')
            self.tracking = True
            self.meta = json.loads(meta)
            self.video_type = 'tvshow' if 'episode' in self.meta else 'movie'
            self._totalTime = self.getTotalTime()
            sql_stub = 'SELECT bookmark FROM bookmarks WHERE video_type=? AND title=?'
            if   self.video_type == 'tvshow': sql_stub += ' AND season=? AND episode=?'
            elif self.video_type == 'movie':  sql_stub += ' AND year=?'
            if DB == 'mysql':
                sql_stub = sql_stub.replace('?', '%s')
                db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
            else:
                db = database.connect(db_dir)
            cur = db.cursor()
            if not 'year'    in self.meta: self.meta['year']    = None
            if not 'imdb'    in self.meta: self.meta['imdb']    = None
            if not 'season'  in self.meta: self.meta['season']  = None
            if not 'episode' in self.meta: self.meta['episode'] = None
            bmark_title = self.meta['title'] if self.video_type == 'movie' else self.meta['TVShowTitle']
            if self.video_type == 'tvshow':
                cur.execute(sql_stub, (self.video_type, bmark_title, self.meta['season'], self.meta['episode']))
            elif self.video_type == 'movie':
                cur.execute(sql_stub, (self.video_type, bmark_title, self.meta['year']))
            bookmark = cur.fetchone()
            db.close()
  
            if bookmark and self.use_custom_resume():
                bookmark = float(bookmark[0])
                if not (self._sought and bookmark):
                    question = 'Resume %s from %s?' % (bmark_title, format_time(bookmark))
                    ln2 = '' if self.video_type == 'movie' else 'Season %s Episode %s' %(self.meta['season'], self.meta['episode'])
                    resume = xbmcgui.Dialog()
                    resume = resume.yesno(bmark_title, '', question, ln2, 'Start from beginning', 'Resume')
                    if resume: self.seekTime(bookmark)
                    self._sought = True
  
    def onPlayBackStopped(self):
        xbmc.log('PrimeWire: Playback Stopped')
        #Is the item from our addon?
        if xbmc.getInfoLabel('Container.FolderPath').startswith(sys.argv[0]):
            playedTime = int(self._lastPos)
            watched_values = [.7, .8, .9]
            min_watched_percent = watched_values[int(ADDON.getSetting('watched-percent'))]
            percent = int((playedTime / self._totalTime) * 100)
            pTime = format_time(playedTime)
            tTime = format_time(self._totalTime)
            xbmc.log('PrimeWire: Service: %s played of %s total = %s%%' % (pTime, tTime, percent))

            bmark_title = self.meta['title'] if self.video_type == 'movie' else self.meta['TVShowTitle']
            videotype = 'movie' if self.video_type == 'movie' else 'episode'
            if playedTime == 0 and self._totalTime == 999999:
                raise RuntimeError('XBMC silently failed to start playback')
            elif ((playedTime / self._totalTime) > min_watched_percent) and (
                        self.video_type == 'movie' or (self.meta['season'] and self.meta['episode'])):
                xbmc.log('PrimeWire: Service: Threshold met. Marking item as watched')
                if xbmc.getInfoLabel('ListItem.FileName').endswith('.strm'):
                    if videotype == 'episode':
                        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"episodeid": %s, "properties": ["playcount"]}, "id": 1}'
                        cmd = cmd %(xbmc.getInfoLabel('ListItem.DBID'))
                        result = json.loads(xbmc.executeJSONRPC(cmd))
                        print (result)
                        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid": %s, "playcount": %s}, "id": 1}'
                        playcount = int(result['result']['episodedetails']['playcount']) + 1
                        cmd = cmd %(xbmc.getInfoLabel('ListItem.DBID'), playcount)
                        result = xbmc.executeJSONRPC(cmd)
                        xbmc.log('PrimeWire: Marking .strm as watched: %s' %result)
                    if videotype == 'movie':
                        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"movieid": %s, "properties": ["playcount"]}, "id": 1}'
                        cmd = cmd %(xbmc.getInfoLabel('ListItem.DBID'))
                        result = json.loads(xbmc.executeJSONRPC(cmd))
                        print (result)
                        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid": %s, "playcount": %s}, "id": 1}'
                        playcount = int(result['result']['moviedetails']['playcount']) + 1
                        cmd = cmd %(xbmc.getInfoLabel('ListItem.DBID'), playcount)
                        result = xbmc.executeJSONRPC(cmd)
                        xbmc.log('PrimeWire: Marking .strm as watched: %s' %result)
                ChangeWatched(self.meta['imdb'], videotype, bmark_title, self.meta['season'], self.meta['episode'], self.meta['year'], watched=7)
                sql = 'DELETE FROM bookmarks WHERE video_type=? AND title=? AND season=? AND episode=? AND year=?'
                if DB == 'mysql':
                    sql = sql.replace('?', '%s')
                    db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
                else:
                    db = database.connect(db_dir)
                cur = db.cursor()
                cur.execute(sql, (self.video_type, self.meta['title'], self.meta['season'], self.meta['episode'], self.meta['year']))
                db.commit()
                db.close()
            else:
                xbmc.log('PrimeWire: Service: Threshold not met. Saving bookmark')
                sql = 'REPLACE INTO bookmarks (video_type, title, season, episode, year, bookmark) VALUES(?,?,?,?,?,?)'
                if DB == 'mysql':
                    sql = sql.replace('?', '%s')
                    db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
                else:
                    sql = 'INSERT or ' + sql
                    db = database.connect(db_dir)
                cur = db.cursor()
                cur.execute(sql, (self.video_type, bmark_title, self.meta['season'],
                                  self.meta['episode'], self.meta['year'], playedTime))
                db.commit()
                db.close()
                if xbmc.getInfoLabel('ListItem.FileName').endswith('.strm'):
                    if videotype == 'episode':
                        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid": %s, "resume": {"position": %s}}, "id": 1}'
                        cmd = cmd %(xbmc.getInfoLabel('ListItem.DBID'), playedTime)
                        result = xbmc.executeJSONRPC(cmd)
                        xbmc.log('PrimeWire: Saving Bookmark for strm file: %s' %result)
                    if videotype == 'movie':
                        cmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetMovieDetails", "params": {"movieid": %s, "resume": {"position": %s}}, "id": 1}'
                        cmd = cmd %(xbmc.getInfoLabel('ListItem.DBID'), playedTime)
                        result = xbmc.executeJSONRPC(cmd)
                        xbmc.log('PrimeWire: Saving Bookmark for strm file: %s' %result)
        self.reset()
  
    def onPlayBackEnded(self):
        xbmc.log('PrimeWire: Playback completed')
        self.onPlayBackStopped()
  
    def use_custom_resume(self):
        xbmc_version = xbmc.getInfoLabel("System.BuildVersion")
        is_gotham = int(xbmc_version[:2]) >= 13 #e.g. "13.0-ALPHA11 Git:20131231-8eb49b3"
        if (not is_gotham) and xbmc.getInfoLabel('ListItem.FileName').endswith('.strm'):
            return True
        if (ADDON.getSetting('use-dialogs') == 'false'):
            return True
        return False