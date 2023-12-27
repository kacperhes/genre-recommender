# Music Genre Recommender

A simple website that allows you to search different songs by tags that uses neo4j under the hood because of graph structure of music genres.

## Running database locally

> **_NOTE:_**  Make sure you've got docker installed on your machine.

1. Installing neo4j image 

```bash
docker pull neo4j
```

2. Running neo4j instance

```bash
docker run \
  --name songs-recommender-neo4j \
  --publish=7475:7474 \
  --publish=7688:7687 \
  --env NEO4J_AUTH=neo4j/password \
  --d \
  neo4j
```

## Adding env variables
```bash
touch .env
```
> **_NOTE:_**  Make sure to fill all env variables from `.env.template`

## Python venv

```bash
python -m venv venv
```

## Installing python dependencies for scripts and backend

```bash
pip3 install -r requirements.txt
```

## Running database seeding script

```bash
python3 scripts/database_seeder.py
```

## Running backend locally

```bash
python3 backend/app.py
```

## Running frontend locally

```bash
cd frontend
```

```bash
npm install
```

```bash
npm start
```

The app should be available under http://localhost:3000



