# saikiran_assignement
mkdir -p data
cp "/Users/saikiran/Downloads/nyc/test.csv" data/

docker-compose down
docker-compose build --no-cache
docker-compose up