import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqllite:///./cafepickly.db")

settings = Settings()