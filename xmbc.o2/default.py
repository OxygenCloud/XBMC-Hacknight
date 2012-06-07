import os
import sys

import xbmc
import xbmcaddon as xa

from resources.lib.exceptions import *
from resources.lib.gui import *

PLUGIN_ID = "plugin.video.oxygencloud"

pluginUrl = sys.argv[0]
pluginId = int(sys.argv[1])
itemId = sys.argv[2].lstrip("?")
addon = xa.Addon(PLUGIN_ID)

try:
    
    else:
        populateDir(pluginUrl, pluginId, putio.getRootListing())
except PutioAuthFailureException, e:
    xbmc.executebuiltin("XBMC.Notification(%s, %s, %d, %s)" % (
        e.header,
        e.message,
        e.duration,
        os.path.join(addon.getAddonInfo("path"), "resources", "images", "error.png")
    ))