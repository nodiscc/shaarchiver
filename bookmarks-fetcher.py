#!/usr/bin/python
#
# -*- coding: utf8 -*-
# Copyright (c) 2014-2015 nodiscc <nodiscc@gmail.com>
# License: GNU GPLv3 (https://www.gnu.org/copyleft/gpl.html)
#
#
#TODO: support plain text (not html) lists
#TODO: bugs at https://github.com/nodiscc/shaarchiver/issues

#TODO: stream action: just play each element in mplayer using youtube-dl (do not download, play only)
#TODO: mkplaylist action: same as stream, but just output the media urls to an .m3u file
#TODO: handle shaarli's self-posts (eg. ?lNXHUw as href)
#TODO: append link descriptions as sub-list item (<DD> half-ass HTML tag)

#TODO: fetch raw webpages for some predefined tags (doc, news, lecture, alire, wiki), see https://superuser.com/questions/55040/save-a-single-web-page-with-background-images-with-wget
#TODO: if link has a numeric tag (d1, d2, d3) and one of the above, recursively follow links restricted to the domain/directory and download them.
#TODO: for tag 'images', download images embedded in pages (use patterns like wp-contents/uploads/*.jpg, i.imgur.com/*.jpg)

#TODO: add a command line switch to use mp3 output (best by default)
#TODO: write a list of URLs fo which downloading has failed
#TODO: usertag option seems broken. plz test.
#TODO: add third-level tags

import os
import sys
import time
import glob
import re
from bs4 import BeautifulSoup
from subprocess import call
from optparse import OptionParser


###############################################################################
######### CONFIG 
###############################################################################

firstleveltags = ["lecture", "doc", "music", "musique", "video"]
secondleveltags = ["books", "cuisine", "samples", "blues", "hiphop", "electronic", "shortfilm", "documentaire", "films", "wtf", "news", "space", "technology", "games"]
download_media_for = ["musique", "music", "video", "samples"] #download multimedia content for these links
extract_audio_for = ["samples", "music"] #only get audio (not video) for links tagged with these tags
no_download_tag = "nodl" #item will not be downloaded (only print external link)

###############################################################################

#Parse command line options
parser = OptionParser()
parser.add_option("-t", "--tag", dest="usertag",
                action="store", type="string",
                help="download files only for specified TAG", metavar="TAG")
parser.add_option("-f", "--file", dest="bookmarksfilename",
                action="store", type="string",
                help="source HTML bookmarks FILE", metavar="FILE")
parser.add_option("-d", "--destination", dest="destdir",
                action="store", type="string",
                help="destination backup DIR", metavar="DIR")
parser.add_option("-m", "--markdown", dest="markdown",
                action="store_true", default="False",
                help="create a summary of files with markdown")
parser.add_option("-n", "--no-download", dest="download",
                action="store_false", default="True",
                help="do not download files")

(options, args) = parser.parse_args()


#Check mandatory options
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


###############################################################################
######### FUNCTIONS
###############################################################################


def gen_markdown(downloadqueue): #Generate markdown copy of all links
    print "DEBUG: gen_markdown"
    curdate = time.strftime('%Y-%m-%d_%H%M')
    markdownoutfilename = options.destdir + "/" + "links-" + curdate + ".md"
    print "DEBUG: date is %s, outfile is %s" % (curdate, markdownoutfilename)
    
    try:
        os.makedirs(options.destdir)
    except:
        pass

    markdownfile = open(markdownoutfilename, 'w+')
    for item in downloadqueue:
        #print "DEBUG: current item: %s" % item
        outitem = " * [" + item.contents[0] + "](" + item.get('href') + ")" + " `@" + unicode(item.get('tags')) + "`"
        markdownfile.write(outitem.encode('utf-8') + "\n")
    markdownfile.close()


def get_link_type(linkurl, linktags): #Find if an item is media, audio or a web page
    print "DEBUG: get_link_type"

    if len(linktags) == 0:
        linktype = "page"
    elif len(list(set(linktags).intersection(set(download_media_for)))) > 0:
        linktype = "media"
        if len(list(set(linktags).intersection(set(extract_audio_for)))) > 0:
            linktype = "audio"
    else:
        linktype = "page"

    print "DEBUG: detected linktype: %s" % linktype
    return linktype



