-- llm_feedback Normalization 진행_20250730(수)
-- [실습 목표]
-- 	. LLM Feedback 데이터 정규화 (3NF까지 고려)
-- 	. model, user, prompt-response, tags 분리
-- 	. tags 필드는:TEXT[ ] 배열로 유지한 구조 (빠른 전처리, FAISS 등 용이)
-- 	. feedback_tag라는 별도 테이블로 정규화 (통계, RAG 전처리 유리)
-- 	.  AI 분석 목적의 전처리 성능 관점에서 두 방식 비교 설명

-- COPY 명령어로 직접 IMPORT
COPY raw_feedbakc
FROM '/Users/minseok/Downloads/ai_feedback_raw.csv'
CSV HEADER;

-- 1. 사용자 테이블
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_name VARCHAR(100),
    user_email VARCHAR(100) UNIQUE
);

-- 2. 모델 테이블
CREATE TABLE models (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100),
    model_version VARCHAR(50)
);

-- 3. 프롬프트/응답 테이블
CREATE TABLE prompts (
    prompt_id SERIAL PRIMARY KEY,
    prompt_text TEXT,
    response_text TEXT
);

-- 4. 피드백 테이블 (정규화된 중심 테이블)
CREATE TABLE feedbacks (
    feedback_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    model_id INTEGER REFERENCES models(model_id),
    prompt_id INTEGER REFERENCES prompts(prompt_id),
    feedback_text TEXT,
    feedback_tags TEXT[],  -- 태그를 배열로 저장
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 태그 정규화 테이블 (배열 태그의 개별 요소를 저장)
CREATE TABLE feedback_tags (
    id SERIAL PRIMARY KEY,
    feedback_id INTEGER REFERENCES feedbacks(feedback_id) ON DELETE CASCADE,
    tag TEXT
);
