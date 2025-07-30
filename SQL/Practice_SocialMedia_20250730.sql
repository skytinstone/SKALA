-- 1. 모델 테이블
CREATE TABLE models (
  model_id SERIAL PRIMARY KEY,
  model_name TEXT UNIQUE
);

-- 2. 사용자 테이블
CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  user_name TEXT UNIQUE
);

-- 3. 메인 테이블: prompt + response + rating 포함
CREATE TABLE prompt_responses (
  pr_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  model_id INT REFERENCES models(model_id),
  prompt_text TEXT,
  response_text TEXT,
  rating NUMERIC(3,1)
);

-- 4. 태그 테이블
CREATE TABLE tags (
  tag_id SERIAL PRIMARY KEY,
  tag_name TEXT UNIQUE
);

-- 5. 응답-태그 연결 테이블 (Many-to-Many)
CREATE TABLE feedback_tags (
  pr_id INT REFERENCES prompt_responses(pr_id) ON DELETE CASCADE,
  tag_id INT REFERENCES tags(tag_id) ON DELETE CASCADE,
  PRIMARY KEY (pr_id, tag_id)
);

-- 6. CSV 임포트를 위한 임시 테이블 (Import 전용)
CREATE TABLE temp_import_table (
  feedback_id TEXT,
  model_name TEXT,
  user_name TEXT,
  prompt_text TEXT,
  response_text TEXT,
  rating NUMERIC(3,1),
  tags TEXT  -- 예: "['감성', '비판적']"
);
