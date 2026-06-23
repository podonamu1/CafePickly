# CafePickly

CafePickly는 현재 위치를 기준으로 근처 카페를 추천해주는 FastAPI 기반 카페 추천 API입니다.

카카오 로컬 API를 이용해 주변 카페를 검색하고, 프랜차이즈 및 일부 특수 업종을 필터링한 뒤 거리와 자체 점수를 기준으로 추천 결과를 반환합니다.

## Features

* 주어진 위치 좌표 기반 카페 검색
* 카카오 로컬 API 연동
* 프랜차이즈 카페 필터링
* 애견카페, 보드게임카페 등 일부 특수 업종 제외
* 거리 기반 추천 점수 계산
* 카페 정보 DB 저장 및 업데이트
* 검색 결과 부족 시 추천 확장 반경 반환
* 카페 상세 조회 API 제공

## Used

* Python
* FastAPI
* SQLAlchemy
* SQLite
* Kakao Local API

## Installing & Executing

### 1. 가상환경 생성 및 실행

```bash
python -m venv .venv
```

Windows PowerShell 기준:

```bash
.venv\Scripts\activate
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

프로젝트 루트에 `.env` 파일을 만들고 아래 값을 설정합니다.

```env
KAKAO_REST_API_KEY=your_kakao_rest_api_key
```

### 4. 서버 실행

```bash
uvicorn app.main:app --reload
```

서버 실행 후 아래 주소에서 Swagger 문서를 확인할 수 있습니다.

```txt
http://127.0.0.1:8000/docs
```

## API Examples

### Search cafes

현재 위치 주변의 카페를 검색합니다.

```bash
curl "http://127.0.0.1:8000/cafes/search?query=카페&x=126.9990&y=37.4998&radius=1000&limit=5"
```

### Search response example

```json
{
  "count": 5,
  "low_result_count": false,
  "message": null,
  "cafes": [
    {
      "place_id": "1697987787",
      "place_name": "레망도레 서래마을점",
      "category_name": "음식점 > 카페",
      "address_name": "서울 서초구 반포동 68-1",
      "road_address_name": "서울 서초구 사평대로26길 9-3",
      "phone": "010-2540-3650",
      "place_url": "http://place.map.kakao.com/1697987787",
      "x": 126.999003683395,
      "y": 37.499777235682,
      "distance": 91,
      "is_franchise": false,
      "ai_summary": "레망도레 서래마을점은 현재 위치에서 매우 가까워 가볍게 들르기 좋은 카페입니다.",
      "summary_updated_at": null,
      "created_at": "2026-06-22T10:11:42",
      "updated_at": "2026-06-23T03:12:05",
      "score": 100
    }
  ],
  "suggested_radius": null
}
```

### Empty search response example

검색 결과가 없으면 빈 배열과 추천 확장 반경을 반환합니다.

```json
{
  "count": 0,
  "low_result_count": true,
  "message": "검색 결과가 없어요. 반경을 넓히면 더 많은 후보를 볼 수 있어요.",
  "cafes": [],
  "suggested_radius": 2000
}
```

### Get cafe detail

특정 카페의 상세 정보를 조회합니다.

```bash
curl "http://127.0.0.1:8000/cafes/1697987787"
```

## Field Notes

* `x`: 경도입니다.
* `y`: 위도입니다.
* `radius`: 검색 반경입니다. 단위는 미터입니다.
* `limit`: 반환할 카페 개수입니다.
* `suggested_radius`: 검색 결과가 적거나 없을 때 추천하는 확장 반경입니다.
* `ai_summary`: 카페 추천용 요약 문장입니다. 현재 MVP에서는 기본 요약이 반환될 수 있습니다.
* `summary_updated_at`: AI 요약이 생성 또는 갱신된 시각입니다. 기본 요약만 있는 경우 `null`일 수 있습니다.

## Current Limitations

* 현재 추천 점수는 거리 중심의 단순 점수입니다.
* 실제 리뷰, 평점, 혼잡도 기반 추천은 아직 적용되지 않았습니다.
* AI 요약은 향후 OpenAI API 연동 후 개선할 예정입니다.
* 프론트엔드는 아직 구현되지 않았습니다.
