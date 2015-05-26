#!/usr/bin/python
#
# -*- coding: utf8 -*-
# License: GNU GPLv3 (https://www.gnu.org/copyleft/gpl.html)
# Copyright (c) 2014-2015 nodiscc <nodiscc@gmail.com>

# TODO write link description to markdown, if any
# TODO also (optional) download links in decsriptions
# TODO catch youtube errors and write them in logfile
# TODO: write a list of URLs fo which downloading has failed
# TODO: don't use --no-playlist when item is tagged playlist, album...
# TODO: new action makeplaylist: create an m3U playlist for media, linking to the media url reported by youtube-dl --get-url
# TODO: make sure links URIs are supported by wget (http(s) vs. magnet vs. javascript vs ftp)
# TODO Separate public/private link directories
# TODO: bugs at https://github.com/nodiscc/shaarchiver/issues
# TODO: support plain text (not html) lists
# TODO: support special archivers for some sites (some url patterns should trigger a custom command, album extraction, etc)


import os
import sys
import time
import glob
import re
from bs4 import BeautifulSoup
from subprocess import call
from optparse import OptionParser

########################################

# Config
download_video_for = ["video", "documentaire"] #get video for links tagged with these tags
download_audio_for = ["musique", "music", "samples"] #get audio for links tagged with these tags
force_page_download_for = ["index", "doc", "lecture"]

nodl_tag = ["nodl"] #items tagged with this tag will not be downloaded
curdate = time.strftime('%Y-%m-%d_%H%M')
ytdl_naming='%(title)s-%(extractor)s-%(playlist_id)s%(id)s.%(ext)s'
ytdl_args = ["--no-playlist",
            "--flat-playlist",
            "--continue",
            #"--rate-limit", "100K",
            "--ignore-errors",
            "--console-title",
            "--add-metadata"]


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
parser.add_option("-n", "--no-download", dest="download",
                action="store_false", default="True",
                help="do not download files")

(options, args) = parser.parse_args()

########################################

# Check mandatory options
if not options.destdir:
    print '''Error: No destination dir specified'''
    parser.print_help()
    exit(1)
try:
    bookmarksfile = open(options.bookmarksfilename)
except (TypeError):
    print '''Error: No bookmarks file specified'''
    parser.print_help()
    exit(1)
except (IOError):
    print '''Error: Bookmarks file %s not found''' % options.bookmarksfilename
    parser.print_help()
    exit(1)


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
    markdown = open(markdownfile, 'w+')

logfile = options.destdir + "/" + "shaarchiver-" + curdate + ".log"
log = open(logfile, "a+")


# Parse HTML
rawdata = bookmarksfile.read()
bsdata = BeautifulSoup(rawdata)
alllinks = bsdata.find_all('a')

#############################################
# Functions

def getlinktags(link):     # return tags for a link (list)
    linktags = link.get('tags')
    if linktags is None:
        linktags = list()
    else:
        linktags = linktags.split(',')
    return linktags

def match_tags(linktags, matchagainst): # check if sets have a common element (bool)
        if bool(set(linktags) & set(matchagainst)):
            return True
        else:
            return False

def check_dl(linktags, linkurl): # check if given link should be downloaded (bool)
    if options.download == False:
        return False
        msg = "Download disabled, not downloading %s" % linkurl
        print msg
        log.write(msg + "\n")
    elif match_tags(linktags, nodl_tag):
        msg = "Link %s is tagged %s and will not be downloaded." % (linkurl, nodl_tag)
        print msg
        log.write(msg + "\n")
        return False 
    elif options.usertag and not match_tags(linktags, options.usertag):
        msg = "Link %s is NOT tagged %s and will not be downloaded." % (linkurl, options.usertag)
        print msg
        log.write(msg + "\n")
        return False 
    else:
        return True


def gen_markdown(linktitle, linkurl, linktags): # Write markdown output to file
    mdline = " * [" + linktitle + "](" + linkurl + ")" + "`@" + ' @'.join(linktags) + "`"
    markdown.write(mdline.encode('utf-8') + "\n")
    log.write("markdown generated for " + linkurl + str(linktags) + "\n")




def download_page(linkurl, linktitle, linktags):
    if check_dl(linktags, linkurl):
        if match_tags(linktags, force_page_download_for):
            msg = "Force downloading page for %s" % linkurl
            print msg
            log.write(msg + "\n")
        elif match_tags(linktags, download_video_for) or match_tags(linktags, download_audio_for):
            msg = "%s will only be searched for media. Not downloading page" % linkurl
            print msg
            log.write(msg + "\n")
        else:
            msg = "Simulating page download for %s. Not yet implemented TODO" % ((linkurl + linktitle).encode('utf-8'))
            #TODO: download pages,see https://superuser.com/questions/55040/save-a-single-web-page-with-background-images-with-wget
            #TODO: if link has a numeric tag (d1, d2, d3), recursively follow links restricted to the domain/directory and download them.
            print msg
            log.write(msg + "\n")



def download_video(linkurl, linktags):
    if check_dl(linktags, linkurl):
        if match_tags(linktags, download_video_for):
            msg = "Downloading video for %s" % linkurl
            print msg
            log.write(msg + "\n")
            command = ["youtube-dl"] + ytdl_args + ["--format", "best",
                    "--output", options.destdir +  "/video/" + "[" + ','.join(linktags) + "]" + ytdl_naming,
                    linkurl]
            call(command)



def download_audio(linkurl, linktags):
    if check_dl(linktags, linkurl):
        if match_tags(linktags, download_audio_for):
            msg = "Downloading audio for %s" % linkurl
            print msg
            log.write(msg = "\n")
            if options.mp3:
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
		linktags = getlinktags(link)
		alltags = list(set(alltags + linktags))
	return alltags


#######################################################################

msg = 'Got %s links.' % len(alllinks)
print msg
log.write(msg + "\n")
if options.markdown:
    markdown.write("## " + options.bookmarksfilename + '\n' + str(len(alllinks)) + " links\n\n") 
    markdown.write("```\n" + ' '.join(get_all_tags(alllinks)).encode('UTF-8') + "\n```\n\n")
    for link in alllinks:
        linkurl = link.get('href')
        linktitle = link.contents[0]
        linktags = getlinktags(link)
        gen_markdown(linktitle, linkurl, linktags)
    markdown.close()

for link in alllinks:
    linkurl = link.get('href')
    linktitle = link.contents[0]
    linktags = getlinktags(link)
    download_page(linkurl, linktitle, linktags)
    download_video(linkurl, linktags)
    #download_audio
    

log.close()