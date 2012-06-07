"""
    Document   : xbmc_gpodder.py
    Package    : GPodder Integration to XBMC
    Author     : Ashley Kitson
    Copyright  : 2010, Ashley Kitson, UK
    License    : Gnu General Public License - see LICENSE.TXT
    Description: Worker class library
"""
"""
This file is part of "The GPodder Integration to XBMC"

    "The GPodder Integration to XBMC" is free software: you can redistribute
    it and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of the License,
    or (at your option) any later version.

    "The GPodder Integration to XBMC" is distributed in the hope that it will
    be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "The GPodder Integration to XBMC".
    If not, see <http://www.gnu.org/licenses/>.

"""
#make xbmc and system modules available
import os
import subprocess
import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui
import dircache
import fnmatch
import re
#from gpodlib import gPodderCli as gpoapi

#define global constants for settings xml tags
__GPOPATH_TAG__ = 'gpoPath'
__GPOUPDT_TAG__ = 'gpoUpdate'

#define global constant for gpodder folder image
__FOLDER_IMG__ = 'folder.jpg'

#pattern to find video files
__PATT_VIDEO__ = "\.(m4v|mp4)$"

#Playlist file suffix
__PLAYLIST__ = '.m3u'

#Addon Title for dialogs
__TITLE__ = 'GPodder-XBMC'

class context(xbmcaddon.Addon):
    """
    Hack to get current context that addon is running in
    #TODO XBMC Trac 10170 - ticket raised to get it into API
    
    @usage      context = context().getContext()
    @thanks amet - xbmc.org
    @link http://wiki.xbmc.org/index.php?title=Window_IDs
    """
    # Set up window Ids for the various contexts
    _ctxt_audio = (10005,10500,10501,10502)
    _ctxt_video = (10006,10024,10025,10028)
    _ctxt_image = (10002)
    _ctxt_executable = (10001,10020)
    # current  window id
    _currId = 0;

    def __init__(self, pluginName):
        xbmcaddon.Addon.__init__(pluginName)
        self._currId = xbmcgui.getCurrentWindowId();

    def getContext(self):
        """
        Returns the current system context
        @return string ('audio','video','image','executable','unknown')
        """
        if self._currId in self._ctxt_audio:
            return 'audio'
        elif self._currId in self._ctxt_video:
            return 'video'
        elif self._currId in self._ctxt_image:
            return 'image'
        elif self._currId in self._ctxt_executable:
            return 'executable'
        else:
            return 'unknown'

#define classes
class housekeeper:
    """
    Run any startup required for the addon
    """
    #
    # PRIVATE Methods
    #

    # current instance of plugin identifer
    _pluginId = 0
    # plugin name
    _pluginName = ''
    #xbmc addon class
    _xbmcaddon = None

    def __init__(self, pluginId, pluginName):
        """
        constructor
        @parm int pluginId - Current instance of plugin identifer
        @param string pluginName - Name of plugin calling us
        """
        self._pluginId = pluginId
        self._pluginName = pluginName
        self._xbmcaddon = context(pluginName)

    def start(self):
        """
        Run the startup
        """
        p = subprocess.Popen(('python','/usr/bin/gpo','update'),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT).stdout
        #p = subprocess.Popen(('python','/home/akddh732/.xbmc/addons/plugin.audio.gpodder-xbmc/test.py'),
        #        stdout=subprocess.PIPE,
        #        stderr=subprocess.STDOUT).stdout
        #p.wait()
        print '--------------------------------'
        print p.readlines()
        print '--------------------------------'
        
        """
        doUpdate = xbmcplugin.getSetting(self._pluginId,__GPOUPDT_TAG__) == "true"
        if doUpdate:
            #print "**************************** 1"
            #ret = os.popen("/usr/bin/gpo update")
            #print ret.readlines()

            #print "run update "
            #print ret
            #print "**************************** 2"
            #ret = os.popen('gpo download').read()


            #print "run download " + ret
            pass
        """
        pass
    
    def end(self):
        """
        Run the end processes
        """
        pass

