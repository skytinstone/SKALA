"""
CSV의 title/description/embedding을 읽어,
PostgreSQL(pgvector) 테이블에 트랜잭션으로 안전 저장.

- 라이브러리: psycopg(=psycopg3), pandas, python-dotenv
- pgvector 확장 필요: CREATE EXTENSION IF NOT EXISTS vector;

작성자 주석: 비전공자도 읽기 쉽게 쉬운 표현으로 설명되어 있습니다.
"""

import os
import ast
import math
from typing import List, Optional

import pandas as pd
import psycopg
from psycopg.rows import tuple_row
from dotenv import load_dotenv

# -----------------------------
# 0) 환경 변수 로드 (.env에 DB 정보 저장해두면 편리)
# -----------------------------
load_dotenv()  # .env 파일이 있으면 자동으로 읽어옴

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = int(os.getenv("PGPORT", "5432"))
PGDATABASE = os.getenv("PGDATABASE", "DBMS_SQL")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", "0530")

CSV_PATH = "sample_designs_500.csv"  # 파일명이 다르면 수정하세요.

# -----------------------------
# 1) 임베딩 생성기 (대체 가능)
# -----------------------------
def generate_embedding_from_text(text: str, dim: int = 1536) -> List[float]:
    """
    실제 서비스에선 OpenAI/HuggingFace 사용.
    여기선 예시로 "텍스트 길이를 시드로 한 의사난수 벡터"를 생성합니다.
    - 항상 같은 입력 텍스트 → 같은 벡터가 나오도록 간단히 고정(seed 느낌)
    """
    # 아주 단순한 해시 → 0~1 사이 값으로 변환
    base = sum(ord(c) for c in (text or ""))
    # 의사난수 생성: sin 함수를 이용해 0~1 사이 값 만들기 (학습용 예시)
    vec = [((math.sin(base * (i + 1)) + 1) / 2.0) for i in range(dim)]
    return vec

# (참고) OpenAI 사용 예시(주석)
# from openai import OpenAI
# def generate_embedding_openai(text: str) -> List[float]:
#     client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#     out = client.embeddings.create(model="text-embedding-3-small", input=text)
#     return out.data[0].embedding  # 길이 1536


# -----------------------------
# 2) CSV의 embedding 문자열을 파싱
# -----------------------------
def parse_embedding_field(value) -> Optional[List[float]]:
    """
    CSV의 'embedding' 컬럼이 문자열 형태('[0.1, 0.2, ...]')면 파이썬 리스트로 바꿔줍니다.
    비어있으면 None을 반환합니다.
    """
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return None
    if isinstance(value, list):
        return value
    if isinstance(value, str) and value.strip():
        try:
            arr = ast.literal_eval(value)  # 안전한 파서
            # float로 캐스팅
            return [float(x) for x in arr]
        except Exception:
            return None
    return None


# -----------------------------
# 3) pgvector 입력 포맷으로 변환
# -----------------------------
def to_sql_vector(values: List[float]) -> str:
    """
    pgvector는 '[1,2,3]' 같은 문자열을 ::vector 로 캐스팅해 넣을 수 있습니다.
    psycopg가 자동 어댑터를 제공하긴 하지만, 환경에 따라 문자열로 넘기는 편이 안전합니다.
    """
    return "[" + ",".join(f"{x:.6f}" for x in values) + "]"


# -----------------------------
# 4) 테이블 생성 (없으면)
# -----------------------------
def ensure_table(conn, dim: int):
    """
    design 테이블이 없으면 생성합니다.
    - embedding 컬럼은 vector(dim) 타입
    """
    create_sql = f"""
    CREATE TABLE IF NOT EXISTS design (
        id          BIGSERIAL PRIMARY KEY,
        title       TEXT,
        description TEXT,
        embedding   VECTOR({dim})
    );
    """
    with conn.cursor() as cur:
        # pgvector 확장 보장
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute(create_sql)


# -----------------------------
# 5) 메인 로직: CSV → DB (트랜잭션)
# -----------------------------
def import_csv_with_transaction(csv_path: str):
    # 5-1) CSV 읽기
    df = pd.read_csv(csv_path)

    # 5-2) 첫 행을 기준으로 임베딩 차원(d) 자동 감지
    first_emb: Optional[List[float]] = None
    for v in df.get("embedding", []):
        first_emb = parse_embedding_field(v)
        if first_emb:
            break

    # 임베딩이 CSV에 없거나 비어 있으면, description로부터 새로 만들 계획
    if first_emb is None:
        # 실제 임베딩 모델 차원에 맞춰 지정 (OpenAI small=1536, ada-002=1536 등)
        detected_dim = 1536
    else:
        detected_dim = len(first_emb)

    print(f"[INFO] 감지된 임베딩 차원: {detected_dim}")

    # 5-3) DB 연결
    conn = psycopg.connect(
        host=PGHOST, port=PGPORT, dbname=PGDATABASE, user=PGUSER, password=PGPASSWORD,
        row_factory=tuple_row, autocommit=False  # autocommit=False → 우리가 직접 commit/rollback
    )

    try:
        # 5-4) 스키마 보장
        ensure_table(conn, detected_dim)

        # 5-5) 하나의 트랜잭션으로 전체 배치를 처리
        with conn.cursor() as cur:
            insert_sql = """
            INSERT INTO design (title, description, embedding)
            VALUES (%s, %s, %s::vector)
            """

            # DataFrame의 각 행을 순회하면서 INSERT 준비
            for idx, row in df.iterrows():
                title = row.get("title", None)
                desc = row.get("description", None)

                # 1) CSV에 embedding이 있으면 사용
                emb_vec = parse_embedding_field(row.get("embedding", None))

                # 2) 없으면 description으로부터 새로 생성(예시 함수)
                if emb_vec is None:
                    emb_vec = generate_embedding_from_text(desc or "", dim=detected_dim)

                # 3) 문자열 포맷으로 변환하여 ::vector 캐스팅
                emb_sql = to_sql_vector(emb_vec)

                # 4) 파라미터 바인딩으로 안전하게 INSERT
                cur.execute(insert_sql, (title, desc, emb_sql))

        # 5-6) 모두 성공했다면 COMMIT
        conn.commit()
        print("[SUCCESS] 전체 COMMIT 완료 (모든 데이터 저장됨)")

    except Exception as e:
        # 5-7) 하나라도 실패하면 전체 ROLLBACK
        conn.rollback()
        print("[ERROR] 예외 발생, ROLLBACK 처리:", e)
        raise

    finally:
        conn.close()
        print("[INFO] DB 연결 종료")


# -----------------------------
# 6) 실행부
# -----------------------------
if __name__ == "__main__":
    import_csv_with_transaction(CSV_PATH)
