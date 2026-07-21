import { useState } from "react";
import { fetchCafes } from "../api/cafeApi";

export default function useCafeSearch() {
  const [cafes, setCafes] = useState([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [errorType, setErrorType] = useState("");


  async function handleSearch(radius) {

    setLoading(true);
    setMessage("");
    setHasSearched(true);
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

            const data = await fetchCafes({ x, y, radius });

            setCafes(data.cafes ?? []);
            setMessage(data.message ?? "");
          } catch (error) {
            setMessage("카페 정보를 불러오지 못했습니다.");
            console.error(error);
          } finally {
            setLoading(false);
          }
      },
      (error) => {
          setErrorType("location");
          setMessage(
            "현재 위치를 가져오지 못했습니다. 위치 권한을 확인해 주세요."
          );
          console.error(error);
          setLoading(false);
      }
    );
  }

  return  {
    cafes,
    message,
    loading,
    hasSearched,
    errorType,
    handleSearch,
  };

}

