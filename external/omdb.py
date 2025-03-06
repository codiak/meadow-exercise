import os
import httpx
from inngest import NonRetriableError, RetryAfterError

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
client = httpx.AsyncClient()


async def get_movie_plot(title: str) -> str:
    """
    Get movie plot from OMDB API, for use as Inngest function.

    Args:
        title: Exact movie title to search for.
    """
    print("RUNNING!")
    if not OMDB_API_KEY:
        raise Exception("OMDB API key is missing!")

    omdb_param = f"&apikey={OMDB_API_KEY}"
    url = f"http://www.omdbapi.com/?t={title}&plot=full{omdb_param}"

    try:
        response = await client.get(url)
        response.raise_for_status()
    except httpx.HTTPError as e:
        if response.status_code == 429:
            # Explicitly backoff if rate limited
            raise RetryAfterError(f"OMDB API rate limit exceeded: {e}", "30m")
        elif response.status_code in [408, 500, 502, 503, 504]:
            # Other HTTP status codes that should be retried:
            raise Exception(f"OMDB API request failed (will retry): {e}")
        else:
            raise NonRetriableError(f"OMDB API request failed: {e}")

    data = response.json()
    if "Plot" not in data or data["Plot"] == "N/A":
        raise NonRetriableError(f"Plot not found for movie: {title}")

    return data["Plot"]
