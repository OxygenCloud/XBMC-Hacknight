import os
import sys


import xbmcgui
import xbmcplugin


PLUGIN_ID = "plugin.video.oxygencloud"

pluginId = int(sys.argv[1])

def createListing():
    cwd = os.getcwd
    os.system ('%d/java -jar runtime.jar' % cwd)
    listing = []
    listing.append('Video')
    return listing
    
def sendToXbmc(listing):
    global pluginId
    
    for item in listing:
        listItem = xbmcgui.ListItem(item)
        xbmcplugin.addDirectoryItem(pluginId,'~/.nancy/',listItem,True)
        
    xbmcplugin.endOfDirectory(pluginId)
    
sendToXbmc(createListing())
