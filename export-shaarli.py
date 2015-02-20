#!/usr/bin/python
#
# -*- coding: utf8 -*-
#
#Description: backup bookmark exports (netscape HTML format) from a Shaarli (https://github.com/shaarli/Shaarli)
#Copyright: (c) 2014 nodiscc <nodiscc@gmail.com>
#License: MIT
#Requires: python-bs4 python-requests
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


import os
import sys
import time
from optparse import OptionParser
import requests
from bs4 import BeautifulSoup

#### Parse command line options

parser = OptionParser()
parser.add_option("--username", dest="username",
                action="store", type="string",
                help="username for HTML and private links export", metavar="USERNAME")
parser.add_option("--password", dest="password",
                action="store", type="string",
                help="password for HTML and private links export", metavar="PASSWORD")
parser.add_option("-d", "--download-dir", dest="downloaddir",
                action="store", type="string",
                help="destination directory for bookmark backups")
parser.add_option("-u", "--url", dest="url",
                action="store", type="string",
                help="URL of your Shaarli (https://my.example.com/links)", metavar="URL")
parser.add_option("-t", "--type", dest="linktype",
                action="store", type="string",
                help="download links of TYPE (public, private or all)", metavar="TYPE")

(options, args) = parser.parse_args()


#### Some checks
if options.url is None:
    parser.print_help()
    parser.error('no URL specified')
    exit(1)

if options.downloaddir is None:
    parser.print_help()
    parser.error('no destination directory specified')
    exit(1)

if options.linktype not in ["public", "private", "all"]:
    parser.print_help()
    parser.error('please specify a type for your exported links: public, private or all')

downloaddir_exists = os.access(options.downloaddir, os.F_OK)
if downloaddir_exists == False:
    os.makedirs(options.downloaddir)

curdate = time.strftime('%Y-%m-%d_%H%M')
outfilename = options.downloaddir + "bookmarks-all_" + curdate + ".html"

#### Open a session to store the cookie, get the login page, and extract the token from HTML
fetcher = requests.Session()
response=fetcher.get(options.url + '/?do=login', verify=False)
html = BeautifulSoup(response.text)
html_token = html.find_all('input', { "name" : "token" })
token = html_token[0].get('value')


#### post login data and cookie to the login page
data = {"login": options.username, "password": options.password, "token": token}
response = fetcher.post(options.url + '/?do=login', data=data, verify=False) #TODO: use verify=false only if specified in options


#Get bookmarks
response = fetcher.get(options.url + '?do=export&what=' + options.linktype, verify=False)
outfile = open(outfilename, 'w+')
outfile.write(response.text.encode('utf-8'))
outfile.close

print "bookmark export written to %s !" % outfilename