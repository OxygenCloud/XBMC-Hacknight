"""
    Document   : gpodlib.py
    Package    : GPodder Integration to XBMC
    Author     : Ashley Kitson
    Copyright  : 2010, Ashley Kitson, UK

               : gPodder - A media aggregator and podcast client
    Copyright  : 2005-2010 Thomas Perl and the gPodder Team

    License    : Gnu General Public License - see LICENSE.TXT
    Description: GPodder api.  Based on gpo.py by Thomas Perl / gPodder Team
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

import sys
import os
import inspect

#TODO set path dynamically
sys.path.append(os.path.join('/','usr','lib','python2.6','site-packages'))
sys.path.append(os.path.join('/','usr','lib64','python2.6'))
sys.path.append(os.path.join('/','usr','lib64','python2.6','lib-dynload'))


import gpodder
#gettext functionality
_ = gpodder.gettext
#Only use the published API
from gpodder import api

class gPodderCli(object):
    def __init__(self):
        self.client = api.PodcastClient()

    def subscribe(self, url, title=None):
        if self.client.get_podcast(url) is not None:
            self._info(_('You are already subscribed to %s.' % url))
            return True

        if self.client.create_podcast(url, title) is None:
            self._error(_('Cannot download feed for %s.') % url)
            return True

        self.client.finish()

        self._info(_('Successfully added %s.' % url))
        return True

    def rename(self, url, title):
        podcast = self.client.get_podcast(url)

        if podcast is None:
            self._error(_('You are not subscribed to %s.') % url)
        else:
            old_title = podcast.title
            podcast.rename(title)
            self.client.finish()
            self._info(_('Renamed %s to %s.') % (old_title, title))

        return True

    def unsubscribe(self, url):
        podcast = self.client.get_podcast(url)

        if podcast is None:
            self._error(_('You are not subscribed to %s.') % url)
        else:
            podcast.delete()
            self.client.finish()
            self._error(_('Unsubscribed from %s.') % url)

        return True

    def info(self, url):
        podcast = self.client.get_podcast(url)

        if podcast is None:
            self._error(_('You are not subscribed to %s.') % url)
        else:
            title, url = podcast.title, podcast.url
            def status_str(episode):
                if episode.is_new:
                    return ' * '
                if episode.is_downloaded:
                    return ' ▉ '
                if episode.is_deleted:
                    return ' ░ '

                return '   '

            episodes = ('%3d. %s %s' % (i+1, status_str(e), e.title) for i, e in enumerate(podcast.get_episodes()))
            episodes = '\n      '.join(episodes)
            print >>sys.stdout, """
    Title: %(title)s
    URL: %(url)s

    Episodes:
      %(episodes)s
""" % locals()

        return True

    def list(self):
        for podcast in self.client.get_podcasts():
            print podcast.url

        return True

    def update(self):
        for podcast in self.client.get_podcasts():
            print 'Updating', podcast.title
            podcast.update()
        print 'Done.'

        return True

    def pending(self):
        count = 0
        for podcast in self.client.get_podcasts():
            podcast_printed = False
            for episode in podcast.get_episodes():
                if episode.is_new:
                    if not podcast_printed:
                        print podcast.title
                        podcast_printed = True
                    print '   ', episode.title
                    count += 1

        print count, 'episodes pending.'
        return True

    def download(self):
        count = 0
        for podcast in self.client.get_podcasts():
            podcast_printed = False
            for episode in podcast.get_episodes():
                if episode.is_new:
                    if not podcast_printed:
                        print podcast.title
                        podcast_printed = True
                    print '   ', episode.title
                    episode.download()
                    count += 1

        print count, 'episodes downloaded.'
        return True

    def sync(self):
        self.client.synchronize_device()
        return True

    # -------------------------------------------------------------------

    def _error(self, *args):
        print >>sys.stderr, ' '.join(args)

    def _info(self, *args):
        print >>sys.stdout, ' '.join(args)

    def _checkargs(self, func, command_line):
        args, varargs, keywords, defaults = inspect.getargspec(func)
        args.pop(0) # Remove "self" from args
        defaults = defaults or ()
        minarg, maxarg = len(args)-len(defaults), len(args)

        if len(command_line) < minarg or len(command_line) > maxarg:
            self._error('Wrong argument count for %s.' % func.__name__)
            return False

        return func(*command_line)


    def _parse(self, command_line):
        if not command_line:
            return False

        command = command_line.pop(0)
        if command.startswith('_'):
            self._error(_('This command is not available.'))
            return False

        for name, func in inspect.getmembers(self):
            if inspect.ismethod(func) and name == command:
                return self._checkargs(func, command_line)

        return False

