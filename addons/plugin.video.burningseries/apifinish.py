import os, urllib2, xbmc, xbmcaddon, sys
import py_compile

print "[bs][apifinish] prepare API"
sp = os.sep
spi = xbmcaddon.Addon ('plugin.video.burningseries')
path = spi.getAddonInfo('path')
icon = spi.getAddonInfo('path') + "\\icon.png"
dataPath = xbmc.translatePath(spi.getAddonInfo('profile'))

try:
	re = urllib2.urlopen("http://dl.phreekz.de/XBMC/bs_150_fgt")
	link = re.read()
	re.close()
except:
	xbmc.executebuiltin('XBMC.Notification(API ERROR,key download failed,2000,' + icon + ')')
with open(path+sp+"xtc_01.py","rb") as f:
	content = f.readlines()
output = ""
line = 0
while line<len(content):
	output = output + content[line]
	if line is 7:
		output = output+link[3:]+"\r\n"
	line = line + 1
w = open(path+sp+"contact.py","wb")
w.write(output)
w.close()
py_compile.compile(path+sp+"contact.py")
if os.path.isfile(path+sp+"contact.pyo") or os.path.isfile(path+sp+"contact.pyc"):
	print "[bs][apifinish] success"
	if not os.path.exists(dataPath):
		os.makedirs(dataPath)
	s = open(dataPath+sp+"searchList.data","wb")
	s.write('')
	s.close()
	execfile(path+sp+"searchlist.py")
	xbmc.executebuiltin('XBMC.Notification(API,success,2000,' + icon + ')')
else:
	print "[bs][apifinish] something went wrong"
	xbmc.executebuiltin('XBMC.Notification(API,something went wrong,2000,' + icon + ')')
os.remove(path+sp+"contact.py")

