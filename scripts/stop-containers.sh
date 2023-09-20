#!/bin/bash

#docker stop app_server database
#docker rm app_server database

STR=`docker ps`
SUB1='server_app'
SUB2='database'
if [[ "$STR" == *"$SUB1"* ]]; then
	docker stop ${SUB1}
	docker rm ${SUB1}	
fi

if [[ "$STR" == *"$SUB2"* ]]; then
        docker stop ${SUB2}
        docker rm ${SUB2}
fi

sudo rm -r /home/ubuntu/production_backend/
mkdir /home/ubuntu/production_backend/

#docker-compose -f /home/ubuntu/production_backend/docker-compose.yml up -d

