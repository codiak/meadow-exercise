from datetime import timedelta
import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
import httpx

from external.omdb import get_movie_plot
from external.resend import send_email


inngest_client = inngest.Inngest(
    app_id="meadow_exercise",
    logger=logging.getLogger("uvicorn"),
)

# TODO: Type validation for message format
# {
#     "name": "meadow_api/movie.watched",
#     "data": {
#       "movie_title": "The Matrix", "recipient_email": "clem@test.com"
#     }
# }
@inngest_client.create_function(
    fn_id="movie_watched_email",
    trigger=inngest.TriggerEvent(event="meadow_api/movie.watched"),
)
async def movie_watched_email(ctx: inngest.Context, step: inngest.Step) -> None:
    data = ctx.event.data
    ctx.logger.info(data)
    title = data['movie_title']
    # TODO: Determine backoff/retry strategy
    plot = await step.run("Get Movie Plot", get_movie_plot, title)
    ctx.logger.info(plot)
    subject = f"Plot for {title}"
    status = await step.run("Send Email", send_email, data['recipient_email'], subject, plot)
    ctx.logger.info(status)

app = FastAPI()

# Serve Inngest endpoint
inngest.fast_api.serve(app, inngest_client, [movie_watched_email])
