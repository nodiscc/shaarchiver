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
shaarli get-links --limit=all >| shaarli-export.json
# create configuration file for hecat
nano .hecat.yml
```
```yaml
steps:
  - name: import data shaarli from shaarli API JSON
    module: importers/shaarli_api
    module_options:
      source_file: shaarli-export.json
      output_file: shaarli.yml
      skip_existing: True # optional, default True

  - name: download video files
    module: processors/download_media
    module_options:
      data_file: shaarli.yml
      only_tags: ['video']
      exclude_tags: ['nodl'] # optional, don't download items tagged with any of these tags
      output_directory: '/path/to/video/directory'
      download_playlists: False # optional, default False
      skip_when_filename_present: False # optional, default False
      retry_items_with_error: True # optional, default True

  - name: download audio files
    module: processors/download_media
    module_options:
      data_file: shaarli.yml
      only_tags: ['music']
      exclude_tags: ['nodl']
      output_directory: '/path/to/audio/directory'
      only_audio: True

  - name: check URLs
    module: processors/url_check
    module_options:
      source_files:
        - shaarli.yml
      check_keys:
        - url
      errors_are_fatal: True
```
```bash
# run the program
hecat -c .hecat.yml
```


See https://github.com/nodiscc/hecat#examples