class creator:
    """
    Responsible for creating the list of items that will get displayed
    """
    #
    # PRIVATE Methods
    #

    # current instance of plugin identifer
    _pluginId = 0
    # plugin name
    _pluginName = ''
    #xbmc addon class
    _xbmcaddon = None
    #context
    _context = 'unknown'

    def __init__(self, pluginId, pluginName):
        """
        constructor
        @parm int pluginId - Current instance of plugin identifer
        @param string pluginName - Name of plugin calling us
        """
        self._pluginId = pluginId
        self._pluginName = pluginName
        self._xbmcaddon = context(pluginName)
        self._context = self._xbmcaddon.getContext()

    def _createListAll(self, dirContent, dir):
        """
        Create the dynamic list of all content
        @param list dirContent - list of __PLAYLIST__ files in gpodder directory
        @param string dir - gpodder directory location
        @access private
        @return list
        """

        #create listing
        listing = []
        for file in dirContent:
            uri = xbmc.translatePath(dir + '/' + file)
            label = file.replace(__PLAYLIST__,'')
            img = xbmc.translatePath(dir + '/' + __FOLDER_IMG__)
            listing.append([label,uri,img])

        return listing

    def _createListVideo(self, dirContent, dir):
        """
        Create a list of video only content
        @param list dirContent - list of __PLAYLIST__ files in gpodder directory
        @param string dir - gpodder directory location
        @access private
        @return list
        """
        #for each __PLAYLIST__ file determine what the contents are
        # if contain video files then use else discard
        Content = []
        for fName in dirContent:
            fileName = xbmc.translatePath(dir + '/' + fName)
            content = [line.strip() for line in file(fileName) if not line.startswith('#')]
            flag = False
            for f in content:
                if re.search(__PATT_VIDEO__,f) != None:
                    flag = True
                    break
            if flag:
                Content.append(fName)

        return self._createListAll(Content, dir)


    def _createListAudio(self, dirContent, dir):
        """
        Create a list of audio only content
        @param list dirContent - list of __PLAYLIST__ files in gpodder directory
        @param string dir - gpodder directory location
        @access private
        @return list
        """
        #for each __PLAYLIST__ file determine what the contents are
        # if contain music files (i.e. doesn't contain video) files then use else discard
        Content = []
        for fName in dirContent:
            fileName = xbmc.translatePath(dir + '/' + fName)
            content = [line.strip() for line in file(fileName) if not line.startswith('#')]
            flag = False
            for f in content:
                if re.search(__PATT_VIDEO__,f) == None:
                    flag = True
                    break
            if flag:
                Content.append(fName)
                
        return self._createListAll(Content, dir)


    #
    # PUBLIC API
    #

    def get(self):
        """
        Refresh and retrieve the current list for display
        @access public
        @returns list
        @usage      c=example2.creator()
                    list = c.get()
        """
        
        #get the user setting for the gpodder directory
        dir = xbmcplugin.getSetting(self._pluginId,__GPOPATH_TAG__)
        #see if path contains '~' and replace with user home directory
        #TODO Does this work in Windows/Mac?
        if re.match('~',dir) != None:
            dir = dir.replace('~',os.getenv('HOME'))

        #we try the next bit but if user home dir isn't set then exit with
        # a message and exit
        try:
            #get contents of gpodder directory
            dirContent = dircache.listdir(dir)
        except:
            xbmcgui.Dialog().ok(
                __TITLE__,
                self._xbmcaddon.getLocalizedString(30300)
            )
            return []

        #parse contents for all .m3u files
        dirContent = fnmatch.filter(dirContent, '*' + __PLAYLIST__)

        #get the relevent list
        if self._context == 'audio':
            return self._createListAudio(dirContent, dir)
        elif self._context == 'video':
            return self._createListVideo(dirContent, dir)
        else:
            return self._createListAll(dirContent, dir)

class sender:
    """
    Responsible for sending output to XBMC
    """
    # current instance of plugin identifer
    _pluginId = 0
 
    def __init__(self, pluginId):
        """
        constructor
        @parm int pluginId - current instance of plugin identifer
        """
        self._pluginId = pluginId


    def send(self,listing):
        """
        Send output to XBMC
        @param list listing - the list of items to display
        @return void
        """
        #create listing items
        # item[0] = list label
        # item[1] = item uri
        # item[2] = image uri
        for item in listing:
            listItem = xbmcgui.ListItem(
                item[0],
                iconImage=item[2],
                thumbnailImage=item[2]
            )
            xbmcplugin.addDirectoryItem(self._pluginId,item[1],listItem)
