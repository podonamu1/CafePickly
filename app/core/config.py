import os
from dotenv import load_dotenv

load_dotenv()

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
