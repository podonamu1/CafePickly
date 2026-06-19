import math as m
from app.services.ai_service import generate_ai_summary
from app.services.ai_service import generate_dummy_summary
from app.services.kakao_service import search_cafes_from_kakao
from app.utils.franchise_filter import FRANCHISE_KEYWORDS

FRANCHISE_KEYWORDS = [
    "스타벅스", "투썸", "할리스", "이디야", "커피빈", "파스쿠찌",
    "메가MGC", "메가커피", "컴포즈", "빽다방", "더벤티",
    "우지커피", "발도스커피", "텐퍼센트", "커피에반하다",
    "카페봄봄", "하삼동커피", "매머드커피", "감성커피",
    "커피베이", "엔제리너스", "폴바셋", "샌두", "더무인"
]

def is_franchise(name:str) -> bool:
    for brand in FRANCHISE_KEYWORDS:
        if brand in name:
            return True
    return False

def calculate_score(cafe):
    radius = 1000

    # 거리
    score_dist = max(0, 1 - (cafe["distance"] / radius))

    # 평점
    basic_score_rating = max(0, min((cafe["rating"] - 3.5) / 1.5, 1))
    score_min_review_count = min(m.log(1 + cafe["review_count"]) / m.log(1 + 50), 1)
    score_rating = basic_score_rating * score_min_review_count

    # 리뷰 수
    score_review_count = min(m.log(1 + cafe["review_count"]) / m.log(1 + 500), 1)

    # 최종 점수
    score = 1.00 * score_dist + 0.35 * score_rating + 0.25 * score_review_count


    return round(score, 4)


def get_recommend_cafes(lat: float, lon: float, radius: int = 1000, limit: int = 5):
    print("NEW GETCAFE")

    docs = search_cafes_from_kakao(
        query="카페",
        x = lat,
        y = lon,
        radius = radius,
        size = 15
    )

    cafes = [ ]
    
    # 점수 계산 + 정렬
    for doc in docs:
        name = doc.get("place_name", "")

        distance_str = doc.get("distance")

        try:
            distance = int(distance_str) if distance_str is not None else 999999
        except ValueError:
            distance = 999999

        if is_franchise(name):
            continue

        cafe = {
            "place_id": doc.get("id"),
            "name": name,
            "address": doc.get("road_address_name") or doc.get("address_name"),
            "x": float(doc.get("x")),
            "y": float(doc.get("y")),
            "distance": distance,
            "rating": 0.0,
            "review_count": 0,
            "place_url": doc.get("place_url")
        }

        raw_score = calculate_score(cafe)
        score = round(100 * raw_score, 1)

        cafe["score"] = score
        cafe["summary"] = generate_dummy_summary(cafe)
        cafes.append(cafe)


    cafes.sort(key = lambda x: x["score"], reverse = True)
    return cafes[:limit]

