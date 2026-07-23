import { useNavigate } from "react-router-dom";

function CafeCard({ cafe }) {
    const navigate = useNavigate();
    const address = cafe.road_address_name || cafe.address_name;

    const openDetail = () => {
        navigate(`/cafes/${cafe.place_id}`);
    };

    return (
        <article
            className="cafe-card"
            onClick={openDetail}
            role="link"
            tabIndex={0}
            onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    openDetail();
                }
            }}
        >
              <div className="cafe-card-header">
                  <h2>{cafe.place_name}</h2>
                  <span className="distance">{cafe.distance}m</span>
              </div>

              <p className="summary">
                  {cafe.ai_summary || "요약 준비 중입니다."}
              </p>

              <p className="address">
                  {address}
              </p>

              {cafe.place_url && (
                  <a
                    className="map-link"
                    href={cafe.place_url}
                    target="_blank"
                    rel="noreferrer"
                    onClick={(event) => event.stopPropagation()}
                  >
                    카카오맵에서 보기
                  </a>
              )}
        </article>

    )

}

export default CafeCard;