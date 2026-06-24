import { useState } from "react";

function App() {
  const [cafes, setCafes] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleClick() {
    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(
        "http://localhost:8000/cafes/search?query=카페&x=126.999003683395&y=37.499777235682&radius=1000"
      );

      const data = await response.json();

      setCafes(data.cafes ?? []);
      setMessage(data.message ?? "");
    } catch (error) {
      setMessage("카페 정보를 불러오지 못했습니다.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>CafePickly</h1>
      <p>근처 괜찮은 개인 카페를 추천해 드립니다.</p>

      <button onClick={handleClick}>카페 추천 받기</button>

      {loading && <p>불러오는 중...</p>}
      {message && <p>{message}</p>}

      <section>
        {cafes.map((cafe) => (
          <article key={cafe.place_id}>
            <h2>{cafe.place_name}</h2>
            <p>{cafe.ai_summary || "요약 준비 중입니다."}</p>
            <p>{cafe.road_address_name || cafe.address_name}</p>
            <p>{cafe.distance}m</p>
          </article>
        ))}
      </section>
    </main>
  );
}

export default App;
