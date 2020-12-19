# shaarchiver

Archive your bookmarks and their contents.

Supported sources:
- [Shaarli](https://github.com/shaarli/Shaarli) (using the REST API)

Output:
- Generates a single file HTML archive of your bookmarks
- Downloads videos and audio (using youtube-dl)

## Installation

```
# clone the repsotory
git clone https://gitlab.com/nodiscc/warchiver

# install requirements
sudo apt install python36venv python3-pip ffmpeg
cd warchiver
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt # https://github.com/shaarli/python-shaarli-client/archive/master.zip
```

## Configuration

Get your Shaarli API token from https://shaarli.myexample.org/?do=configure

```bash
# create a configuration directory
mkdir -p ~/.config/warchiver

# configure the the shaarli API client
nano ~/.config/warchiver/python-shaarli-client.ini
```

```ini
[shaarli]
url = https://shaarli.myexample.org
secret = mYS3CR3t
```

```bash
# configure youtube-dl
nano ~/.config/warchiver/youtube-dl.video.config
```

```ini
--continue
--output '/path/to/videos/download/directory/%(uploader)s-%(title)s-%(id)s-%(extractor)s.%(ext)s'
--write-sub
--write-auto-sub
--write-info-json
```

```bash
# you can define multiple configuration presets for archival tasks
nano ~/.config/youtube-dl/music.config
```

```ini
--extract-audio
--continue
--output '/path/to/music/download/directory/%(uploader)s-%(title)s-%(id)s-%(extractor)s.%(ext)s'
--write-sub
--write-auto-sub
--write-info-json
```

```bash
# configure archival tasks
nano ~/.config/warchiver/warchiver.yml
```

```yaml
TODO
```

## Usage TODO BELOW THIS POINT

Download videos for all shaares tagged "video"

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
