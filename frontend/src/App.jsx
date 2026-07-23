import "./App.css";
import CafeCard from "./components/CafeCard";
import CafeDetail from "./components/CafeDetail";
import RadiusSelector from "./components/RadiusSelector";
import useCafeSearch from "./hooks/useCafeSearch";
import { useState } from "react";
import { Route, Routes } from "react-router-dom";

function App() {
  const [radius, setRadius] = useState(1000);

  const {
    cafes,
    message,
    loading,
    hasSearched,
    errorType,
    handleSearch,
  } = useCafeSearch();

  const searchPage = (
    <main>
      <h1>CafePickly</h1>
      <p>근처 괜찮은 개인 카페를 추천해 드립니다.</p>

      <RadiusSelector radius={radius} onChange={setRadius} />

      <button onClick={() => handleSearch(radius)}>
          카페 추천 받기
      </button>

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

  return (
    <Routes>
      <Route path="/" element={searchPage} />
      <Route path="/cafes/:placeId" element={<CafeDetail />} />
    </Routes>
  );
}

export default App;
