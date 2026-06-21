FRANCHISE_KEYWORDS = [
    "스타벅스", "투썸", "할리스", "이디야", "커피빈", "파스쿠찌",
    "메가MGC", "메가커피", "컴포즈", "빽다방", "더벤티", "공차",
    "우지커피", "발도스커피", "텐퍼센트", "커피에반하다",
    "카페봄봄", "하삼동커피", "매머드커피", "감성커피",
    "커피베이", "엔제리너스", "폴바셋", "샌두", "더무인"
]

def is_franchise(name:str) -> bool:
    for brand in FRANCHISE_KEYWORDS:
        if brand in name:
            return True
    return False