# shaarchiver - TODO

## export-shaarli.py

```
#TODO merge script with bookmarks-fetcher.py
#TODO: allow downloading links via RSS, if linktype=public, no password/username required
#TODO:
    # parser.add_option("--html", dest="html",
    #                 action="store_true", default="False",
    #                 help="download HTML bookmarks export")
    # parser.add_option("--rss", dest="rss",
    #                 action="store_true", default="False",
    #                 help="download public bookmarks via RSS (no need to login)")
    # parser.add_option("--rss-private", dest="rss-private",
    #                 action="store_true", default="False",
    #                 help="also download private links via RSS")
```

## bookmarks-fetcher.py

```
# TODO write successfully downloaded urls in done.log
#      if link has already been downloaded, skip download (--skip)
#      if link has already been downloaded, just check headers with curl/ytdl and issue a warning if page is gone.
# TODO catch errors and write them in shaarchiver-errors-date.log
# TODO escape special markdown characters when writing descriptions
# TODO [doc] add examples blacklist entries for youtube channels, soundcloud streams...
# TODO download pages (wget, httrack with −%M generate a RFC MIME−encapsulated full−archive (.mht) (−−mime−html), pavuk, scrapy, https://github.com/lorien/grab)
#       https://superuser.com/questions/55040/save-a-single-web-page-with-background-images-with-wget
# TODO if link has a numeric tag (d1, d2, d3), recursively follow links to htm,html,zip,png,jpg,wam,ogg,mp3,flac,avi,webm,ogv,mp4,pdf... restricted to the domain/directory and download them.
# TODO if download fails due to "unsupported url", download page
# TODO make sure links URIs are supported by wget (http(s) vs. javascript vs ftp)
#      write   next to magnet links title
# TODO use special downloaders/extractor when link url matches a pattern (https://github.com/alexgisby/imgur-album-downloader ...)
# TODO write a link to the local, archived file after the URL  for pages,  for video,  for audio
# TODO don't use --no-playlist when item is tagged playlist, album...
# TODO build HTML index (don't use mdwiki)
#      Make it filterable/searchable https://github.com/krasimir/bubble.js
# TODO Separate public/private link directories
# TODO new action makeplaylist: create an m3U playlist for media, linking to the media url reported by youtube-dl --get-url
# TODO filter ads from downloaded webpages (dnsmasq and host files)
#       https://github.com/Andrwe/privoxy-blocklist/blob/master/privoxy-blocklist.sh
#       patterns in ad-hosts.txt
#       https://github.com/jacobsalmela/pi-hole
#       ublock hosts file list
#       https://github.com/StevenBlack/hosts
# TODO new action new action: upload to archive.org (public links only)
#       saving pages to archive.org can be done with curl https://web.archive.org/save/$url
#       add archive.org url to markdown output 'https://web.archive.org/web/' + item.get('href')
#       Uploading media to archive.org can be done with https://github.com/Famicoman/ia-ul-from-youtubedl
#       ability to mirror/re-post to other sites
# TODO bugs at https://github.com/nodiscc/shaarchiver/issues
# TODO support plain text (not html) lists
# TODO scan for links/hashes/magnets inside description...
# TODO also (optional) download links in dessriptions
# TODO GUI https://ipfs.pics/ipfs/Qmd7vy36VqSE3PqVSdjTMA2apfeboe49oJkVspKGdLpFd9, see python-wxgtk
# TODO add readability/page alteration features https://github.com/wallabag/wallabag/tree/master/inc/3rdparty/site_config
# TODO support special archivers for some sites (some url patterns should trigger a custom command, album extraction, etc)
```