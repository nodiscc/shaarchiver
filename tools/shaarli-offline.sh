#!/bin/bash
set -o errexit
set -o nounset

#source beammedown.conf
remotehost="telecom"
remote_shaarli_dir="/var/www/links/"

SHAARLI_LOCAL_PORT=7431

_CBSyncShaarli() {
remote_temp_dir=$(ssh $remotehost mktemp -d)
remote_ssh_user=$(ssh $remotehost whoami)
ssh "$remotehost" sudo cp -r "$remote_shaarli_dir" "$remote_temp_dir"
ssh "$remotehost" sudo chown -R "$remote_ssh_user":"$remote_ssh_user" "$remote_temp_dir"
scp -r "$remotehost":"$remote_temp_dir" local-shaarli
ssh "$remotehost" rm -r "$remote_temp_dir"

#rsync -avzP  ${NZ_FQDN}:/${NZ_APACHE_DOCUMENTROOT}/${NZ_SHAARLI_PATH}/ backups/
}

_CBServeShaarli() {
cd local-shaarli/
php -S localhost:${SHAARLI_LOCAL_PORT}
echo "Please go to http://localhost:${SHAARLI_LOCAL_PORT}"
}

_CBSyncShaarli
_CBServeShaarli
