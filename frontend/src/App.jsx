import "./App.css";
import CafeCard from "./components/CafeCard";
import RadiusSelector from "./components/RadiusSelector";
import { useState } from "react";

function App() {
  const [cafes, setCafes] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [radius, setRadius] = useState(1000);
  const [hasSearched, setHasSearched] = useState(false);
  const [errorType, setErrorType] = useState("");

  async function handleClick() {
    setLoading(true);
    setMessage("");
    setHasSearched(true)
    setErrorType("");

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
            setErrorType("location");
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

      <RadiusSelector radius={radius} onChange={setRadius} />

      <button onClick={handleClick}>카페 추천 받기</button>

      {loading && <p>불러오는 중...</p>}

      <section className="cafe-list">
        {cafes.map((cafe) => (
          <CafeCard key={cafe.place_id} cafe={cafe} />
        ))}
      </section>

      {hasSearched && !loading && !errorType && cafes.length === 0 && (
        <div className="empty-state">
            <h2> 근처 카페가 적어요</h2>
            <p>{message || "조건에 맞는 카페를 찾지 못했어요."}</p>
            <p>반경을 넓혀 다시 찾아보세요.</p>
        </div>
      )}

      {errorType === "location" && !loading && (
        <div className="empty-state">
            <h2>위치 권한이 필요해요.</h2>
            <p>현재 위치를 가져오지 못했어요.</p>
            <p>브라우저 위치 권한을 허용한 뒤 다시 시도해 주세요.</p>
        </div>
      )}

    </main>
  );
}

export default App;
