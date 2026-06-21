import requests
from app.core.config import settings

KAKAO_KEYWORD_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"

def search_cafes_from_kakao(query: str, x: float, y: float, radius: int = 1000, size: int = 15):
    headers = {
        "Authorization": f"KakaoAK {settings.KAKAO_REST_API_KEY}"
    }

    params = {
        "query": query,
        "x": x,
        "y": y,
        "radius": radius,
        "size": size,
        "sort": "distance"
    }

    response = requests.get(
        KAKAO_KEYWORD_URL,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data.get("documents", [])