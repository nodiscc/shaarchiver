# shaarchiver
Archive your [Shaarli](https://github.com/sebsauvage/Shaarli) or [delicious](https://delicious.com) bookmarks.
Status: **draft**. Use at your own risk

 * Supports local Shaarli/delicious bookmark exports (Netscape HTML format)
 * Supports downloading exports from your own Shaarli install
 * Downloads all linked media for archiving, backup, offline use...

### Installation
 * `git clone https://github.com/nodiscc/shaarchiver` or download and extract the [zip archive](https://github.com/nodiscc/shaarchiver/archive/master.zip)
 * install the required python modules: `python-bs4 python-requests`


#### Usage
Edit the config variables at the beginning of bookmarks-fetcher.py if needed.

    ./export-shaarli.py #download HTML export from your shaarli
    ./bookmarks-fetcher.py #download and archive pages/media in your HTML export

```
 ↳ ./export-shaarli.py -h
Usage: export-shaarli.py [options]

Options:
  -h, --help            show this help message and exit
  --username=USERNAME   username for HTML and private links export
  --password=PASSWORD   password for HTML and private links export
  -d DOWNLOADDIR, --download-dir=DOWNLOADDIR
                        destination directory for bookmark backups
  -u URL, --url=URL     URL of your Shaarli (https://my.example.com/links)
  -t TYPE, --type=TYPE  download links of TYPE (public, private or all)


```

```
 ↳ ./bookmarks-fetcher.py -h
Usage: bookmarks-fetcher.py [options]

Options:
  -h, --help            show this help message and exit
  -t TAG, --tag=TAG     download files only for specified TAG
  -f FILE, --file=FILE  source HTML bookmarks FILE
  -d DIR, --destination=DIR
                        destination backup DIR
  -m, --markdown        create a summary of files with markdown
  -n, --no-download     do not download files

```

#### Bugs/feature requests/discussion
 * https://github.com/nodiscc/shaarchiver/issues/

