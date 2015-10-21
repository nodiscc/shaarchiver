#!/usr/bin/python
#
# -*- coding: utf8 -*-
# License: GNU GPLv3 (https://www.gnu.org/copyleft/gpl.html)
# Copyright (c) 2014-2015 nodiscc <nodiscc@gmail.com>

# TODO write link description to markdown, if any
# TODO escape special markdown characters when writing descriptions
# TODO add blacklist entries for youtube channels, soundcloud streams...
# TODO download pages (wget, httrack with −%M generate a RFC MIME−encapsulated full−archive (.mht) (−−mime−html), pavuk, scrapy)
# TODO catch errors and write them in shaarchiver-errors-date.log
# TODO write successfully downloaded urls in shaarchiver-archived-date.log
#      if link has already been downloaded, skip download (--skip)
#      if link has already been downloaded, just check headers with curl/ytdl and issue a warning if page is gone.
# TODO if download fails due to "unsupported url", download page
# TODO make sure links URIs are supported by wget (http(s) vs. magnet vs. javascript vs ftp)
#      if link is a magnet, download it to $hash.magnet and write the uri inside
#      write  next to title
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
# TODO also (optional) download links in dessriptions
# TODO  add --max-date --min-date options
# TODO new action new action: upload to archive.org (public links only)
#       saving pages to archive.org can be done with curl https://web.archive.org/save/$url
#       add archive.org url to markdown output 'https://web.archive.org/web/' + item.get('href')
#       Uploading media to archive.org can be done with https://github.com/Famicoman/ia-ul-from-youtubedl
#       ability to mirror/re-post to other sites
# TODO bugs at https://github.com/nodiscc/shaarchiver/issues
# TODO support plain text (not html) lists
# TODO scan for links/hashes/magnets inside description...
# TODO add readability/page alteration features https://github.com/wallabag/wallabag/tree/master/inc/3rdparty/site_config
# TODO support special archivers for some sites (some url patterns should trigger a custom command, album extraction, etc)


import os
import sys
import time
import glob
import re
from datetime import date, datetime
from bs4 import BeautifulSoup
from subprocess import call
from optparse import OptionParser
from collections import namedtuple
curdate = time.strftime('%Y-%m-%d_%H%M')

# Define a struct to hold link data
# As a bonus, namedtuple is immutable, which is good because we never need to modify it
Link = namedtuple("Link", "add_date href private tags title description")
########################################

# Config
download_video_for = ["video", "documentaire"] # get video content for links with these tags
download_audio_for = ["musique", "music", "samples"] # get audio content for links with these tags
force_page_download_for = ["index", "doc", "lecture"] # force downloading page even if we found a media link
nodl_tag = ["nodl"] # items tagged with this tag will not be downloaded
ytdl_naming='%(title)s-%(extractor)s-%(playlist_id)s%(id)s.%(ext)s'
ytdl_args = ["--no-playlist", #see http://manpages.debian.org/cgi-bin/man.cgi?query=youtube-dl
            "--flat-playlist",
            "--continue",
            #"--max-filesize", "100M",
            #"--rate-limit", "100K",
            "--ignore-errors",
            "--console-title",
            "--add-metadata"]
url_blacklist = [ #links with these exact urls will not be downloaded
                "http://www.midomi.com/",  #workaround for broken redirect
                "http://broadcast.infomaniak.net/radionova-high.mp3" #prevents downloading live radio stream
                ]


########################################

# Parse command line options
parser = OptionParser()
parser.add_option("-t", "--tag", dest="usertag",
                action="store", type="string",
                help="download files only for specified TAG", metavar="TAG")
parser.add_option("-f", "--file", dest="bookmarksfilename", action="store", type="string",
                help="source HTML bookmarks FILE", metavar="FILE")
parser.add_option("-d", "--destination", dest="destdir", action="store", type="string",
                help="destination backup DIR", metavar="DIR")
parser.add_option("-m", "--markdown", dest="markdown",
                action="store_true", default="False",
                help="create a summary of files with markdown")
