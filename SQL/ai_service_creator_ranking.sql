-- ✅ 실습 2: WITH (CTE) + 집계로 인기 기획자 추출
-- Tilte : AI Service review System
-- Goals :
-- CTE(Common Tabel Expression)로 집계 테이블을 구성!
-- AVG(평점)과 COUNT(리뷰)를 기준으로 인기 있는 기획자 선정!
-- ROW_NUMBER()로 랭킹 부여!
-- 향후 AI 추천(예 : 유사도 기반 + 평점 기반 추천) 전단 필터링에 활용!

-- [👿실습 문제]
-- 1.각 기획자의 평균 평점과 리뷰 수를 계산하고, 리뷰 수가 2개 이상인 사람 중에서 평점이 높은 순으로 랭킹 정리
-- 2.최소 쿼리를 2개 이상 작성하고, 각각에 대한 실행결과값이 어떻게 나오는지 비교하여 원인에 대한 의견 정리 

-- Source Written by. Minseok Shin, Date 20250731, SKALA 2nd --



-- 기존 테이블 제거
DROP TABLE IF EXISTS ai_service_reviews;
DROP TABLE IF EXISTS ai_service_creators;

-- 기획자 테이블 생성
CREATE TABLE ai_service_creators (
    creator_id SERIAL PRIMARY KEY,
    creator_name TEXT
);

-- 리뷰 테이블 생성
CREATE TABLE ai_service_reviews (
    review_id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES ai_service_creators(creator_id),
    rating INTEGER,  -- 1~5점
    review_text TEXT
);

-- 기획자 데이터 삽입
INSERT INTO ai_service_creators (creator_name) VALUES
('Alice Kim'),
('Brian Lee'),
('Clara Park'),
('David Choi');

-- 리뷰 데이터 삽입
INSERT INTO ai_service_reviews (creator_id, rating, review_text) VALUES
(1, 5, '서비스가 직관적이고 좋았습니다.'),
(1, 4, '빠르게 응답했어요.'),
(2, 3, '기능이 부족해요.'),
(2, 2, '사용성이 떨어져요.'),
(2, 4, '업데이트 기대합니다.'),
(3, 5, '딥러닝 기능이 인상 깊었어요.'),
(3, 5, '추천 정확도가 높아요.'),
(4, 3, '보통이에요.'),
(4, 2, '불편했어요.');

-------------------------<실습 query문>---------------------------

-- 테이블명: ai_service_reviews
-- 주요 컬럼:
-- Data Input (예:'회원 번호','평점','평가')
-- description_text (서비스 설명 텍스트)

------------------------<SELECT문을 활용>-------------------------- 



-- 쿼리 B: review_count 필터를 CTE 밖으로 옮긴 방식
WITH creator_stats AS (
    SELECT
        c.creator_id,
        c.creator_name,
        COUNT(r.review_id) AS review_count,
        ROUND(AVG(r.rating)::numeric, 2) AS avg_rating
    FROM
        ai_service_creators c
    JOIN
        ai_service_reviews r ON c.creator_id = r.creator_id
    GROUP BY
        c.creator_id, c.creator_name
)
SELECT
    *,
    ROW_NUMBER() OVER (ORDER BY avg_rating DESC, review_count DESC) AS rank
FROM creator_stats
WHERE review_count >= 2;

----------------------------성능 평가---------------------------------

EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
WITH creator_stats AS (
    SELECT
        c.creator_id,
        c.creator_name,
        COUNT(r.review_id) AS review_count,
        ROUND(AVG(r.rating)::numeric, 2) AS avg_rating
    FROM
        ai_service_creators c
    JOIN
        ai_service_reviews r ON c.creator_id = r.creator_id
    GROUP BY
        c.creator_id, c.creator_name
),
ranked_creators AS (
    SELECT
        *,
        ROW_NUMBER() OVER (ORDER BY avg_rating DESC, review_count DESC) AS rank
    FROM
        creator_stats
    WHERE
        review_count >= 2
)
SELECT * FROM ranked_creators;








