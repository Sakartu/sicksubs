SickSubs
========


```
IMPORTANT

At the end of November bierdopje.com stopped offering subtitles. SickSubs has
since been reprogrammed to use periscope since then, but this requires a clean
database! So, if you still want to use SickSubs you have to remove your old
database (usually located at ~/.sicksubs/sicksubs.db) so it can be reinitialized.

My apologies for any inconvenience :)
```

Thank you for downloading SickSubs. This tool fits perfectly in your Sickbeard 
show-download-chain and helps you download subtitles (either in Dutch
or in English) for all your downloaded eps.

All the configuration can be found inside the sicksubs.py file, including an
explanation on what each parameter does and how to use it.

One of the goals of SickSubs is to stay simple, small and nimble, so no big
databases or folder scans. If installed correctly (see INSTALLATION.md), SickSubs
works as follows:

1. When Sickbeard is done processing the downloaded ep, SickSubs will be
   notified. It adds information for the downloaded and processed ep to it's local
   database and will try to find a subtitle for your ep. If there is no sub
   available yet it will remain in the database for cron to process later. If a sub
   can be found it will be downloaded and the ep information will be removed
   immediately from the db.
2. Once every x hours (depending on how the crontab is setup) SickSubs will check
   all items in the database and will try to find subs for each of them using the
   [periscope](http://code.google.com/p/periscope/).

SickSubs can be found on github: https://github.com/Sakartu/sicksubs.git

If you like SickSubs you may want to try out my other show management tool as well
called next. next can be found at https://github.com/Sakartu/next

Included with SickSubs is a small rename_subs utility. If you already downloaded
some subs but they don't have the correct name yet (read: there's still scene
release group stuff in the name and the avi doesn't have that), just run
rename_subs in the dir where the subs/avi files are located and it will rename
the sub file to the proper name, using the avi naming scheme. If you provide 
a single commandline argument to rename_subs you can indicate the directory in
which it should work (instead of the current working directory).
