import streamlit as st
import random

# 1. 라이브러리 체크 (ImportError 방지)
try:
    from groq import Groq
except ImportError:
    st.error("❗ 'groq' 라이브러리가 설치되지 않았습니다. 터미널에 'pip install groq'를 입력해주세요.")
    st.stop()

# 2. 페이지 설정
st.set_page_config(page_title="번개 챗봇 AI", page_icon="⚡")

# 3. 사계절 배경 설정 함수 (겨울 이미지 업데이트)
def get_season_data():
    seasons = {
        "봄": "https://images.unsplash.com/photo-1490750967868-88aa4486c946",
        "여름": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
        "가을": "https://images.unsplash.com/photo-1507783548227-544c3b8fc065",
        # 새로운 겨울 이미지 (눈 덮인 숲이나 마을 느낌)
        "겨울": "https://images.unsplash.com/photo-1478720568477-152d9b164e26" 
    }
    name, url = random.choice(list(seasons.items()))
    return name, url

# 세션 상태에 배경 정보가 없으면 처음 한 번만 생성
if "bg_data" not in st.session_state:
    name, url = get_season_data()
    st.session_state.bg_data = {"name": name, "url": url}

# CSS 적용 (매 리런마다 세션에 저장된 고정된 URL 사용)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), 
                    url("{st.session_state.bg_data['url']}");
        background-size: cover;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

# 타이틀에 저장된 계절 이름 표시
st.title(f"⚡ 번개 챗봇 AI ({st.session_state.bg_data['name']})")

# 4. API 키 확인
if "GROQ_API_KEY" not in st.secrets:
    st.warning("⚠️ .streamlit/secrets.toml 파일에 GROQ_API_KEY를 설정해주세요.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 5. 세션 상태 및 시스템 프롬프트 (한국어 고정 명령 추가)
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system", 
        "content": (
            "너는 코딩을 아주 쉽게 알려주는 친절한 선생님이야. "
            "사용자가 어떤 언어(영어, 러시아어, 중국어 등)로 물어보더라도 "
            "반드시 답변은 '한국어'로만 해야 해. "
            "복잡한 개념도 비유를 들어서 초등학생도 이해할 수 있게 설명해줘."
        )
    }]

# 사이드바 리셋 버튼
with st.sidebar:
    if st.button("💬 대화 내용 지우기"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# 6. 대화 출력
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. 사용자 입력 및 답변 생성
if prompt := st.chat_input("선생님께 질문해보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="⚡"):
        try:
            # llama-3.3-70b-versatile 모델 사용 (한국어 처리 능력이 더 우수함)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")