SickSubs Installation
===================

The SickSubs installation consists of three steps:

1. Download and configure SickSubs itself
2. Add SickSubs to the Sickbeard configuration as post-post-processing script
3. Add a crontab line for SickSubs

Each of these steps will be described below in detail. Before we proceed,
however, let's see what setup we assume for this guide:

- You have SickBeard successfully setup
- SickBeard performs your post-processing, e.g., something else (SABnzbd?) just
downloads the files to a dir from which SickBeard fetches new eps, renames them
and moves them to another location.
- Sickbeard runs under it's own user (called sickbeard)

Download and configure
----------------------
We should put SickSubs somewhere SickBeard can
execute it. Throughout this manual we'll be using /home/sickbeard/bin/sicksubs as
a default directory. To download SickSubs right from github we use git (so make
sure it's installed). The permissions should already be good, but make sure it's
executable by all. Something like 755 should be good, or use something more
paranoid if you want :)

```
sickbeard@box$ cd /home/sickbeard/bin/
sickbeard@box$ git clone git://github.com/Sakartu/sicksubs.git
```

Let's do a little test run to make sure everything is working correctly:

```
sickbeard@box$ cd /home/sickbeard/bin/sicksubs/
sickbeard@box$ ./test.py
.
----------------------------------------------------------------------
Ran 1 test in 15.270s

OK
```

Now we're ready to configure SickSubs itself. There are really only two
configuration parameters you need to worry about, they are the FULL CAPS
variables found at the top of SickSubs.py. You need to make sure the location you
specify for the database is either mkdir-able for the user running SickSubs.py or
make the required directories and files yourself. The database should be
writable for the SickBeard user. A sane location is
/home/sickbeard/.sicksubs/sicksub.db

All configuration parameters have sane defaults, but change them if you want.

Sickbeard
---------
Setting up for  SickBeard is a little tricky, mainly because you can't set it up
from the webinterface. First, make sure you shutdown SickBeard, otherwise it'll
reset the config file after you edited it. Then go to the place where you have
SickBeard.py installed and find the config.ini. Open it and change the line:

```
extra_scripts = ""
```

to

```
extra_scripts = /home/user/bin/sicksubs/SickSubs.py
```

where, ofcourse, the path is the path to the SickSubs.py file. Afterwards you can
restart SickBeard

crontab
-------
The final step in installing SickSubs is setting up a crontab to make sure your
subs are downloaded for you. Make sure you don't set the crontab to run too
often, otherwise the API key will get revoked making the app unusable for
everyone. A good default is to run it once every hour. To set this up, first
edit the crontab for user sickbeard:

```
sickbeard@box$ crontab -e
```

Then, in the editor that started, add the following line to the bottom:

```
0   *   *   *   *   /home/user/bin/SickSubs/SickSubs.py
```

This will run SickSubs every hour.

Happy subtitling!
