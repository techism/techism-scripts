#!/bin/bash

for kind in techism2_event techism2_organization 
do
  appcfg.py download_data \
    --application=techism2 \
    --url=http://techism2.appspot.com/remote_api \
    --config_file=bulkloader.yaml \
    --log_file=${TMPDIR}appcfg_download_data_${kind}_log.log \
    --db_file=${TMPDIR}appcfg_download_data_${kind}_progress.sql3 \
    --result_db_filename=${TMPDIR}appcfg_download_data_${kind}_result.sql3 \
    --filename=backups/${kind}.csv \
    --kind=${kind}
done

