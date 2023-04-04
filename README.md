# shaarchiver

**DEPRECATED** use [python-shaarli-client](https://github.com/shaarli/python-shaarli-client/) and [hecat](https://github.com/nodiscc/hecat) instead:

```bash
# install requirements
sudo apt install python3-venv python3-pip
# create a python virtualenv
python3 -m venv ~/.venv
# activate the virtualenv
source ~/.venv/bin/activate
# install the shaarli API client and hecat
pip3 install shaarli-client git+https://gitlab.com/nodiscc/hecat.git
# create configuration file for the API client
mkdir -p ~/.config/shaarli/ && nano ~/.config/shaarli/client.ini
```
```ini
[shaarli]
url = https://links.example.org
secret = AAAbbbZZZvvvSSStttUUUvvVXYZ
```
```bash
# download data from the API to a file
shaarli --outfile shaarli-export.json get-links --limit=all
# create configuration file for hecat
nano .hecat.yml
```
```yaml
steps:
  - name: import data from shaarli API JSON
    module: importers/shaarli_api
    module_options:
      source_file: shaarli-export.json
      output_file: shaarli.yml
      skip_existing: True # (default True) skip importing items whose 'url:' already exists in the output file
      clean_removed: False # (default False) remove items from the output file, whose 'url:' was not found in the input file
      sort_by: created # (default 'created') key by which to sort the output list
      sort_reverse: True # (default True) sort the output list in reverse order

- name: download video files
    module: processors/download_media
    module_options:
      data_file: shaarli.yml # path to the YAML data file
      only_tags: ['video'] # only download items tagged with all these tags
      exclude_tags: ['nodl'] # (default []), don't download items tagged with any of these tags
      output_directory: '/path/to/video/directory' # path to the output directory for media files
      download_playlists: False # (default False) download playlists
      skip_when_filename_present: True # (default True) skip processing when item already has a 'video_filename/audio_filename': key
      retry_items_with_error: True # (default True) retry downloading items for which an error was previously recorded
      use_download_archive: True # (default True) use a yt-dlp archive file to record downloaded items, skip them if already downloaded

  - name: download audio files
    module: processors/download_media
    module_options:
      data_file: shaarli.yml
      only_tags: ['music']
      exclude_tags: ['nodl']
      output_directory: '/path/to/audio/directory'
      only_audio: True # (default False) download the 'bestaudio' format instead of the default 'best'

  - name: check URLs
    module: processors/url_check
    module_options:
      source_files:
        - shaarli.yml
      check_keys:
        - url
      errors_are_fatal: True
      exclude_regex:
        - '^https://www.youtube.com/watch.*$' # don't check youtube video URLs, always returns HTTP 200 even for unavailable videos

- name: export shaarli data to HTML table
    module: exporters/html_table
    module_options:
      source_file: shaarli.yml # file from which data will be loaded
      output_file: index.html # (default index.html) output HTML table file
      html_title: "Shaarli export - shaarli.example.org" # (default "hecat HTML export") output HTML title
      description_format: paragraph # (details/paragraph, default details) wrap the description in a HTML details tag
```
```bash
# run the program
hecat -c .hecat.yml
```


See https://github.com/nodiscc/hecat#examples
