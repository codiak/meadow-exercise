# Meadow Exercise

[to detail]

## Development: Running Locally

Run the app (function server):
```
(INNGEST_DEV=1 uvicorn main:app --reload)
```

Install [Docker](https://docs.docker.com/get-started/introduction/get-docker-desktop/), and run the Inngest Dev server:
```
docker run -p 8288:8288 inngest/inngest \
  inngest dev -u http://host.docker.internal:8000/api/inngest --no-discovery
```

Access Inngest Dev Server UI at `http://localhost:8288`.

Send a test event along the lines of:
```
{
  "name": "meadow_api/movie.watched",
  "data": {
    "movie_title": "The Matrix",
    "recipient_email": "codypumper@gmail.com"
  }
}
```
