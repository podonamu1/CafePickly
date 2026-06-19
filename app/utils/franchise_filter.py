FRANCHISE_KEYWORDS = [
    "스타벅스",
    "이디야",
    "메가커피",
    "빽다방",
    "투썸",
    "컴포즈"
]

def is_franchise(name: str) -> bool:
    return any(keyword in name for keyword in FRANCHISE_KEYWORDS)