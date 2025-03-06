import os
import httpx
import dotenv
from inngest import NonRetriableError

dotenv.load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_KEY")

async def get_movie_plot(title: str) -> str:
    if not OMDB_API_KEY:
        raise Exception("OMDB API key is missing!")

    omdb_param = f"&apikey={OMDB_API_KEY}"
    url = f"http://www.omdbapi.com/?t={title}{omdb_param}"

    try:
        # TODO: use async client
        response = httpx.get(url)
        response.raise_for_status()
    except httpx.HTTPError as e:
        # HTTP status codes that should be retried:
        if response.status_code in [408, 429, 500, 502, 503, 504]:
            raise Exception(f"OMDB API request failed (will retry): {e}")
        else:
            raise NonRetriableError(f"OMDB API request failed: {e}")

    data = response.json()
    if "Plot" not in data:
        raise NonRetriableError(f"Plot not found for movie: {title}")

    return data["Plot"]
