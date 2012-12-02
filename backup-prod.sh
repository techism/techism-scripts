#!/bin/bash

for kind in techism2_event techism2_eventchangelog techism2_location techism2_organization techism2_setting techism2_tweetedevent auth_user django_openid_auth_useropenid auth_permission django_admin_log django_content_type
do
  appcfg.py download_data \
    --application=techism2 \
    --url=https://techism2.appspot.com/remote_api \
    --config_file=conf/bulkloader.yaml \
    --log_file=log-prod/appcfg_download_data_${kind}_log.log \
    --db_file=log-prod/appcfg_download_data_${kind}_progress.sql3 \
    --result_db_filename=log-prod/appcfg_download_data_${kind}_result.sql3 \
    --filename=data-prod/${kind}.csv \
    --kind=${kind}
done

