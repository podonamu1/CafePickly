import "./App.css";
import { useState } from "react";

function App() {
  const [cafes, setCafes] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [radius, setRadius] = useState(1000);

  async function handleClick() {
    setLoading(true);
    setMessage("");

    if (!navigator.geolocation) {
        setMessage("이 브라우저에서는 현재 위치를 사용할 수 없습니다.");
        setLoading(false);
        return;
    }

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            try {
                const x = position.coords.longitude;
                const y = position.coords.latitude;

                const response = await fetch(
                    `http://localhost:8000/cafes/search?query=카페&x=${x}&y=${y}&radius=${radius}`
                );

                const data = await response.json();

                setCafes(data.cafes ?? []);
                setMessage(data.message ?? "");
            }
            catch (error) {
                setMessage("카페 정보를 불러오지 못했습니다.");
                console.error(error);
            }
            finally {
                setLoading(false);
            }
        },
        (error) => {
            setMessage("현재 위치를 가져오지 못했습니다. 위치 권한을 확인해 주세요.");
            console.error(error);
            setLoading(false);
        }
    );
  }

  return (
    <main>
      <h1>CafePickly</h1>
      <p>근처 괜찮은 개인 카페를 추천해 드립니다.</p>

      <div className="radius-selector">
          <p>검색 반경</p>

          <div className="radius-buttons">
              {[500, 1000, 1500].map((value) => (
                <button
                    key={value}
                    type="button"
                    className={radius === value? "radius-button active" : "radius-button"}
                    onClick={() => setRadius(value)}
                >
                    {value}m
                </button>
              ))}
          </div>
      </div>

      <button onClick={handleClick}>카페 추천 받기</button>

      {loading && <p>불러오는 중...</p>}
      {message && <p>{message}</p>}

      <section className="cafe-list">
        {cafes.map((cafe) => (
          <article className="cafe-card" key={cafe.place_id}>
              <div className="cafe-card-header">
                  <h2>{cafe.place_name}</h2>
                  <span className="distance">{cafe.distance}m</span>
              </div>

              <p className="summary">
                  {cafe.ai_summary || "요약 준비 중입니다."}
              </p>

              <p className="address">
                  {cafe.road_address_name || cafe.address_name}
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
        ))}
      </section>
    </main>
  );
}

export default App;
