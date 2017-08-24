from modules import stringUtils, jsonUtils
import re, os
import xbmc, xbmcaddon

ADDON_ID = 'plugin.video.osmosix'
REAL_SETTINGS = xbmcaddon.Addon(id=ADDON_ID)
profile = xbmc.translatePath(REAL_SETTINGS.getAddonInfo('profile').decode('utf-8'))

def create(strm_name, url, media_type):
    return update(strm_name, url, media_type, None)

def update(strm_name, url, media_type, thelist):
    if url.find("action=playVod") > 0:
        return url + "&playMode=play"
    return url
