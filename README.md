SabSub
======

Thank you for downloading SabSub. This tool fits perfectly in your SABnzbd +
Sickbeard show-download-chain and helps you download subtitles (either in Dutch
or in English) for all your downloaded eps.

All the configuration can be found inside the sabsub.py file, including an
explanation on what each parameter does and how to use it.

One of the goals of SabSub is to stay simple, small and nimble, so no big
databases or folder scans. If installed correctly (see INSTALLATION.md), SabSub
works as follows:

1. When an ep is downloaded by SABnzbd, SabSub will be notified through the
   SABnzbd post-processing hook. It adds information about the downloaded show
   to the queue-file, namely the job name and the intermediate location of the
   episode.
2. When Sickbeard is done processing the downloaded ep, SabSub will be notified
   again to add some more data to the queue-file, namely the final destination
   and name of the ep.
3. Once every x hours (depending on how the crontab is setup) SabSub will check
   all items in the queue and will try to find subs for each of them using the
   Bierdopje (http://www.bierdopje.com) API. As it knows exactly the show and ep
   for which to find a subtitle the API load is minimal, but try to keep it that
   way by not setting your crontab to check for subs every 3 seconds :)

SabSub can be found on github: https://github.com/Sakartu/sabsub

If you like SabSub you may want to try out my other show management tool as well
called next. next can be found at https://github.com/Sakartu/next
