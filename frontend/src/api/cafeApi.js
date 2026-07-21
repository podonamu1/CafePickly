export async function fetchCafes({ x, y, radius }) {
    const response = await fetch(
        `http://localhost:8000/cafes/search?query=카페&x=${x}&y=${y}&radius=${radius}`
    );

    if (!response.ok) {
        throw new Error("카페 검색 API 요청에 실패했습니다.");
    }

    return response.json();

}