parser.add_option("-3", "--mp3", dest="mp3",
                action="store_true", default="False",
                help="Download audio as mp3 (or convert to mp3 after download)")
parser.add_option("-n", "--no-download", dest="download",
                action="store_false", default="True",
                help="do not download files")
parser.add_option("--min-date", dest="minimum_date",
                action="store", type="string",
                help="earliest date from which the links should be exported (DD/MM/YYYY)")
parser.add_option("--max-date", dest="maximum_date",
                action="store", type="string",
                help="latest date from which the links should be exporter (DD/MM/YYYY)")
(options, args) = parser.parse_args()

########################################


# Check mandatory options
if not options.destdir:
    print('''Error: No destination dir specified''')
    parser.print_help()
    exit(1)
try:
    bookmarksfile = open(options.bookmarksfilename)
except (TypeError):
    print('''Error: No bookmarks file specified''')
    parser.print_help()
    exit(1)
except (IOError):
    print('''Error: Bookmarks file %s not found''' % options.bookmarksfilename)
    parser.print_help()
    exit(1)

options.compare_with_max = False
options.compare_with_min = False
options.should_compare_dates = False

if options.minimum_date is not None:
	options.should_compare_dates = True
	options.compare_with_min = True
	options.minimum_date_parsed = datetime.strptime(options.minimum_date, "%d/%m/%Y").date()

if options.maximum_date is not None:
	options.should_compare_dates = True
	options.compare_with_max = True
	options.maximum_date_parsed = datetime.strptime(options.maximum_date, "%d/%m/%Y").date()


# Open files
try:
    os.makedirs(options.destdir)
    os.makedirs(options.destdir + "/video")
    os.makedirs(options.destdir + "/audio")
    os.makedirs(options.destdir + "/pages")
except:
    pass

if options.markdown:
    markdownfile = options.destdir + "/links-" + curdate + ".md"
    markdown = open(markdownfile, 'wt+')

logfile = options.destdir + "/" + "shaarchiver-" + curdate + ".log"
log = open(logfile, "a+")


# Parse HTML
rawdata = bookmarksfile.read()
bsdata = BeautifulSoup(rawdata)
alllinks = bsdata.find_all(["dt", "dd"])
#############################################
# Functions

def get_link_list(links):
	item_count = len(links)
	link_list = list()
	for i in range(0, item_count):
		if links[i].name == "dd":
			# We don't want to parse dd links, just find out if they're after a dt
			continue

		desc = ""
		if i + 1 < item_count and links[i+1].name == "dd":
			desc = links[i+1].contents[0]

		subtag = links[i].find('a')
		tags_as_list = subtag['tags'].split(',') if subtag['tags'] is not None or subtag['tags'] is not "" else list()
		item = Link(add_date = subtag['add_date'],
					href = subtag['href'],
					private = subtag['private'] is '1',
					tags = tags_as_list,
					title = subtag.contents[0],
					description = desc)
		link_list.append(item)

	return link_list

def match_list(linktags, matchagainst): # check if sets have a common element (bool)
        if bool(set(linktags) & set(matchagainst)):
            return True
        else:
            return False

def check_dl(linktags, linkurl): # check if given link should be downloaded (bool)
    if linkurl in url_blacklist:
        msg = "[shaarchiver] Url %s is in blacklist. Not downloading item." % (linkurl)
        print(msg)
        log.write(msg + "\n")
        return False
    elif options.download == False:
        return False
        msg = "[shaarchiver] Download disabled, not downloading %s" % linkurl
        print(msg)
        log.write(msg + "\n")
    elif match_list(linktags, nodl_tag):
        msg = "[shaarchiver] Link %s is tagged %s and will not be downloaded." % (linkurl, nodl_tag)
        print(msg)
        log.write(msg + "\n")
        return False
    elif options.usertag and not match_list(linktags, options.usertag):
        msg = "[shaarchiver] Link %s is NOT tagged %s and will not be downloaded." % (linkurl, options.usertag)
        print(msg)
        log.write(msg + "\n")
        return False

    else:
        return True


