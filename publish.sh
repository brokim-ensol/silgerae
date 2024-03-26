docker cp silgerae:/opt/myproject/db/silgerae.db /volume1/homes/brokim/silgerae/db
docker rm -f silgerae
docker rmi silgerae
docker build -t silgerae --name Dockerfile_silgerae .
docker run -d -p 8000:8000 --name silgerae2 silgerae