import os
import sys


import xbmcgui
import xbmcplugin


PLUGIN_ID = "plugin.video.oxygencloud"

#pluginUrl = sys.argv[0]
pluginId = int(sys.argv[1])
#itemId = sys.argv[2].lstrip("?")
#addon = xa.Addon(PLUGIN_ID)

# try:
#     
#     else:
#         populateDir(pluginUrl, pluginId, putio.getRootListing())
# except PutioAuthFailureException, e:
#     xbmc.executebuiltin("XBMC.Notification(%s, %s, %d, %s)" % (
#         e.header,
#         e.message,
#         e.duration,
#         os.path.join(addon.getAddonInfo("path"), "resources", "images", "error.png")
#     ))

def createListing():
    listing = []
    listing.append('Doctor.Who.2005.6x13.The.Wedding.Of.River.Song.HDTV.XviD-FoV.avi')
    listing.append('20120606173915.txt')
    listing.append('The Thrid')
    return listing
    
def sendToXbmc(listing):
    global pluginId
    
    for item in listing:
        listItem = xbmcgui.ListItem(item)
        xbmcplugin.addDirectoryItem(pluginId,'https://i-7b3c1b1d.oxygencloud.com/storagegateway/download?c=c1a6571f-ea0a-4abb-b9c8-102189b0c3eb&s=120d863eb6d37764770ecb425a632accd1bc39e1&h=52a2f7689b26fc2a5bd27082a20a7f085e91e857',listItem)
        
    xbmcplugin.endOfDirectory(pluginId)
    
sendToXbmc(createListing())