def gen_markdown(linktitle, linkurl, linktags): # Write markdown output to file
    mdline = " * [" + linktitle + "](" + linkurl + ")" + "`@" + ' @'.join(linktags) + "`"
    markdown.write((mdline.encode('utf-8') + "\n".encode('UTF-8')).decode('UTF-8'))
    log.write("markdown generated for " + linkurl + str(linktags) + "\n")




def download_page(linkurl, linktitle, linktags):
    if check_dl(linktags, linkurl):
        if match_list(linktags, force_page_download_for):
            msg = "[shaarchiver] Force downloading page for %s" % linkurl
            print(msg)
            log.write(msg + "\n")
        elif match_list(linktags, download_video_for) or match_list(linktags, download_audio_for):
            msg = "[shaarchiver] %s will only be searched for media. Not downloading page" % linkurl
            print(msg)
            log.write(msg + "\n")
        else:
            msg = "[shaarchiver] Simulating page download for %s. Not yet implemented TODO" % ((linkurl + linktitle).encode('utf-8'))
            #TODO: download pages,see https://superuser.com/questions/55040/save-a-single-web-page-with-background-images-with-wget
            #TODO: if link has a numeric tag (d1, d2, d3), recursively follow links restricted to the domain/directory and download them.
            print(msg)
            log.write(msg + "\n")



def download_video(linkurl, linktags):
    if check_dl(linktags, linkurl):
        if match_list(linktags, download_video_for):
            msg = "[shaarchiver] Downloading video for %s" % linkurl
            print(msg)
            log.write(msg + "\n")
            command = ["youtube-dl"] + ytdl_args + ["--format", "best",
                    "--output", options.destdir +  "/video/" + "[" + ','.join(linktags) + "]" + ytdl_naming,
                    linkurl]
            call(command)



def download_audio(linkurl, linktags):
    if check_dl(linktags, linkurl):
        if match_list(linktags, download_audio_for):
            msg = "[shaarchiver] Downloading audio for %s" % linkurl
            print(msg)
            log.write(msg + "\n")
            if options.mp3 == True:
                command = ["youtube-dl"] + ytdl_args + ["--extract-audio", "--audio-format", "mp3",
                        "--output", options.destdir + "/audio/mp3/" + "[" + ','.join(linktags) + "]" + ytdl_naming,
                        linkurl]
                call(command)
            else:
                command = ["youtube-dl"] + ytdl_args + ["--extract-audio", "--audio-format", "best",
                        "--output", options.destdir + "/audio/" + "[" + ','.join(linktags) + "]" + ytdl_naming,
                        linkurl]
                call(command)


def debug_wait(msg):
    raw_input("DEBUG: %s") % msg

def get_all_tags(alllinks):
	alltags = []
	for link in alllinks:
		alltags = list(set(alltags + link.tags))
	return alltags


#######################################################################

link_list = get_link_list(alllinks)

msg = '[shaarchiver] Got %s links.' % len(link_list)
print(msg)
log.write(msg + "\n")
if options.markdown:
    markdown.write("## " + options.bookmarksfilename + '\n' + str(len(link_list)) + " links\n\n")
    markdown.write(("```\n".encode('UTF-8') + ' '.join(get_all_tags(link_list)).encode('UTF-8') + "\n```\n\n".encode('UTF-8')).decode('UTF-8'))
    # Python2 & 3 compatibility. the str type has changed in python3.

for link in link_list:
	if options.should_compare_dates:
		linkdate = date.fromtimestamp(float(link.add_date))
		if options.compare_with_min and (linkdate < options.minimum_date_parsed):
			continue
		if options.compare_with_max and (linkdate > options.maximum_date_parsed):
			continue

	linkurl = link.href
	linktitle = link.title
	download_page(linkurl, linktitle, link.tags)
	download_video(linkurl, link.tags)
	download_audio(linkurl, link.tags)
	if options.markdown:
		gen_markdown(linktitle, linkurl, linktags)

log.close()
if options.markdown:
	markdown.close()