def get_tag(linktags, taglist): #find item's first and second level tags (TODO: BUG: broken)
    print "DEBUG: get_tag"
    intersection = list(set(linktags).intersection(set(taglist)))
    if len(intersection) > 0:
        matchingtag = intersection[0]
    else:
        matchingtag = "other"

    print "DEBUG: found matching tag: %s" % matchingtag
    return matchingtag



def download_link(link): #elect the appropriate download location for the link
    print "DEBUG: download_link"
    print ' * Downloading %s [%s]' % (link.contents[0], link.get('href'))
    
    linktags = link.get('tags')
    if linktags is None:
        linktags = list()
    else:
        linktags = linktags.split(',')

    linktype = get_link_type(link.get('href'), linktags)
    if linktype == "media":
        ytdl_media(link)
    elif linktype == "audio":
        ytdl_audio(link)
    elif linktype == "page":
        wget_dl(link)

    print "DEBUG: Linkype is %s" % linktype




def do_download_queue(downloadqueue): #start markdown generation and download process if appropriate
    print "DEBUG: do_download_queue"
    if options.markdown:
        gen_markdown(downloadqueue)

    if options.download:
        print "DEBUG: Downloading %s items" % len(downloadqueue)
        for item in downloadqueue:
            download_link(item)
    else:
        print "Downloading disabled, skipping download."




def get_output_dir(link): #generate an output path based on tags (broken?)
    #should be options.destdir/linktype/firstleveltag/secondleveltag/
    print "DEBUG: get_output_dir"
    # intersection = (link.get('tags').split(',') and firstleveltags)
    # if intersection != None:
    #     firstleveltag = intersection[0]
    # else:
    #     firstleveltag = "other"

    # intersection = (link.get('tags').split(',') and secondleveltags)
    # if intersection != None:
    #     secondleveltag = intersection[0]
    # else:
    #     secondleveltag = "other"

    # linktype = get_link_type(link.get('href'), link.get('tags').split(','))

    linktags = link.get('tags')  #TODO: move this to a separate function, call it everytime link.get('tags') is needed
    if linktags is None:
        linktags = list()
    else:
        linktags = linktags.split(',')

    linktags = link.get('tags')
    if linktags is None:
        linktags = list()
    else:
        linktags = linktags.split(',')

    linktype = get_link_type(link.get('href'), linktags)
    firstleveltag = get_tag(linktags, firstleveltags)
    secondleveltag = get_tag(linktags, secondleveltags)
    return "%s/%s/%s/%s" % (options.destdir, linktype, firstleveltag, secondleveltag)




def ytdl_media(link): #download a link using youtube-dl
    print "DEBUG: ytdl_media"

    outdir = get_output_dir(link)
    try:
        os.makedirs(outdir)
    except:
        pass

    call(["youtube-dl", "--no-playlist", "--continue", "--ignore-errors", "--console-title", "--add-metadata", "--format", "best", link.get('href')], cwd=outdir)




def ytdl_audio(link): #download a link using youtube-dl (audio only)
    print "DEBUG: ytdl_audio"

    outdir = get_output_dir(link)
    try:
        os.makedirs(outdir)
    except:
        pass

    call(["youtube-dl", "--no-playlist", "--continue", "--ignore-errors", "--console-title", "--add-metadata", "--format", "bestaudio", link.get('href')], cwd=outdir)



def wget_dl(link): #download a web page (TODO)
    print "DEBUG: NOT IMPLEMENTED YET"




def gen_download_queue(links): #generate list of links to download
    print "DEBUG: gen_download_queue"
    downloadqueue = list()
    for item in links:
        if options.usertag:
            print "DEBUG: only downloading if tagged %s" % options.usertag
            print "DEBUG: item tags: %s" % item.get('tags') #TODO: BUG: replace all occurences of item.get('tags') with a function that returns an empty links if no tags found (currently it returns a NoneType)
            if options.usertag in item.get('tags') and no_download_tag not in item.get('tags'): #TODO: move the no_download_tag check to do_download_queue else markdown will not be generated
                downloadqueue.append(item)
        else:
            downloadqueue.append(item)

    print "DEBUG: Got %s elements" % len(downloadqueue)
    return downloadqueue



def get_links(): #extract links from HTML file
    print "DEBUG: get_links"
    rawdata = bookmarksfile.read()
    data = BeautifulSoup(rawdata)
    links = data.find_all('a') #list of all links

    return links


############################################################################

def main():
    print "DEBUG: main"
    links = get_links()
    downloadqueue = gen_download_queue(links)
    do_download_queue(downloadqueue)

############################################################################

main()
print "Done."
