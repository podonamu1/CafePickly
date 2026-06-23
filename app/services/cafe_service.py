import requests
import math as m
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.cafe import Cafe

from app.services.ai_service import generate_ai_summary
from app.services.ai_service import generate_dummy_summary, is_summary_expired
from app.services.kakao_service import search_cafes_from_kakao
from app.utils.franchise_filter import is_franchise

async def get_or_create_summary(cafe, db):
    # 1. 기존 요약 있고 TTL 안 지났으면 그대로 사용
    if cafe.ai_summary and not is_summary_expired(cafe.summary_updated_at):
        return cafe.ai_summary

    # 2. TTL 지났거나 요약 없으면 새로 생성
    new_summary = generate_dummy_summary(cafe)

    # 3. DB 에 저장
    cafe.ai_summary = new_summary
    cafe.summary_updated_at = datetime.now(timezone.utc)

    db.add(cafe)
    db.commit()
    db.refresh(cafe)

    return new_summary

def calculate_score(cafe):
    radius = 1000

    # 거리
    if cafe["distance"] <= 100:
        score_dist = 1.0
    else:
        score_dist = max(0, 1 - ((cafe["distance"] - 100) / (radius - 100)) ** 0.7)

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

        # 프랜차이즈 여부 검사
        if is_franchise(name):
            continue

        # 커피숍 아닌 카페 제거
        category = doc.get("category_name", "")
        name = doc.get("place_name", "")

        if not category.startswith("음식점 > 카페"):
            continue

        EXCLUDE_KEYWORDS = [
            # 동물/펫
            "애견", "반려견", "반려동물", "강아지카페", "고양이카페", "동물카페",
            "펫카페", "펫동반", "펫 동반",

            # 놀이/체험형
            "보드게임카페", "보드게임", "만화카페", "키즈카페", "방방",
            "실내놀이터", "VR카페", "VR", "플스방", "닌텐도", "멀티방", "DVD방",

            # 공부/업무형
            "스터디카페", "스터디룸", "독서실", "공유오피스", "코워킹",

            # 휴식/찜질/마사지형
            "수면카페", "낮잠카페", "찜질카페", "찜질방", "좌욕", "족욕",
            "마사지", "안마", "스파", "힐링센터",

            # 룸/특수 목적
            "룸카페", "파티룸", "공간대여",

            # 운세/성인/흡연
            "타로카페", "사주카페", "운세", "흡연카페", "전자담배",
        ]

        if any(keyword in name for keyword in EXCLUDE_KEYWORDS):
            continue

        cafe = {
            "place_id": doc.get("id"),
            "place_name": doc.get("place_name"),
            "category_name": doc.get("category_name"),
            "address_name": doc.get("address_name"),
            "road_address_name": doc.get("road_address_name"),
            "phone": doc.get("phone"),
            "place_url": doc.get("place_url"),
            "x": float(doc.get("x")),
            "y": float(doc.get("y")),
            "distance": distance,
            "rating": 0.0,
            "review_count": 0,
            "is_franchise": is_franchise(doc.get("place_name", "")),
            "ai_summary": generate_dummy_summary(doc),
        }

        raw_score = calculate_score(cafe)
        score = round(100 * raw_score, 1)

        cafe["score"] = score
        cafe["ai_summary"] = generate_dummy_summary(doc)
        cafes.append(cafe)


    cafes.sort(key = lambda x: x["score"], reverse = True)
    return cafes[:limit]

def upsert_cafe(db: Session, item: dict) -> Cafe:
    print("UPSERT ITEM:", item)
    print("UPSERT ITEM KEYS:", item.keys())

    place_id = item.get("place_id")

    cafe = db.query(Cafe).filter(Cafe.place_id == place_id).first()

    if cafe is None:
        cafe = Cafe(place_id=place_id)
        db.add(cafe)

    cafe.place_name = item.get("place_name", "")
    cafe.category_name = item.get("category_name")
    cafe.address_name = item.get("address_name")
    cafe.road_address_name = item.get("road_address_name")
    cafe.phone = item.get("phone")
    cafe.place_url = item.get("place_url")
    cafe.x = float(item.get("x")) if item.get("x") is not None else None
    cafe.y = float(item.get("y")) if item.get("y") is not None else None
    cafe.distance = int(item.get("distance")) if item.get("distance") is not None else None
    cafe.is_franchise = is_franchise(item.get("place_name", ""))
    cafe.ai_summary = cafe.ai_summary or generate_dummy_summary(item)
    cafe.score = round(100 * calculate_score(item), 1)
    return cafe


def build_search_response(cafes: list, radius: int):
    count = len(cafes)

    if count == 0:
        suggested_radius = min(radius * 2, 5000)

        return {
            "count": 0,
            "low_result_count": True,
            "message": "검색 결과가 없어요. 반경을 넓히면 더 많은 후보를 볼 수 있어요.",
            "suggested_radius": suggested_radius,
            "cafes": []
        }

    if count < 3:
        suggested_radius = min(radius * 2, 5000)

        return {
            "count": count,
            "low_result_count": True,
            "message": "근처 카페가 적어요. 반경을 넓히면 더 많은 후보를 볼 수 있어요.",
            "suggested_radius": suggested_radius,
            "cafes": cafes,
        }

    return {
        "count": count,
        "low_result_count": False,
        "message": None,
        "suggested_radius": None,
        "cafes": cafes,
    }



def search_and_save_cafes(
    db: Session,
    query: str,
    x: float,
    y: float,
    radius: int = 1000,
    limit: int = 5,
) -> list[Cafe]:
    items = get_recommend_cafes(
        lat = x,
        lon = y,
        radius = radius,
        limit = limit,
    )

    cafes: list[Cafe] = []

    for item in items:
        cafe = upsert_cafe(db, item)

        if not cafe.is_franchise:
            cafes.append(cafe)

    db.commit()

    for cafe in cafes:
        db.refresh(cafe)
        
    return cafes


def cafe_to_response(cafe: Cafe) -> dict:
    return {
        "place_id": cafe.place_id,
        "place_name": cafe.place_name,
        "category_name": cafe.category_name,
        "address_name": cafe.address_name,
        "road_address_name": cafe.road_address_name,
        "phone": cafe.phone,
        "place_url": cafe.place_url,
        "x": cafe.x,
        "y": cafe.y,
        "distance": cafe.distance,
        "is_franchise": cafe.is_franchise,
        "ai_summary": cafe.ai_summary,
        "created_at": cafe.created_at,
        "updated_at": cafe.updated_at,
        "score" : cafe.score,
    }


