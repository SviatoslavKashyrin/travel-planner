import httpx
from fastapi import HTTPException
from async_lru import alru_cache

ART_API_BASE = "https://api.artic.edu/api/v1/artworks"


@alru_cache(maxsize=100)
async def verify_place_exists(external_id: str) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ART_API_BASE}/{external_id}", timeout=5.0)
        except httpx.RequestError:
            raise HTTPException(
                status_code=502,
                detail="Error communicating with Art Institute API (Connection failed)"
            )

        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False


        raise HTTPException(
            status_code=502,
            detail=f"Error communicating with Art Institute API. Status code: {response.status_code}"
        )