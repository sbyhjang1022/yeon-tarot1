# pages/타로카드_참고자료.py
import streamlit as st

st.set_page_config(page_title="타로카드 참고자료", layout="wide")

st.markdown("<h1 style='color:#5a5a5a'>타로카드 참고자료 🎴</h1>", unsafe_allow_html=True)
st.markdown("유니카드와 오쇼카드 두 가지 덱 중심으로 간단한 키워드·해설을 제공합니다. 카드는 예시로 몇 장만 넣었습니다. 카드 이미지 파일을 추가하시면 `st.image()`로 크게 보여줄 수 있습니다.")

deck = st.selectbox("덱 선택", ["유니카드 (Unicard)", "오쇼카드 (Osho)"])

# 간단 예시 카드 데이터
UNICARD = {
    "태양 (The Sun)": {
        "keywords": ["성장", "명료함", "성공"],
        "meaning": "긍정적인 변화와 성취를 나타냅니다. 현재의 노력은 좋은 결실을 맺습니다."
    },
    "달 (The Moon)": {
        "keywords": ["잠재의식", "불안", "직관"],
        "meaning": "감정의 불확실성이 있을 수 있으니 직감과 조심스러운 접근을 권합니다."
    },
    "운명의 수레바퀴 (Wheel of Fortune)": {
        "keywords": ["변화", "순환", "운"],
        "meaning": "운의 흐름이 바뀔 수 있음을 알립니다. 변화에 유연하게 적응하세요."
    }
}

OSHO = {
    "침묵 (Silence)": {
        "keywords": ["내면", "휴식", "명상"],
        "meaning": "내면의 고요를 찾아야 할 때입니다. 과도한 활동보다는 멈추고 성찰하세요."
    },
    "빛 (Light)": {
        "keywords": ["깨달음", "직관", "명료함"],
        "meaning": "직관이 열리는 시기입니다. 작은 신호를 놓치지 마세요."
    },
    "변화 (Transformation)": {
        "keywords": ["변형", "해방", "재탄생"],
        "meaning": "구조적 변화가 필요합니다. 오래된 패턴을 내려놓으세요."
    }
}

cards = UNICARD if "유니카드" in deck else OSHO
card_list = list(cards.keys())
selected = st.selectbox("카드 선택", card_list)

col1, col2 = st.columns([1,2])
with col1:
    # 이미지가 있으면 ./cards/<deck_name>/<cardname>.png 로 두면 표시하도록 안내
    st.markdown("### 카드 이미지")
    st.info("이미지를 추가하려면 앱 폴더에 `cards/<덱이름>/<카드파일>.png` 형식으로 넣고, 코드의 이미지 경로를 맞춰주세요.")
    # fallback visual
    st.markdown("#### (이미지 없음) 🎴")
with col2:
    info = cards[selected]
    st.markdown(f"### {selected}")
    st.markdown(f"**키워드:** {', '.join(info['keywords'])}")
    st.markdown("**해설**")
    st.write(info["meaning"])

st.markdown("---")
st.markdown("팁: 실제 상담에서 카드 해석은 문맥(질문자 상태, 질문 내용, 주변 카드)과 결합해 해석하세요. 🎎🫖🍡")

