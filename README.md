# AmendmentApp

```bash
docker pull mongodb/mongodb-community-server:latest
docker run --name mongodb -p 27017:27017 -d mongodb/mongodb-community-server:latest

#put amendment_data_set.json in src/init/
#network needed between containers (via docker-compose)
#docker build . -t amendementsapp
#docker run amendmentsapp -p 8000:8000
#instead use
pip install requirements.txt
pip install --upgrade pip && pip --no-cache-dir install -r requirements.txt
python src/main.py
```