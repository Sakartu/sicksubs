SabSub Installation
===================

The SabSub installation consists of three steps:

1. Add SabSub to the SABnzbd configuration as post-processing script
2. Add SabSub to the Sickbeard configuration as post-post-processing script
3. Add a crontab line for SabSub

Each of these steps will be described below in detail.

SABnzbd
-------
In the main SABnzbd interface, go to:

```
Config -> Folders
```

and at the "Post-Processing Scripts Folder" setting, put the folder where SabSub
is located. This is probably something like "/home/user/bin/sabsub" if you
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
The final step in installing SabSub is setting up a crontab to make sure your subs are downloaded for you. Make sure you don't set the crontab to run too often, otherwise the API key will get revoked making the app unusable for everyone. A good default is to run it once every hour. To set this up, first edit your crontab:

```
user@box$ crontab -e
```

Then, in the editor that started, add the following line to the bottom (without the >, if you're reading this INSTALLATION file in a text editor instead of github):

```
0   *   *   *   *   /home/user/bin/sabsub/sabsub.py
```

This will run sabsub every hour.

Happy subtitling!
