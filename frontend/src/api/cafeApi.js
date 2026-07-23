const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function fetchCafes({ x, y, radius }) {

    const response = await fetch(
        `${API_BASE_URL}/cafes/search?query=카페&x=${x}&y=${y}&radius=${radius}`
    );

    if (!response.ok) {
        throw new Error("카페 검색 API 요청에 실패했습니다.");
    }

    return response.json();

}

export async function fetchCafeDetail(placeId) {
    const response = await fetch(
        `${API_BASE_URL}/cafes/${placeId}`
    );

    if (!response.ok) {
        throw new Error("카페 상세 정보 요청에 실패했습니다.");
    }

    return response.json();
}