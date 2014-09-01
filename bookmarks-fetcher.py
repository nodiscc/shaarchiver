#!/usr/bin/python
import os
import sys
from bs4 import BeautifulSoup
from subprocess import call

destdir = sys.argv[1]

usertag = raw_input('Enter the tag you want to download media for (music, video...): ')
bookmarksfilename = raw_input('Enter the bookmarks.html filename you want to read: ') 
#TODO: pass options as command line arguments: -d destination_dir -t tag1 -t tag2 -f /path/to/bookmarks.html
#TODO: detect if bookmarks filename has correct format
#TODO: support plain text (not html) lists
#TODO: stream action: just play each element in mplayer using youtube-dl (do not download, play only)
#TODO: mkplaylist action: same as stream, but just output the media urls to an .m3u file
#TODO: markdown action: just send the relevant links to a nice markdown file, and convert it to HTML also
#TODO: fetch raw webpages for some predefined tags (doc, news, lecture, alire, wiki), see https://superuser.com/questions/55040/save-a-single-web-page-with-background-images-with-wget
#TODO: if link has a numeric tag (1, 2, 3) and one of the above, recursively follow links restricted to the domain/directory and download them.
#TODO: for tag 'images', download images embedded in pages (use patterns like wp-contents/uploads/*.jpg, i.imgur.com/*.jpg)
bookmarksfile = open(bookmarksfilename)
rawdata = bookmarksfile.read()
data = BeautifulSoup(rawdata)
links = data.find_all('a')

#Check and create directories
downloaddir = destdir + "/" + usertag
downloaddir_exists = os.access(downloaddir, os.F_OK)
if downloaddir_exists == False:
    os.makedirs(downloaddir)
os.chdir(downloaddir)

#Catch em all
print '[html extractor] Getting %s files...' % usertag
for item in links:
    if usertag in item.get('tags') and 'nodl' not in item.get('tags'):
        outitem = " * [" + item.contents[0] + "](" + item.get('href') + ")" + " `@" + item.get('tags') + "`"
        print outitem #TODO: print to outfile
        #TODO: add a command line switch to extract audio
        #TODO: add a command line switch to use mp3 output (best by default)
        if usertag == 'music' or usertag == 'musique':
            call(["youtube-dl", "--extract-audio", "--audio-quality", "0", item.get('href')])
        else:
            call(["youtube-dl", "--add-metadata", item.get('href')])
            #TODO: output a file containing URLs for which youtube-dl failed

