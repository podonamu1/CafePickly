# AI 설명 생성 전담
# 카페 정보 받아서 짧은 추천 문장 생성
# AI 붙이기 전: 임시 함수로 문자열 반환

def topic_marker(name: str) -> str:
    last = name[-1]
    code = ord(last) - ord("가")

    if 0 <= code <= 11171:
        jong = code % 28
        return "은" if jong else "는"

    return "은"

def generate_dummy_summary(cafe) -> str:
    name = cafe["name"]
    marker = topic_marker(name)
    distance = cafe["distance"]

    if distance <= 300:
        return f"{name}{marker} 현재 위치에서 매우 가까워 가볍게 들르기 좋은 카페입니다."
    elif distance <= 700:
        return f"{name}{marker} 도보로 방문하기 적당한 거리의 카페입니다."
    else:
        return f"{name}{marker} 조금 걸어야 하지만 반경 안에서 찾을 수 있는 카페입니다."

def generate_ai_summary(cafe) -> str:
    marker = topic_marker(cafe["name"])

    if cafe["rating"] >= 4.5:
        return f'{cafe["name"]}{marker} 평점이 높고 만족도가 좋은 카페입니다.'
    elif cafe["distance"] <= 300:
        return f'{cafe["name"]}{marker} 가까워서 가볍게 방문하기 좋은 카페입니다.'
    else:
        return f'{cafe["name"]}{marker} 무난하게 방문하기 좋은 카페입니다.'