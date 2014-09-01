# warchiver
A web scraper to archive your [Shaarli](https://github.com/sebsauvage/Shaarli) or [delicious](https://delicious.com) bookmarks 


## Offline mode
* Downloads a backup of your Shaarli/delicious bookmarks (bookmarks.html file) or uses another local HTML/text file.
* Downloads all linked media/pages.
* Generates a nice, portable html page of all your links, with search/filtering (#TODO: http://www.ecyseo.net/article36/filtrer-une-liste-en-pur-javascript-et-sans-jquery)
* Your bookmarks and data are ready for **full offline access**.

TODO add screenshots

## local PHP mode
 * Downloads a copy of your Shaarli instance over SFTP
 * Runs Shaarli locally with full functionality using the the PHP command line tool (`php-cli`).

```
$ ./tools/shaarli-offline.sh 
PHP 5.6.0RC4 Development Server started at Mon Sep  1 21:56:19 2014
Listening on http://localhost:7431
Document root is /home/bsp/git/cloudbackup/backups/links
Press Ctrl-C to quit.

[Mon Sep  1 21:56:27 2014] ::1:57868 [200]: /
[Mon Sep  1 21:56:27 2014] ::1:57869 [200]: /index.html
[Mon Sep  1 21:56:37 2014] ::1:57881 [200]: /...
```

Resource usage:
