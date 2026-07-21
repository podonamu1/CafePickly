function CafeCard({ cafe }) {
    const address = cafe.road_address_name || cafe.address_name;

    return (
        <article className="cafe-card">
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
                  >
                    카카오맵에서 보기
                  </a>
              )}
        </article>

    )

}

export default CafeCard;