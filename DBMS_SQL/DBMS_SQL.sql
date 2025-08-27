-- 최초 1회만 적용!
CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS design;

CREATE TABLE design (
    id SERIAL PRIMARY KEY,
    title TEXT,
    description TEXT,
    embedding VECTOR(384)   -- pgvector 확장 타입
);

COPY design(title, description, embedding)
FROM '/Users/minseok/workspace/basic/DBMS_SQL/sample_designs_500.csv'
DELIMITER ','
CSV HEADER;

-- 전체 행 수 확인
SELECT COUNT(*) FROM design;

-- 일부 데이터 확인
SELECT id, title, description, embedding[0:5] AS first_5_dims
FROM design
LIMIT 10;

