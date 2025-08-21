-- ✅ 실습 1: 키워드 기반 서비스 기획안 검색 쿼리
-- Tilte : AI Service 기획안 설명 검색
-- Goal :
-- Keyword 검색(ILIKE)을 통해 텍스트 필터링 수행
-- 향후 텍스트 임베딩 + 벡터 유사도 기반 검색과 비교 가능하게 설계
-- 실제 서비스 분류(Category)와 설명(description)을 동시에 필터링!

-- [👿실습 문제]
-- 1.설명(description_text)에 '분석'이라는 단어가 포함되어있고, 카테고리가 '헬스케어'인 서비스만 조회
-- 2.설명에 '기록'이 포함되고, 카테고리가 '헬스케어'인 서비스 조회
-- 3.category가 '교육'이고, 설명에 '추천'이 포함되 기획안 조회
-- 4.설명에 '예측' 혹은 '분석'이 포함된 모든 기획안을 조회

-- Source Written by. Minseok Shin, Date 20250731, SKALA 2nd --

-- 테이블 삭제 및 생성
DROP TABLE IF EXISTS ai_service_plans;

-- ai_service_plans라는 이름의 table 생성!
CREATE TABLE ai_service_plans (
    id SERIAL PRIMARY KEY,   -- id를 "Primary Key"로 설정! 
    service_name TEXT,		 -- service이름을 텍스트로 설정!
    category TEXT,           -- 카테고리 읽어들일 텍스트로 설정! [ex : '헬스케어', '금융', '교육', '리테일']
    description_text TEXT    -- descrition_text를 텍스트로 설정! -> "서비스 개요 설명"
);

-- 예시 데이터 삽입

INSERT INTO ai_service_plans (service_name, category, description_text) VALUES
('SmartFit', '헬스케어', 'AI를 활용한 개인 맞춤형 운동 코칭 서비스'),
('EduBot', '교육', '학생의 학습 패턴을 분석하여 추천 커리큘럼 제공'),
('FinGuard', '금융', '소비 내역 분석을 통한 금융 사기 탐지 서비스'),
('RetailMate', '리테일', '매장 내 고객 행동을 분석하여 상품 배치 최적화'),
('HealthGuard', '헬스케어', '건강 기록 기반의 조기 질병 예측 AI 시스템');


-------------------------<실습 query문>---------------------------

-- 테이블명: ai_service_plans
-- 주요 컬럼:
-- category (예: '헬스케어', '금융', '교육', '리테일')
-- description_text (서비스 설명 텍스트)

------------------------<SELECT문을 활용>-------------------------- 

-- 1.'분석'포함 + 카테코리'헬스케어'
SELECT *
FROM ai_service_plans
WHERE category = '헬스케어'
  AND description_text LIKE '%분석%'; --Like : 문자열 패턴 매칭 연산자 

-- 2.'기록'포함 +카테고리'헬스케어'
SELECT *
FROM ai_service_plans
WHERE category = '헬스케어'
  AND description_text LIKE '%기록%';

-- 3.'추천'포함 +카테고리'교육'
SELECT *
FROM ai_service_plans
WHERE category = '교육'
	AND description_text LIKE '%추천';

-- 4.'예측' OR '분석'포함
SELECT *
FROM ai_service_plans
WHERE description_text LIKE '%예측%'    -- %keyword% 대소문자 구분 OK -> 허나 대소문자 구분이 필요없어도 되니 그대로 진행해도 됨!
	OR description_text LIKE '%분석%';  -- %keyword% 대소문자 구분 OK -> 허나 대소문자 구분이 필요없어도 되니 그대로 진행해도 됨!
