import streamlit as st
from groq import Groq

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="번개 챗봇 AI", page_icon="⚡")
st.title("⚡ 번개 챗봇 AI")
st.markdown("---")

# 2. API 키 설정 (st.secrets 사용)
# .streamlit/secrets.toml 파일에 GROQ_API_KEY = "your_api_key_here"가 있어야 합니다.
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. 세션 상태(st.session_state) 초기화: 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "너는 코딩을 아주 쉽게 알려주는 친절한 선생님이야. 복잡한 개념도 비유를 들어서 초등학생도 이해할 수 있게 설명해줘."}
    ]

# 4. 사이드바 구성: 대화 초기화 기능
with st.sidebar:
    st.title("설정")
    if st.button("💬 대화 내용 지우기"):
        st.session_state.messages = [
            {"role": "system", "content": "너는 코딩을 아주 쉽게 알려주는 친절한 선생님이야. 복잡한 개념도 비유를 들어서 초등학생도 이해할 수 있게 설명해줘."}
        ]
        st.rerun()

# 5. 기존 대화 기록 출력 (System 메시지 제외)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. 사용자 입력 및 AI 답변 처리
if prompt := st.chat_input("선생님께 무엇이든 물어보세요!"):
    # 사용자 메시지 표시 및 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Groq API 호출 및 답변 생성
    with st.chat_message("assistant", avatar="⚡"):
        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                stream=False # 스트리밍을 원하면 True로 변경 가능
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            
            # AI 답변 저장
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")