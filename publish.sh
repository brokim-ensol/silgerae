#!/bin/bash
# check if the container is running
if [ "$(docker ps -a -f name=silgerae)" ]; then
    echo "=> Copying the database file to the host"
    docker cp silgerae:/opt/myproject/db/silgerae.db /volume1/homes/brokim/silgerae/db
    echo "=> Removing the container"
    docker rm -f silgerae
fi
# check if the image exists
if [ "$(docker images -q silgerae)" ]; then
    echo "=> Removing the image"
    docker rmi silgerae
fi
echo "=> Pulling the latest changes from the repository"
git pull
echo "=> Building the image"
docker build -t silgerae --file Dockerfile_silgerae .
echo "=> Running the container"
docker run -d -p 8000:8000 --name silgerae silgerae
echo "=> Done"