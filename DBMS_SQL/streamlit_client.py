"""
Streamlit 클라이언트
- 사용자가 title/description/embedding(선택)을 입력
- '등록' 버튼 클릭 시 FastAPI /register_design 로 POST 전송
- 결과(신규 id 등)를 화면에 표시

실행: streamlit run streamlit_client.py
"""

import ast
import requests
import streamlit as st

# FastAPI 서버 주소 (필요 시 바꾸세요)
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Design 등록", page_icon="🎨", layout="centered")
st.title("🎨 Design 등록 (Streamlit → FastAPI)")

with st.form("design_form"):
    st.write("아래 항목을 입력한 뒤, '등록하기' 버튼을 누르세요.")
    title = st.text_input("제목 (title)", placeholder="예: 도어 핸들 디자인 v1")
    description = st.text_area("설명 (description)", height=160, placeholder="설계를 간단히 설명하세요.")

    st.caption("선택: 이미 임베딩이 있다면 파이썬 리스트 형태로 붙여넣기 (예: [0.1, 0.2, ...])")
    embedding_str = st.text_area("임베딩 (선택)", height=100, placeholder="[0.12, 0.34, ...]")

    submitted = st.form_submit_button("등록하기")

if submitted:
    if not title or not description:
        st.error("제목과 설명은 필수입니다.")
    else:
        payload = {
            "title": title,
            "description": description,
        }

        # 임베딩이 입력되었으면 문자열을 파싱해 리스트로 변환
        if embedding_str.strip():
            try:
                parsed = ast.literal_eval(embedding_str.strip())
                if not isinstance(parsed, list):
                    raise ValueError("임베딩은 리스트여야 합니다. 예: [0.1, 0.2]")
                # float 변환 시도 (FastAPI에서 차원/타입 최종 검증)
                payload["embedding"] = [float(x) for x in parsed]
            except Exception as e:
                st.error(f"임베딩 파싱 실패: {e}")
                st.stop()

        try:
            res = requests.post(f"{API_BASE}/register_design", json=payload, timeout=15)
            if res.status_code == 200:
                data = res.json()
                st.success("등록 성공!")
                st.json(data)
                st.info("💡 Tip: pgAdmin4에서 SELECT로 실제 저장 여부를 확인해보세요.\n"
                        "예) SELECT id, title, embedding[0:5] FROM design ORDER BY id DESC LIMIT 5;")
            else:
                st.error(f"등록 실패: {res.status_code}\n{res.text}")
        except Exception as e:
            st.error(f"요청 중 오류: {e}")
