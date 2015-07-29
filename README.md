# shaarchiver
Archive your Firefox, [Shaarli](https://github.com/shaarli/Shaarli) or [delicious](https://delicious.com) bookmarks.

 * Downloads exports from your own Shaarli install
 * Extract and archive links from Shaarli/delicious bookmark exports (Netscape HTML format)
 * Downloads all linked media (audio/video) for archiving, backup, offline use... (uses [youtube-dl](https://github.com/rg3/youtube-dl/))

### Installation
 * `git clone https://github.com/nodiscc/shaarchiver` or download and extract the [zip archive](https://github.com/nodiscc/shaarchiver/archive/master.zip)
 * install the required python modules: `python-bs4 python-requests`


### Usage
Edit the config variables at the beginning of `bookmarks-fetcher.py` if needed.

#### Backup your Shaarli bookmarks as an HTML file

```
 ↳ ./export-shaarli.py -h
Usage: export-shaarli.py [options]

Options:
  -h, --help            show this help message and exit
  --username=USERNAME   username for HTML and private links export
  --password=PASSWORD   password for HTML and private links export
  -d DOWNLOADDIR, --download-dir=DOWNLOADDIR
                        destination directory for bookmark backups
  -u URL, --url=URL     URL of your Shaarli (https://my.example.com/links)
  -t TYPE, --type=TYPE  download links of TYPE (public, private or all)


```

#### Archive contents (pages, audio, video) for links in the HTML file

```
 ↳ ./bookmarks-fetcher.py -h
Usage: bookmarks-fetcher.py [options]

Options:
  -h, --help            show this help message and exit
  -t TAG, --tag=TAG     download files only for specified TAG
  -f FILE, --file=FILE  source HTML bookmarks FILE
  -d DIR, --destination=DIR
                        destination backup DIR
  -m, --markdown        create a summary of files with markdown
  -3, --mp3             Download audio as mp3 (or convert to mp3 after
                        download)
  -n, --no-download     do not download files
```

#### Bugs/feature requests/discussion
 * https://github.com/nodiscc/shaarchiver/issues/

#### Examples

Download all links from an HTML export, and generate a markdown file:

```
$ ./bookmarks-fetcher.py -d backups --markdown -f bookmarks_public_20150527_005153.html 

[shaarchiver] Got 2751 links.
[shaarchiver] https://soundcloud.com/incontrol/the-dont-look-back-mix-es112 will only be searched for media. Not downloading page
[shaarchiver] Downloading audio for https://soundcloud.com/incontrol/the-dont-look-back-mix-es112
[soundcloud] incontrol/the-dont-look-back-mix-es112: Resolving id
[soundcloud] incontrol/the-dont-look-back-mix-es112: Downloading info JSON
[soundcloud] 76401832: Downloading track url
[soundcloud] 76401832: Checking download video format URL
[soundcloud] 76401832: Checking http_mp3_128_url video format URL
[download] Destination: backups/audio/[music,album,electronic,swing]the don't look back mix « a trip to electro swing, future blues & soul 3.0 »-soundcloud-NA76401832.mp3
[download] 100% of 56.16MiB in 01:28
[ffmpeg] Adding metadata to 'backups/audio/[music,album,electronic,swing]the don't look back mix « a trip to electro swing, future blues & soul 3.0 »-soundcloud-NA76401832.mp3'
[youtube] Post-process file backups/audio/[music,album,electronic,swing]the don't look back mix « a trip to electro swing, future blues & soul 3.0 »-soundcloud-NA76401832.mp3 exists, skipping
[shaarchiver] Force downloading page for http://www.aurel32.net/elec/frequences_radio.php
[shaarchiver] Force downloading page for https://automatetheboringstuff.com/
[shaarchiver] Simulating page download for http://www.jeuxvideo.com/jeux/jeu-62643/Jeu Grand Theft Auto : San Andreas sur Jeuxvideo.com. Not yet implemented TODO
[shaarchiver] Force downloading page for http://www.influencia.net/fr/actualites/com-media,media,six-principes-universels-influence,5410.html
[shaarchiver] Simulating page download for http://www.allocine.fr/film/fichefilm_gen_cfilm=25802.htmlStar Wars : Episode V - L'Empire contre-attaque - film 1980 - AlloCiné. Not yet implemented TODO
[shaarchiver] Simulating page download for http://www.allocine.fr/film/fichefilm_gen_cfilm=10126.htmlPulp Fiction - film 1994 - AlloCiné. Not yet implemented TODO
[shaarchiver] Force downloading page for https://en.wikipedia.org/wiki/Surround_sound
[shaarchiver] http://boitalopez.neuviemepage.com/ will only be searched for media. Not downloading page
[shaarchiver] Downloading audio for http://boitalopez.neuviemepage.com/
[generic] boitalopez.neuviemepage: Requesting header
WARNING: Falling back on generic information extractor.
[generic] boitalopez.neuviemepage: Downloading webpage
[generic] boitalopez.neuviemepage: Extracting information
ERROR: Unsupported URL: http://boitalopez.neuviemepage.com/
[shaarchiver] https://www.youtube.com/watch?v=aOPW6wzs8Ks will only be searched for media. Not downloading page
[shaarchiver] Downloading video for https://www.youtube.com/watch?v=aOPW6wzs8Ks
[youtube] aOPW6wzs8Ks: Downloading webpage
[youtube] aOPW6wzs8Ks: Extracting video information
[youtube] aOPW6wzs8Ks: Downloading DASH manifest
[download] Destination: backups/video/[video,société]Maladies à vendre #DATAGUEULE 37-youtube-NAaOPW6wzs8Ks.mp4
[download] 100% of 44.08MiB in 01:03
[ffmpeg] Adding metadata to 'backups/video/[video,société]Maladies à vendre #DATAGUEULE 37-youtube-NAaOPW6wzs8Ks.mp4'
[shaarchiver] Force downloading page for https://medium.com/@landongn/12-years-later-what-i-ve-learned-about-being-a-software-engineer-d6e334d6e8a3
[shaarchiver] Simulating page download for https://www.flickr.com/photos/19334142@N05/sets/72157651767516139North Korea Panorama | Flickr - Photo Sharing!. Not yet implemented TODO
[shaarchiver] https://www.youtube.com/watch?v=ZqcOpShEOZ0 will only be searched for media. Not downloading page
[shaarchiver] Downloading audio for https://www.youtube.com/watch?v=ZqcOpShEOZ0
[youtube] ZqcOpShEOZ0: Downloading webpage
[youtube] ZqcOpShEOZ0: Extracting video information
[youtube] ZqcOpShEOZ0: Downloading DASH manifest
[download] Destination: backups/audio/[music,blues]Fink - Pretty Little Thing-youtube-NAZqcOpShEOZ0.m4a
[download] 100% of 8.37MiB in 00:12
[ffmpeg] Correcting container in "backups/audio/[music,blues]Fink - Pretty Little Thing-youtube-NAZqcOpShEOZ0.m4a"
[ffmpeg] Adding metadata to 'backups/audio/[music,blues]Fink - Pretty Little Thing-youtube-NAZqcOpShEOZ0.m4a'
[youtube] Post-process file backups/audio/[music,blues]Fink - Pretty Little Thing-youtube-NAZqcOpShEOZ0.m4a exists, skipping
[shaarchiver] https://www.youtube.com/watch?v=HI7J-1NZT2U will only be searched for media. Not downloading page
[shaarchiver] Downloading audio for https://www.youtube.com/watch?v=HI7J-1NZT2U
[youtube] HI7J-1NZT2U: Downloading webpage
[youtube] HI7J-1NZT2U: Extracting video information
[youtube] HI7J-1NZT2U: Downloading DASH manifest
[download] Destination: backups/audio/[music,hiphop,dark,oldschool]Survival of the Fittest---Mobb Deep(HQ).-youtube-NAHI7J-1NZT2U.m4a
[download] 100% of 6.50MiB in 00:09
```

Here is what your backup directory should look like after archiving some links:

```
$ tree backups

backups/
├── audio
│   ├── [downtempo,music,pl:high,soul,triphop]Alina Baraz & Galimatias - Show Me-soundcloud-NA206220422.mp3
│   ├── [music,album,electronic,swing]the don't look back mix « a trip to electro swing, future blues & soul 3.0 »-soundcloud-NA76401832.mp3
│   ├── [music,blues,album,oldschool]Howlin' Wolf - Moanin' in the Moonlight FULL ALBUM [1959]-youtube-NAb3_87n7Kn94.m4a
│   ├── [music,blues]B.B.King -  Why I Sing the Blues-youtube-NAIBBFnmcfYOg.m4a
│   ├── [music,blues]Fink - Pretty Little Thing-youtube-NAZqcOpShEOZ0.m4a
│   ├── [music,blues,oldschool]Jacques Dutronc - Fais Pas Ci Fais Pas Ça-youtube-NA7QN2Jcor60A.m4a
│   ├── [music,electronic,dnb,oldschool]Aphrodite - Stalker [Original mix]-youtube-NANJNHL4WPO9w.m4a
│   ├── [music,electronic,trap]TroyBoi - Remember-youtube-NAmNeQWl4C12w.m4a
│   ├── [music,hiphop,dark,oldschool]Survival of the Fittest---Mobb Deep(HQ).-youtube-NAHI7J-1NZT2U.m4a
│   ├── [music,hiphop,oldschool]Mobb Deep - Shook Ones Part II (HD)-youtube-NA0NUX4tW5pps.m4a
│   ├── [music,hiphop]Snoop Dogg - The Next Episode (with lyrics)-youtube-NA0Uyfc3EDPBA.m4a
│   ├── [music,hiphop,soul,jazz]Soul Square - That Swing-youtube-NAJLcrjowDu1M.m4a
│   ├── [music,hiphop,soul]Soul Square - Change feat. Justis-youtube-NAlzLKklvmG7c.m4a
│   ├── [music,hiphop,soul]Soul Square - It's All In Your Mind feat. Melodiq-youtube-NAc2RS-rzbv3g.m4a
│   ├── [music,hiphop,soul]Soul Square - Know I'm Sayin'-youtube-NAU0pQd2_pspE.m4a
│   ├── [music,hiphop,soul]Soul Square - Take It Back feat. Blezz-youtube-NAXYrnB-o-xiI.m4a
│   ├── [music,jazz,hiphop]Soul Square - Trippin' feat. Blezz-youtube-NAJpd2p8Ns8dQ.m4a
│   ├── [music,jazz]Nu jazz _ New sector movement _ Mass Car Raid-youtube-NATxKxWiyCRLM.m4a
│   ├── [music,oldschool,reggae]Linval Thompson - Cool Down Your Temper b_w Version-youtube-NAchuuKmij-WA.m4a
│   ├── [music,reggae,groove]Damian Marley - Road To Zion Feat  Nas-youtube-NA986bKHVUvNI.m4a
│   ├── [music,reggae,ragga]Damian Marley Welcome To Jamrock lyrics on SCREEN-youtube-NA9Q4IO19E8Kg.m4a
│   ├── [music,soul,triphop,downtempo]Alina Baraz & Galimatias - Drift-soundcloud-NA104762415.mp3
│   ├── [music,triphop]Polaroid 85 - The Time (Rogan Remix)-soundcloud-NA148503120.mp3
│   ├── [music,triphop,soul,downtempo]Alina Baraz & Galimatias - Can I-soundcloud-NA202198852.mp3
│   ├── [music,video,animation]Le Cafe - Oldelaf _ Future Shorts-youtube-NAUGtKGX8B9hU.m4a
│   └── [video,jazz,music,oldschool]Art Blakey & The Jazz Messengers  - A Night In Tunisia - 1958-youtube-NA2IQNPlnc9c0.m4a
├── links-2015-07-28_2307.md
├── pages
├── shaarchiver-2015-07-28_2307.log
└── video
    ├── [audio,elec,history,instruments,wtf,video]Electronic Musician Jean-Jacques Perrey on 'I've Got a Secret'-youtube-NA7pOqkn9JgO8.mp4
    ├── [music,video,animation]Le Cafe - Oldelaf _ Future Shorts-youtube-NAUGtKGX8B9hU.mp4
    ├── [video,jazz,music,oldschool]Art Blakey & The Jazz Messengers  - A Night In Tunisia - 1958-youtube-NA2IQNPlnc9c0.mp4
    └── [video,société]Maladies à vendre #DATAGUEULE 37-youtube-NAaOPW6wzs8Ks.mp4

3 directories, 32 files
```
