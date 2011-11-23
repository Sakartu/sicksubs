SabSub Installation
===================

The SabSub installation consists of four steps:

1. Download and configure SabSub itself
2. Add SabSub to the SABnzbd configuration as post-processing script
3. Add SabSub to the Sickbeard configuration as post-post-processing script
4. Add a crontab line for SabSub

Each of these steps will be described below in detail. Before we proceed,
however, let's see what setup we assume for this guide:

- You have SABnzbd and SickBeard successfully setup, they both work and both
work together to download your shows.
- SickBeard performs your post-processing, e.g., SABnzbd just downloads the
files to a dir from which SickBeard fetches new eps, renames them and moves them
to another location.
- Both SABnzbd and SickBeard run under their own user.

Download and configure
----------------------
We should put SabSub somewhere where both SABnzbd *and* SickBeard can
execute it. Furthermore, SABnzbd wants to be able to write in the script
directory (God knows why), so the best place is probably in the SABnzbd
homedirectory. Throughout this manual we'll be using /home/sabnzbd/bin/sabsub as
a default directory. To download sabsub right from github we use git (so make
sure it's installed). The permissions should already be good, but make sure it's
executable by all. Something like 755 should be good, or use something more
paranoid if you want :)

```
user@box$ cd /home/sabnzbd/bin/
user@box$ git clone git://github.com/Sakartu/sabsub.git
```

Now we're ready to configure SabSub itself. There are really only two
configuration parameters you need to worry about, they are the FULL CAPS
variables found at the top of sabsub.py. You need to make sure the location you
specify for the database is either mkdir-able for the user running sabsub.py or
make the required directories and files yourself. The database should be
writable for both the SABnzbd user and the SickBeard user, so creating a group
where both users are in and setting the database permissions correctly is a good
idea:

```
user@box$ sudo addgroup showprocessors
user@box$ sudo adduser sickbeard showprocessors
user@box$ sudo adduser sabnzbd showprocessors
user@box$ cd /home/sickbeard/
user@box$ chmod g+w sabsub.db
```

SABnzbd
-------
In the main SABnzbd interface, go to:

```
Config -> Folders
```

and at the "Post-Processing Scripts Folder" setting, put the folder where SabSub
is located. This is probably something like "/home/sabnzbd/bin/sabsub" if you
checked out the github repo there.

Then, set the script as post-processing script as follows. Go to:

```
Config -> Categories
```

and find the category your eps are being downloaded for. For this category,
select sabsub.py in the dropdown script (make sure it's chmodded
executable!)

Sickbeard
---------
Installing SickBeard is a little trickier, mainly because you can't set it up
from the webinterface. First, make sure you shutdown SickBeard, otherwise it'll
reset the config file after you edited it. Then go to the place where you have
SickBeard.py installed and
find the config.ini. Open it and change the line:

```
extra_scripts = ""
```

to

```
extra_scripts = /home/user/bin/sabsub/sabsub.py
```

where, ofcourse, the path is the path to the sabsub.py file. Afterwards you can
restart SickBeard

crontab
-------
The final step in installing SabSub is setting up a crontab to make sure your
subs are downloaded for you. Make sure you don't set the crontab to run too
often, otherwise the API key will get revoked making the app unusable for
everyone. A good default is to run it once every hour. To set this up, first
edit your crontab:

```
user@box$ crontab -e
```

Then, in the editor that started, add the following line to the bottom:

```
0   *   *   *   *   /home/user/bin/sabsub/sabsub.py
```

This will run sabsub every hour.

Happy subtitling!
