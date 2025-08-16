-- pgvector 확장이 설치되어 있는지 확인
CREATE EXTENSION IF NOT EXISTS vector;

-- 테이블 생성
CREATE TABLE review_vectors (
    id SERIAL PRIMARY KEY,           -- 각 리뷰를 구분하기 위한 고유 ID
    review TEXT,                     -- 원본 리뷰 텍스트
    embedding VECTOR(384)            -- 384 차원 벡터 (sentence-transformers 모델로 생성된 임베딩)
);


CREATE INDEX IF NOT EXISTS review_vectors_embedding_hnsw
ON review_vectors
USING hnsw(embedding vector_cosine_ops)
WITH (m = 16, ef_construction =64);