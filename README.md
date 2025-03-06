# Meadow Exercise

This is a simple FastAPI app with one Inngest function that listens for "movie.watched" events and sends an email of the plot to the recipient.


## Assumptions

- The movie title is expected to be an exact match to the title in the OMDb API. Presumably the "move.watched" event would be downstream of a movie selection event, so the title would be known.
- The recipient email is expected to be a valid email address. That is, email address validation, and guaranteeing a valid email address, are handled at user signup.
- OMDb API usage assumes a per-minute rate limit, retrying again in 30 minutes. This delay also assumes that the email does not need to be timely, otherwise it would be better to communicate an error to the user.
- This email type is assumed to be used occasionally, so emails are rate limited to 1 per minute to prevent accidental spamming.
- Apart from rate limiting, identical emails to the same user (same movie) are allowed, and each event is treated as new. If this is not the desired behavior, a unique id (idempotency key) should be included in the event.


## Exercise Improvements

Overall, this exercise seemed well-scoped. However, it could have been expanded into a scenario that involved a delayed function, like a follow-up email, or a case where an additional event is triggered. Alternatively, there could be an opportunity to test the applicant's conversion of a product use-case into a part of a system by leaving it more open-ended.

Note: As a quick exercise, using TypeScript and Vercel would be a much quicker way to get runtime type validation and a working deployment up and running given the support that Inngest provides for both. Plus, the TypeScript SDK's support for testing is first class. You may wish to communicate this discrepancy between using Python and using TypeScript.


## Steps to run locally

### Setup

Prerequisites: You will need [Docker](https://docs.docker.com/get-started/introduction/get-docker-desktop/) and Python 3 installed.

First clone this repo, then install the dependencies (using `venv` is recommended):
```
pip install -r requirements.txt
```

Add a `.env` file in the project root and add your API keys as environment variables:
```
OMDB_API_KEY=add_your_key_here  # from https://www.omdbapi.com
RESEND_API_KEY=add_your_key_here  # from https://resend.com
```


### Run Services and Verify

Run the Inngest dev server image with Docker:
```
docker run -p 8288:8288 inngest/inngest \
  inngest dev -u http://host.docker.internal:8000/api/inngest --no-discovery
```

With the docker service running, in a separate terminal run the app (in development mode):
```
(INNGEST_DEV=1 uvicorn main:app --reload)
```

Access Inngest Dev Server UI at `http://localhost:8288` and send a test event, such as:
```
{
  "name": "meadow_api/movie.watched",
  "data": {
    "movie_title": "The Matrix",
    "recipient_email": "tester@email.com"
  }
}
```

If all is working well, a _run_ should appear in the dashboard, and eventually show as "Completed".


## Future Improvements

* Resend webhooks could be used to handle the "email.bounced" event, and prevent further emails to the associated address. This would help maintain the sender reputation for the domain.

* Resend email sending and the wait_for_event() are both blocking steps, and could potentially be optimized as separate functions. Although, my understanding is that Inngest already handles "wait_for_event" in a way that does not impact step concurrency.


## Deploying and Running in the Cloud

To run in the cloud, you will need to add the following environment variables to your cloud provider:
```
INNGEST_EVENT_KEY=add_your_key_here
INNGEST_SIGNING_KEY=add_your_key_here
```

And the function server will need to be deployed so that it is publicly accessible.
