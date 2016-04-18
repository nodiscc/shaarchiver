#!/usr/bin/python
# -*- coding: utf8 -*-
#
# License: GNU GPLv3 (https://www.gnu.org/copyleft/gpl.html)
# Copyright (c) 2014-2015 nodiscc <nodiscc@gmail.com>

import os
import sys
import time
import glob
import re
import codecs
from datetime import date, datetime
from bs4 import BeautifulSoup
from subprocess import call
from optparse import OptionParser
from collections import namedtuple
curdate = time.strftime('%Y-%m-%d_%H%M')
# Define a struct to hold a link data
# namedtuples are immutables
Link = namedtuple("Link", "add_date href private tags title description is_magnet")

# Converts a string to its unicode representation
def make_unicode(input):
    if type(input) != unicode:
        input =  input.decode('utf-8')
        return input
    else:
        return input

########################################

#Config
download_video_for = ["video", "documentaire"] # get video content for links with these tags
download_audio_for = ["musique", "music", "samples"] # get audio content for links with these tags
force_page_download_for = ["index", "doc", "lecture"] # force downloading page even if we found a media link
nodl_tag = ["nodl"] # items tagged with this tag will not be downloaded
ytdl_naming='%(title)s-%(extractor)s-%(playlist_id)s%(id)s.%(ext)s' #naming pattern for downloaded media
ytdl_args = [ #Youtube-dl options, see http://manpages.debian.org/cgi-bin/man.cgi?query=youtube-dl
            "--no-playlist", 
            "--flat-playlist",
            "--continue",
            "--max-filesize", "1200M",
            #"--rate-limit", "100K",
            "--ignore-errors",
            "--console-title",
            "--add-metadata"]
url_blacklist = [ #links with these exact urls will not be downloaded
                "http://www.midomi.com/",  #workaround for broken redirect
                "http://broadcast.infomaniak.net/radionova-high.mp3", #prevents downloading live radio stream
                "https://en.wikipedia.org/wiki/Youtube" #prevents downloading wikipedia spoken article
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
                help="latest date from which the links should be exported (DD/MM/YYYY)")
parser.add_option("--no-skip", dest="no_skip",
                action="store_true", default="False",
                help="Do not skip downloading links present in done.log")
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
    markdown = codecs.open(markdownfile,'wb+', encoding="utf-8")

logfile = options.destdir + "/" + "shaarchiver-" + curdate + ".log"
log = codecs.open(logfile, "a+", encoding="utf-8")

log_done = codecs.open(options.destdir + "/done.log", "r+", encoding="utf-8")
#Read already downloaded URLs
downloaded_urls = log_done.readlines()
downloaded_urls = [x.replace('\n', '') for x in downloaded_urls]


# Parse HTML
rawdata = bookmarksfile.read()
bsdata = BeautifulSoup(rawdata)
alllinks = bsdata.find_all(["dt", "dd"])

#############################################
# Functions

def getlinktags(link):     # return tags for a link (list)
    linktags = link.get('tags')
    if linktags is None:
        linktags = list()
    else:
        linktags = linktags.split(',')
    return linktags

def get_link_list(links):
    item_count = len(links)
    link_list = list()
    for i in range(0, item_count):
        if links[i].name == "dd":
            # We don't want to parse <DD>s, just find out if they're after a <DT>
            continue

        desc = ""
        if i + 1 < item_count and links[i+1].name == "dd":
            desc = links[i+1].contents[0]

        subtag = links[i].find('a')
        tags_as_list = list()
        if subtag.has_attr('tags'):
            tags_as_list = subtag['tags'].split(',')
        
        item = Link(add_date=subtag['add_date'],
                    href=subtag['href'],
                    private=subtag['private'] == "1",
                    tags=tags_as_list,
                    title=subtag.contents[0],
                    description=desc,
                    is_magnet=subtag['href'].startswith("magnet:"))

        link_list.append(item)

    return link_list


def match_list(linktags, matchagainst): # check if sets have a common element (bool)
        if bool(set(linktags) & set(matchagainst)):
            return True
        else:
            return False

def check_dl(linktags, linkurl): # check if given link should be downloaded (bool)
    dl_allowed = True
    if linkurl in url_blacklist:
        msg = "[shaarchiver] Url %s is in blacklist. Not downloading item." % (make_unicode(linkurl))
        dl_allowed = False
    elif options.download == False:
        msg = "[shaarchiver] Download disabled, not downloading %s" % make_unicode(linkurl)
        dl_allowed = False
    elif match_list(linktags, nodl_tag):
        msg = "[shaarchiver] Link %s is tagged %s and will not be downloaded." % (make_unicode(linkurl), nodl_tag)
        dl_allowed = False
    elif options.usertag and not match_list(linktags, options.usertag):
        msg = "[shaarchiver] Link %s is NOT tagged %s and will not be downloaded." % (make_unicode(linkurl), options.usertag)
        dl_allowed = False
    elif match_list([linkurl], downloaded_urls) and not options.no_skip:
        msg = "[shaarchiver] Link %s was already downloaded. Skipping." % make_unicode(linkurl)
        dl_allowed = False
    if not dl_allowed:
        print(msg)
        log.write(msg + "\n")
    return dl_allowed

