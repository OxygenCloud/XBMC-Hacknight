You've seen the license, now read this

This addon is produced as a helpful item for people wishing to integrate their
gPodder system with XBMC

What we can do now
------------------

- Display podcasts in the relevant sections of XBMC, i.e video podcasts in
Video, audio in Music
- Run gPodder on your xbmc box and on some other machine to connect to to xbmc
box as its source folder - this means you can have a central podcast repository.
I do just that, running several machines off of one source
- Use gPodder to control your subscriptions etc.
- run the CLI version (outside of XBMC) to run a cron job to automatically
update your subscriptions

What we can't do now
--------------------

Integrate gPodder update and download functionality into XBMC
- why? - because XBMC is stuck at version 2.4 of Python. gPodder runs on
version 2.6 and has a number of dependencies on it.  Until that is resolved it
is not possible to utilise the gPodder API to do for instance;
- manage subscriptions
- manage episodes
- runs updates
- and so on

Under current development plans, even if xbmc does run under 2.6 of Python it
will be effectively sandboxed and not able to reach other systems such as
gPodder

What you can do next
--------------------

- lobby XBMC to let the system run under the default install of Python
- or lobby XBMC to get them to ensure that the system can access other Python
scripts within the same release level of Python
- report back via the issue tracker any problems you have running this
minimalist addon so that it can be developed

If you have installed gPodder on a Linux system you can follow the instruction
at http://forum.xbmc.org/showthread.php?t=80476 to automate your gPodder
updates.

If you figure out how to do it on other systems, please add to that forum thread
so I can include it in the general documentation

Caveat
------
I'm a Linux developer, have been for over 10 years, (First commercial operating
system was CTOS - 25 years ago - don't ask!.) I don't/can't run Microsoft
systems.  Nor do I have much experience with the Mac OS except for hacking it
(it's only Unix after all, I have an iPhone duh.)  If you have problems on
Windoze or Mac, please do report them, but try to provide a fix or a lead as
well. The more info you give the better chance I have at least of phrasing the
right question to those xbmc devs who do understand those platforms.

For the inquisitive, you can see the code that runs this addon in your
.xbmc/addons/plugin.audio.gpodder-xbmc directory.  It does contain some code
in the resources/lib dir that is waiting for xbmc to get to 2.6 Python!

Kind regards
Ashley Kitson (chippyash at XBMC forums)

Downloads:
Zip: http://http://code.google.com/p/xbmc-gpodder-integration/downloads/list
Xbmc: via XBMC addons

SVN: Please apply via http://code.google.com/p/xbmc-gpodder-integration/
if you want to get involved. At this point, public svn access is disabled

Issues:
http://code.google.com/p/xbmc-gpodder-integration/issues/list

