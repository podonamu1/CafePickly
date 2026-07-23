import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { fetchCafeDetail } from "../api/cafeApi";

function CafeDetail() {
    const { placeId } = useParams();
    const navigate = useNavigate();

    const [cafe, setCafe] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        async function loadCafeDetail() {
            try {
                const data = await fetchCafeDetail(placeId);
                setCafe(data);
            } catch {
                setError(true);
            } finally {
                setLoading(false);
            }
        }

        loadCafeDetail();
    }, [placeId]
    );

    if (loading) {
        return <main><p>카페 정보를 불러오는 중...</p></main>
    }

    if (error || !cafe) {
        return (
            <main>
                <p>카페 정보를 불러오지 못했어요.</p>
                <button onClick={() => navigate(-1)}>
                    뒤로 가기
                </button>
            </main>
        );
    }

    return (
        <main className="detail-page">
            <button
                className="back-button"
                onClick={() => navigate(-1)}
            >
                ← 뒤로 가기
            </button>

            <article className="detail-card">
                <span className="detail-category">
                    {cafe.category_name}
                </span>

                <h1>{cafe.place_name}</h1>

                <p className="detail-summary">
                    {cafe.ai_summary || "아직 카페 요약이 없어요."}
                </p>

                <dl>
                    <div>
                        <dt>주소</dt>
                        <dd>{cafe.road_address_name || cafe.address_name}</dd>
                    </div>

                    {cafe.phone && (
                        <div>
                            <dt>전화</dt>
                            <dd>{cafe.phone}</dd>
                        </div>
                    )}
                </dl>

                <a
                    className="detail-map-link"
                    href={cafe.place_url}
                    target="_blank"
                    rel="noreferrer"
                >
                    카카오맵에서 보기
                </a>
            </article>
        </main>
    );
}

export default CafeDetail;