#!/usr/bin/python
#
# -*- coding: utf8 -*-
#TODO: detect if bookmarks filename has correct format
#TODO: support plain text (not html) lists

#TODO: stream action: just play each element in mplayer using youtube-dl (do not download, play only)
#TODO: mkplaylist action: same as stream, but just output the media urls to an .m3u file
#TODO: markdown action: just send the relevant links to a nice markdown file, and convert it to HTML also

#TODO: fetch raw webpages for some predefined tags (doc, news, lecture, alire, wiki), see https://superuser.com/questions/55040/save-a-single-web-page-with-background-images-with-wget
#TODO: if link has a numeric tag (d1, d2, d3) and one of the above, recursively follow links restricted to the domain/directory and download them.
#TODO: for tag 'images', download images embedded in pages (use patterns like wp-contents/uploads/*.jpg, i.imgur.com/*.jpg)

#TODO: add a command line switch to use mp3 output (best by default)
#TODO: BUG: output path generation is broken
#TODO: write a list of URLs fo which downloading has failed
#TODO: check if usertag option works as expected

import os
import sys
import time
import glob
import re
from bs4 import BeautifulSoup
from subprocess import call
from optparse import OptionParser


###############################
firstleveltags = ["lecture", "doc", "music", "musique", "video"]
secondleveltags = ["books", "cuisine", "blues", "hiphop", "electronic", "shortfilm", "documentaire", "films"]
download_media_for = ["musique", "music", "video", "samples"] #download multimedia content for these links
extract_audio_for = ["samples", "music"] #only get audio (not video) links tagged with these tags
no_download_tag = "nodl" #item will not be downloaded (external link only)

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
    parser.print_help()
    parser.error('No destination dir specified')
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


#TODO: Generate markdown
#def gen_markdown():
    #Base vars
    #curdate = time.strftime('%Y-%m-%d_%H%M') #date
    #markdownoutfile = downloaddir + "/" + "links-" + curdate + ".md" #markdown output file
    #print "DEBUG: gen_markdown"
    #outitem = " * [" + item.contents[0] + "](" + item.get('href') + ")" + " `@" + item.get('tags') + "`"
    #print outitem


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



def get_tag(linktags, taglist): #find item's first and second level tags (broken?)
    intersection = (linktags and taglist)
    if len(intersection) > 0:
        firstleveltag = intersection[0]
    else:
        firstleveltag = "other"

    return firstleveltag



def download_link(link): #elect the appropriate download cation for the link
    print "DEBUG: download_link"
    print ' * Downloading %s [%s]' % (link.contents[0], link.get('href'))
    
    linktags = link.get('tags')
    if linktags is None:
        linktags = list()
    else:
        linktags = linktags.split(',')

    type = get_link_type(link.get('href'), linktags)
    firstleveltag = get_tag(linktags, firstleveltags)
    secondleveltag = get_tag(linktags, secondleveltags)
    if type == "media":
        ytdl_media(link)
    elif type == "audio":
        ytdl_audio(link)
    elif type == "page":
        wget_dl(link)

    print "DEBUG: Type is %s" % type




def do_download_queue(downloadqueue): #start markdown generation and download process if appropriate
    print "DEBUG: do_download_queue"
    #if options.markdown:
        #gen_markdown(downloadqueue)

    if options.download:
        print "DEBUG: Downloading %s items" % len(downloadqueue)
        for item in downloadqueue:
            download_link(item)
    else:
        print "Downloading disabled, skipping."




def get_output_dir(link): #generate an output path based on tags (broken?)
    #should be options.destdir/linktype/firstleveltag/secondleveltag/
    print "DEBUG: get_output_dir"
    intersection = (link.get('tags').split(',') and firstleveltags)
    if intersection != None:
        firstleveltag = intersection[0]
    else:
        firstleveltag = "other"

    intersection = (link.get('tags').split(',') and secondleveltags)
    if intersection != None:
        secondleveltag = intersection[0]
    else:
        secondleveltag = "other"

    linktype = get_link_type(link.get('href'), link.get('tags').split(','))

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
    print "DEBUG: FSCK OFF"




def gen_download_queue(links): #generate list of links to download
    print "DEBUG: gen_download_queue"
    downloadqueue = list()
    for item in links:
        if options.usertag in locals():
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