def gen_markdown(link): # Write markdown output to file
    tags = ""
    if len(link.tags) > 0:
        tags = ' @'
    tags += ' @'.join(link.tags)
    mdline = make_unicode(" * [" + link.title + "](" + link.href + ")" + "`" + tags + "`\n")
    markdown.write(mdline)
    if link.description != "":
        desc = make_unicode(u"```\n{0}```\n".format(link.description))
        markdown.write(desc)
    log.write("markdown generated for " + link.href + str(link.tags) + "\n")

def download_page(linkurl, linktitle, linktags):
    if link.is_magnet:
        # We found a magnet link ! create a new file and write it
        # Here's a lovely regex to retrieve the SHA hash from a magnet
        # xt=.*:([^&]*)
        # This works with the hash anywhere in the magnet, with btih: or sha1: schemes
        matches = re.findall("xt=.*:([^&]*)", link.href)
        if matches is None or len(matches) == 0:
            msg = "[shaarchiver] Link appears to be a magnet, but no hash could be found. Not saving it"
            print(msg)
            log.write(msg + "\n")
            pass
        hash = matches[0]
        msg = "[shaarchiver] Link is a magnet. Saving it to %s.magnet" % hash
        print(msg)
        handle = open(options.destdir + "/" + hash + ".magnet", "w+")
        handle.write(link.href)
        handle.close()
    elif match_list(linktags, force_page_download_for):
        msg = "[shaarchiver] Force downloading page for %s" % linkurl
        print(msg)
        log.write(msg + "\n")
    elif match_list(linktags, download_video_for) or match_list(linktags, download_audio_for):
        pass
        #msg = "[shaarchiver] %s will only be searched for media. Not downloading page" % linkurl
        #print(msg)
        #log.write(msg + "\n")
    else:
        msg = "[shaarchiver] Simulating page download for %s. Not yet implemented TODO" % ((linkurl + linktitle).encode('utf-8'))
        print(msg)
        log.write(msg + "\n")

    if not options.no_skip:
        log_done.write(linkurl + "\n")


def download_video(linkurl, linktags):
    if match_list(linktags, download_video_for):
        msg = "[shaarchiver] Downloading video for %s" % linkurl
        print(msg)
        log.write(msg + "\n")
        command = ["youtube-dl"] + ytdl_args + ["--format", "best",
                "--output", options.destdir +  "/video/" + "[" + ','.join(link.tags) + "]" + ytdl_naming,
                linkurl]
        retcode = call(command)

        if retcode == 0: # Log the URL as downloaded youtube-dl was successful
            if not options.no_skip:
                log_done.write(linkurl + "\n")
        else:
            msg = "[shaarchiver] ERROR Download failed for %s" % linkurl
            print(msg)
            log.write(msg + "\n")


def download_audio(linkurl, linktags):
    if match_list(linktags, download_audio_for):
        msg = "[shaarchiver] Downloading audio for %s" % linkurl
        print(msg)
        log.write(msg + "\n")
        if options.mp3 == True:
            command = ["youtube-dl"] + ytdl_args + ["--extract-audio", "--audio-format", "mp3",
                    "--output", options.destdir + "/audio/mp3/" + "[" + ','.join(link.tags) + "]" + ytdl_naming,
                    linkurl]
        else:
            command = ["youtube-dl"] + ytdl_args + ["--extract-audio", "--audio-format", "best",
                    "--output", options.destdir + "/audio/" + "[" + ','.join(link.tags) + "]" + ytdl_naming,
                    linkurl]
        retcode = call(command)

        if retcode == 0: # Log the URL as downloaded youtube-dl was successful
            if not options.no_skip:
                log_done.write(linkurl + "\n")
        else:
            msg = "[shaarchiver] ERROR Download failed for %s" % linkurl
            print(msg)
            log.write(msg + "\n")
        


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
    markdown.write(make_unicode("## " + options.bookmarksfilename + '\n' + str(len(link_list)) + " links\n\n"))
    taglist = make_unicode(' '.join(get_all_tags(link_list)))
    markdown.write(make_unicode(u"```\n{0}\n```\n\n".format(taglist)))

for link in link_list:
    if options.should_compare_dates:
        linkdate = date.fromtimestamp(float(link.get("add_date")))
        if options.compare_with_min and (linkdate < options.minimum_date_parsed):
            continue
        if options.compare_with_max and (linkdate > options.maximum_date_parsed):
            continue

    if check_dl(link.tags, link.href)
        download_page(link.href, link.title, link.tags)
        download_video(link.href, link.tags)
        download_audio(link.href, link.tags)

    if options.markdown:
        gen_markdown(link)

log.close()
log_done.close()
if options.markdown:
    markdown.close()
