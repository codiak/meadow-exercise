import dotenv
dotenv.load_dotenv()

from datetime import timedelta
import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest import NonRetriableError
import httpx

from models import MovieWatchedEvent
from external.omdb import get_movie_plot
from external.resend import send_email

RESEND_WEBOOKS = False

inngest_client = inngest.Inngest(
    app_id="meadow_exercise",
    logger=logging.getLogger("uvicorn"),
)


@inngest_client.create_function(
    fn_id="movie_watched_email",
    trigger=inngest.TriggerEvent(event=MovieWatchedEvent.name),
    rate_limit=inngest.RateLimit(
        # Prevent spamming the user
        limit=1,
        period=timedelta(minutes=1),
        key='event.data.recipient_email',
    ),
)
async def movie_watched_email(ctx: inngest.Context, step: inngest.Step) -> str:
    # Validate event data
    try:
        event = MovieWatchedEvent.from_event(ctx.event)
    except Exception as e:
        raise NonRetriableError(f"Invalid event data: {e}")
    data = event.data
    ctx.logger.debug(data)

    # Get plot (only pass title to leverage Inngest's memoization)
    plot = await step.run("Get Movie Plot", get_movie_plot, data.movie_title)
    ctx.logger.debug(plot)

    # Send email
    subject = f"Plot for {data.movie_title}"
    # If new inbox, "warmup" by using throttling
    email_id = await step.run("Send Email", send_email, data.recipient_email, subject, plot)

    if RESEND_WEBOOKS:
        # Configuration: https://www.inngest.com/docs/guides/resend-webhook-events
        await step.wait_for_event(
            "wait_for_email_sent",
            event="resend/email.sent",
            timeout=timedelta(seconds=10),
        )

    return f"Email sent: {email_id}"


app = FastAPI()

# Serve Inngest endpoint
inngest.fast_api.serve(app, inngest_client, [movie_watched_email])
