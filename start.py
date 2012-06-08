import os
import sys


import xbmcgui
import xbmcplugin
import xbmcaddon


PLUGIN_ID = "plugin.video.oxygencloud"

pluginId = int(sys.argv[1])
addon = xbmcaddon.Addon( id=PLUGIN_ID)
def createListing():

    cwd = addon.getAddonInfo('path')
    os.system ('java -jar %s/runtime.jar' % cwd)
    listing = []
    listing.append('Video')
    return listing
    
def sendToXbmc(listing):
    global pluginId
    home = os.getenv('USERPROFILE') or os.getenv('HOME')
    nancyDir = xbmc.translatePath(os.path.join(home, '.nancy'))
    for item in listing:
        listItem = xbmcgui.ListItem(item)
        xbmcplugin.addDirectoryItem(pluginId,nancyDir,listItem,True)
        
    xbmcplugin.endOfDirectory(pluginId)
    
sendToXbmc(createListing())
