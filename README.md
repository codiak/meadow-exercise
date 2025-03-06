# Meadow Exercise

This is a simple FastAPI app with one Inngest function that listens for "movie.watched" events and sends an email of the plot to the recipient.


## Assumptions

- The movie title is an exact match to the title in the OMDb API. Presumably the "move.watched" event would be downstream of a movie selection event, so the title would be known.
- The recipient email is a valid email address. Email address validation, and guaranteeing a valid email address, should be handled at user signup.


## Exercise Improvements

The exercise seemed well scoped, but it would have been interesting to work on an expanded scenario that involved a delayed function, like a follow-up email, or a case where an additional event is triggered. Inngest provides some great flexibility out of the box.

As a quick exercise, using TypeScript and Vercel would be a much quicker way to get  runtime type validation and a working deployment up and running given the support that Inngest provides for both. Plus, the TypeScript SDK's support for testing is first class. You may wish to communicate the discrepancy when compared to the Python route.


## Steps to run locally

After cloning the repo, install the dependencies:
```
pip install -r requirements.txt
```

And add a `.env` file with the following environment variables:
```
OMDB_API_KEY=add_your_key_here  # from https://www.omdbapi.com
RESEND_API_KEY=add_your_key_here  # from https://resend.com
```

Install [Docker](https://docs.docker.com/get-started/introduction/get-docker-desktop/), and run the Inngest dev server image:
```
docker run -p 8288:8288 inngest/inngest \
  inngest dev -u http://host.docker.internal:8000/api/inngest --no-discovery
```

Run the app (in development mode):
```
(INNGEST_DEV=1 uvicorn main:app --reload)
```

Access Inngest Dev Server UI at `http://localhost:8288` and send a test event, such as:
```
{
  "name": "meadow_api/movie.watched",
  "data": {
    "movie_title": "The Matrix",
    "recipient_email": "codypumper@gmail.com"
  }
}
```


## Deploying and Running in the Cloud

To run in the cloud, you will need to add the following environment variables to your cloud provider:
```
INNGEST_EVENT_KEY=add_your_key_here
INNGEST_SIGNING_KEY=add_your_key_here
```
