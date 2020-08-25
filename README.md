# shaarchiver

Archive your Firefox, [Shaarli](https://github.com/shaarli/Shaarli) or [delicious](https://delicious.com) bookmarks.

**This project will not be maintained anymore.** The same results can be achieved using Shaarli's [REST API](https://shaarli.github.io/api-documentation/), [python-shaarli-client](https://python-shaarli-client.readthedocs.io/en/latest/), [jq](https://stedolan.github.io/jq/) and basic shell pipes. For example:

- get your Shaarli API token from https://shaarli.myexample.org/?do=configure
- create a configuration file for the shaarli API client

```ini
# nano ~/.config/python-shaarli-client.ini
[shaarli]
url = https://shaarli.myexample.org
secret = mYS3CR3t
```
- install the shaarli API client and requirements

```bash
$ sudo apt install python3-venv python3-pip jq youtube-dl ffmpeg
$ python3 -m venv ~/.local/venv
$ source ~/.local/venv/bin/activate
$ pip3 install https://github.com/shaarli/python-shaarli-client/archive/master.zip
```
- configure youtube-dl

```ini
# nano ~/.config/youtube-dl/video.config
--continue
--output '/path/to/videos/directory/%(uploader)s-%(title)s-%(id)s-%(extractor)s.%(ext)s'
--write-sub
--write-auto-sub
--write-info-json

# nano ~/.config/youtube-dl/music.config
--extract-audio
--continue
--output '/path/to/music/directory/%(uploader)s-%(title)s-%(id)s-%(extractor)s.%(ext)s'
--write-sub
--write-auto-sub
--write-info-json
```

- download videos for all shaares tagged "video"

```bash
$ source ~/.local/venv/bin/activate
$ shaarli --config ~/.config/python-shaarli-client.ini get-links --limit all --searchtags video | jq ".[].url" | sed 's/"//g' | youtube-dl --config-location ~/.config/youtube-dl/video.config --batch-file -
```

- download videos for all shaares tagged "music"

```bash
$ source ~/.local/venv/bin/activate
$ shaarli --config ~/.config/python-shaarli-client.ini get-links --limit all --searchtags music | jq ".[].url" | sed 's/"//g' | youtube-dl --config-location ~/.config/youtube-dl/music.config --batch-file -
```

Other examples could be added (for example how to download webpages using `wget`, how to create an index.html page...). Have a look at [ArchiveBox](https://github.com/pirate/ArchiveBox) if you're looking for full-fledged archiveing capabilities (it supports Shaarli Netscape HTML exports as a source).