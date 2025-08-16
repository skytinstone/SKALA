# sentecnetransformer.py
# 작성자 : 신민석
# 작성일 : 2025.08.13(수)
# 팀 : SKALA,SK AX AI Leader Academy 2nd
# 반 : 1반
# 번호 : 15번
# ------------------------------------------------------------
# 목적: typing과 mypy를 이용한 타입 검사 및 성능 비교
# 구조:
#   - SentenceTransformer 모델을 사용하여 리뷰 데이터를 벡터화
#   - PostgreSQL 데이터베이스에 벡터를 저장하고 유사도 검색
#   - pgvector 확장을 사용하여 벡터 데이터를 저장
#   - 리뷰 데이터는 한국어로 작성된 예시 리뷰들
#   - 벡터화된 리뷰 데이터를 PostgreSQL에 저장하고, 유사도 검색을 수행
#   - 코사인 유사도를 사용하여 유사한 리뷰를 검색
#   - PostgreSQL 연결 설정 및 벡터 저장을 위한 테이블 생성
#   - 리뷰 데이터와 벡터를 PostgreSQL에 저장
#   - 유사도 검색을 통해 특정 리뷰와 유사한 리뷰를 찾음
#   - pgvector 확장을 사용하여 벡터 데이터를 저장

# 동작:
#   - SentenceTransformer 모델을 사용하여 리뷰 데이터를 벡터화
#   - PostgreSQL 데이터베이스에 벡터를 저장하고 유사도 검색
#   - pgvector 확장을 사용하여 벡터 데이터를 저장
#   - 리뷰 데이터는 한국어로 작성된 예시 리뷰들 
# ------------------------------------------------------------

from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import execute_values

# ===================== 설정 ===================== #
# ▶ 본인 환경에 맞게 DB 연결 정보 수정
DSN = "dbname= user= password= host= port=" # 예시: "dbname=mydb user=myuser password=mypassword host=localhost port=5432"
# DSN 경로 루트 반드시 본인이 실행하고자 하는 Database의 경로 및 파일 정보 수정 추가

# ▶ 모델 선택 (둘 다 384차원)
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L6-v2"
# 한국어 위주면 아래로 교체 가능:
# MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

EMBED_DIM = 384 # 임베딩 차원
K = 3  # 검색 결과 상위 K개

# ▶ 실습용 리뷰 데이터
REVIEWS = [
    "배송이 빠르고 제품도 좋아요.",
    "품질이 기대 이상입니다!",
    "생각보다 배송이 오래 걸렸어요.",
    "배송은 느렸지만 포장은 안전했어요.",
    "아주 만족스러운 제품입니다."
]

# ▶ 검색 쿼리 문장
QUERY_TEXT = "배송이 느렸어요"

# ===================== 유틸 ===================== #
def vec_to_pgvector_str(vec) -> str:
    """파이썬 list[float] → pgvector 텍스트 표현('[1,2,...]')"""
    return "[" + ",".join(str(float(x)) for x in vec) + "]"

# ===================== 메인 로직 ===================== #
def main():
    # 1) 임베딩 모델 로드 및 인퍼런스
    print(f"[INFO] Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    print("[INFO] Encoding sentences (L2 normalize for cosine search)...")
    embeddings = model.encode(REVIEWS, normalize_embeddings=True)
    assert embeddings.shape[1] == EMBED_DIM, f"임베딩 차원({embeddings.shape[1]})이 {EMBED_DIM}와 다릅니다."

    # 2) DB 접속
    print("[INFO] Connecting to PostgreSQL ...")
    with psycopg2.connect(DSN) as conn, conn.cursor() as cur:#cur: 커서 생성 -> cursor는 SQL문을 실행하고 결과를 가져오는 객체
        # 세션 스키마 고정(혼동 방지)
        cur.execute("SET search_path TO public;")

        # 2-1) pgvector 확장 (현재 DB에 설치)
        print("[INFO] Ensuring pgvector extension ...") #terminal에서 pgvector 설치 확인 가능
        # SQL문 실행 코드
        # ----------------------------------------------------------------------------------
        try:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        except Exception as e:
            print("[WARN] CREATE EXTENSION vector 실패 (권한/환경 이슈일 수 있습니다). 진행을 계속합니다.")
            print("       자세한 오류:", e)

        # 2-2) 테이블 생성
        print("[INFO] Ensuring table public.review_vectors ...")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS public.review_vectors (
                id SERIAL PRIMARY KEY,
                review TEXT,
                embedding VECTOR(%s)
            );
            """,
            (EMBED_DIM,),
        )

        # 2-3) HNSW 인덱스 생성 (pgvector 0.5+) : HNSW(Hierarchical Navigable Small World) 알고리즘
        # HNSW는 벡터 검색을 위한 효율적인 인덱싱 방법으로, 빠른 근사 최근접 이웃 검색을 지원
        # HNSW 인덱스는 벡터 검색 성능을 크게 향상시킴
        # m: 각 노드의 최대 연결 수, ef_construction: 인덱스 생성 시 탐색 깊이
        # ef_search: 검색 시 탐색 깊이 (HNSW 탐색 파라미터)
        # vector_cosine_ops: 코사인 유사도 연산을 위한 pgvector
        # vector_cosine_ops는 pgvector 확장에서 제공하는 코사인 유사도
        # ops는 벡터 간의 코사인 유사도를 계산하는 연산
        # ----------------------------------------------------------------------------------
        print("[INFO] Ensuring HNSW index on embedding ...") 
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS review_vectors_embedding_hnsw
            ON public.review_vectors
            USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64);
            """
        )
        conn.commit()

        # 3) 데이터 INSERT (기존 데이터 초기화 원하면 주석 해제)
        # cur.execute("TRUNCATE TABLE public.review_vectors;")

        print("[INFO] Inserting rows ...") 
        rows = []
        for text, emb in zip(REVIEWS, embeddings):
            rows.append((text, vec_to_pgvector_str(emb)))

        execute_values(
            cur,
            "INSERT INTO public.review_vectors (review, embedding) VALUES %s",
            rows,
            template="(%s, %s)",
        )
        conn.commit()

        # 검증용 카운트
        cur.execute("SELECT COUNT(*) FROM public.review_vectors;")
        total = cur.fetchone()[0]
        print(f"[INFO] INSERT 완료. 현재 행 수: {total}")

        # 4) 유사도 검색
        print(f'[INFO] Searching similar to: "{QUERY_TEXT}"')
        q_vec = model.encode([QUERY_TEXT], normalize_embeddings=True)[0]
        q_vec_str = vec_to_pgvector_str(q_vec)

        # HNSW 탐색 파라미터(선택)
        cur.execute("SET hnsw.ef_search = 40;")

        sql = """
        SELECT id, review, 1 - (embedding <=> %s) AS similarity
        FROM public.review_vectors
        ORDER BY embedding <=> %s
        LIMIT %s;
        """
        cur.execute(sql, (q_vec_str, q_vec_str, K))
        rows = cur.fetchall()

        print("\n[RESULT]")
        for i, (rid, review, sim) in enumerate(rows, 1):
            print(f"{i}. id={rid}, sim={sim:.4f} | {review}")

    print("\n[OK] Done.")

if __name__ == "__main__":
    main()
