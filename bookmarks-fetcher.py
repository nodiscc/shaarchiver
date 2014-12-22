#!/usr/bin/python
#
#TODO: detect if bookmarks filename has correct format
#TODO: support plain text (not html) lists

#TODO: stream action: just play each element in mplayer using youtube-dl (do not download, play only)
#TODO: mkplaylist action: same as stream, but just output the media urls to an .m3u file
#TODO: markdown action: just send the relevant links to a nice markdown file, and convert it to HTML also

#TODO: fetch raw webpages for some predefined tags (doc, news, lecture, alire, wiki), see https://superuser.com/questions/55040/save-a-single-web-page-with-background-images-with-wget
#TODO: if link has a numeric tag (d1, d2, d3) and one of the above, recursively follow links restricted to the domain/directory and download them.
#TODO: for tag 'images', download images embedded in pages (use patterns like wp-contents/uploads/*.jpg, i.imgur.com/*.jpg)

#TODO: add a command line switch to use mp3 output (best by default)

import os
import sys
import time
from bs4 import BeautifulSoup
from subprocess import call
from optparse import OptionParser


###############################
first_level_tags = [lecture, doc, music, musique, video]
second_level_tags = [books, cuisine, blues, hiphop, electronic, shortfilm, documentaire, films]
extract_audio_for = [samples, music]
no_download_tag = "nodl"

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
# extractaudio = True
# parser.add_option("--no-extract-audio", dest="extractaudio",
#                 action="store_false",
#                 help="do not extract audio from downloaded music")


(options, args) = parser.parse_args()

###############################################################################

#Base vars
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

rawdata = bookmarksfile.read()
data = BeautifulSoup(rawdata)
links = data.find_all('a')
curdate = time.strftime('%Y-%m-%d_%H%M')
downloaddir = options.destdir + "/" + options.usertag
markdownoutfile = downloaddir + "/" + "links-" + curdate + ".md"

#Create files/directories
try:
    os.makedirs(downloaddir)
    os.makedirs(downloaddir + '/media/')




###############################################################################
#Catch em all

#os.chdir(downloaddir)

if 'options.usertag' in locals():
    mode = get_single_tag
else:
    mode = get_all_tags

if mode = get_single_tag:
    get_single_tag()
elif mode = get_all_tags:
    get_all_tags()


def gen_markdown():
    outitem = " * [" + item.contents[0] + "](" + item.get('href') + ")" + " `@" + item.get('tags') + "`"
    print outitem #TODO: print to outfile



def get_single_tag():
    print '[html extractor] Getting files tagged %s...' % options.usertag

    #for each item, define if it has the specified tag, if yes, add it to the download queue


    for item in links:
        if options.usertag in item.get('tags') and no_download_tag not in item.get('tags'):
            #todo: generate a download_queue list first, call this later on every item of download_queue
            print ' * Downloading %s [%s]' % (item.contents[0], item.get('href'))




            #find item type
            #if it is in list of yt-dl supported sites 
                #TODO: list of yt-dl supported domains
                #TODO: match url against the list
                #and in is tagged with the extract_audio_for tag
                    #then type=audio
                #else type=media
            #else it's not in yt-dl supported sites, type=page

            #define item's output dir
            #if it has type=media or audioduse media as 0-level dir, else use pages
            #https://stackoverflow.com/questions/3697432/python-how-to-find-list-intersection
            #if it has one tag that matches an item from the first_level_tags list, use this as first level
                #if it has one that matches an item in second_level_tag, use this as first level
                #else use other as second level
            #if it has no match, use other as first level

            #if type=audio, download and extract audio
            #if type=media, download with yt dl
            #if type=page, wget
            #for every type, generate markdown
            if options.markdown == True:
                gen_markdown()



            # if extractaudio == True:
            #     if options.usertag == 'music' or options.usertag == 'musique':
            #         call(["youtube-dl", "-q", "--continue", "--ignore-errors", "--console-title", "--add-metadata",
            #             "--extract-audio", "--audio-quality", "best", "-o", downloaddir + "/media/##### TTTTTAGGGGGG ######%(title)s-%(id)s.%(ext)" item.get('href')])
            #             # -f bestaudio should work

            # else:
            #     call(["youtube-dl", "-q", "--continue", "--ignore-errors", "--console-title",  "--add-metadata", item.get('href')])
            #     #TODO: output a file containing URLs for which youtube-dl failed

