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



import os
import sys
import time
from bs4 import BeautifulSoup
from subprocess import call
from optparse import OptionParser


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
extractaudio = True
parser.add_option("--no-extract-audio", dest="extractaudio",
                action="store_false",
                help="do not extract audio from downloaded music")
#TODO: add a command line switch to use mp3 output (best by default)

(options, args) = parser.parse_args()



#Base vars
bookmarksfile = open(options.bookmarksfilename)
rawdata = bookmarksfile.read()
data = BeautifulSoup(rawdata)
links = data.find_all('a')
curdate = time.strftime('%Y-%m-%d_%H%M')
downloaddir = options.destdir + "/" + options.usertag
markdownoutfile = downloaddir + "/" + "links-" + curdate + ".md"

#Check and create files/directories
downloaddir_exists = os.access(downloaddir, os.F_OK)
if downloaddir_exists == False:
    os.makedirs(downloaddir)





os.chdir(downloaddir)
#Catch em all
print '[html extractor] Getting files tagged %s...' % options.usertag
for item in links:
    if options.usertag in item.get('tags') and 'nodl' not in item.get('tags'):
        print ' * Downloading %s [%s]' % (item.contents[0], item.get('href'))

        #Output markdown if needed #TODO
        if options.markdown == True:
            outitem = " * [" + item.contents[0] + "](" + item.get('href') + ")" + " `@" + item.get('tags') + "`"
            print outitem #TODO: print to outfile


        if extractaudio == True:
            if options.usertag == 'music' or options.usertag == 'musique':
                call(["youtube-dl", "-q", "--console-title", "--add-metadata",
                    "--extract-audio", "--audio-quality", "0", item.get('href')])


        else:
            call(["youtube-dl", "-q", "--console-title",  "--add-metadata", item.get('href')])
            #TODO: output a file containing URLs for which youtube-dl failed

