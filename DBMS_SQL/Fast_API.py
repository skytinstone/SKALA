"""
FastAPI 기반 /register_design API
A안 반영: 서버 시작 시 design 테이블을 384차원(pgvector)로 '깨끗하게' 재생성
- DROP TABLE IF EXISTS design;
- CREATE EXTENSION IF NOT EXISTS vector;
- CREATE TABLE design (... embedding VECTOR(384));

실행:
  uvicorn Fast_API:app --reload
환경변수(.env):
  PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
옵션:
  INIT_RESET=1  -> 서버 시작 시 테이블 드롭 후 재생성 (기본값: 1)
  INIT_RESET=0  -> 드롭/재생성 하지 않음 (운영 권장)
"""

import os
import math
from typing import List, Optional

import psycopg
from psycopg.rows import tuple_row
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------
# 0) 환경변수(.env) 로드
# -----------------------------
load_dotenv()

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = int(os.getenv("PGPORT", "5432"))
PGDATABASE = os.getenv("PGDATABASE", "your_database")
PGUSER = os.getenv("PGUSER", "your_username")
PGPASSWORD = os.getenv("PGPASSWORD", "your_password")

# A안에서 사용할 임베딩 차원(테이블과 반드시 일치)
EMBEDDING_DIM = 384

# 서버 시작 시 테이블을 드롭/재생성할지 여부 (A안 기본: 켜짐)
INIT_RESET = os.getenv("INIT_RESET", "1") == "1"

# -----------------------------
# 1) 임베딩 유틸 (학습용 더미 구현)
# -----------------------------
def generate_embedding_from_text(text: str, dim: int = EMBEDDING_DIM) -> List[float]:
    """
    실제 서비스에서는 OpenAI/HuggingFace 모델 사용.
    여기선 '항상 같은 텍스트 -> 같은 벡터'가 되도록 간단 의사난수 벡터 생성.
    """
    base = sum(ord(c) for c in (text or ""))
    return [((math.sin(base * (i + 1)) + 1) / 2.0) for i in range(dim)]

def to_sql_vector(values: List[float]) -> str:
    """
    pgvector는 문자열 "[1,2,3]" 형태를 ::vector 로 캐스팅해 저장 가능.
    환경 의존도 낮추기 위해 문자열 캐스팅 방식 사용.
    """
    return "[" + ",".join(f"{x:.6f}" for x in values) + "]"

# -----------------------------
# 2) 스키마 초기화(A안)
# -----------------------------
def reset_schema_drop_and_create(conn, dim: int):
    """
    A안: design 테이블을 깨끗하게 재생성 (데이터 전부 삭제됨)
    """
    ddl = f"""
    CREATE EXTENSION IF NOT EXISTS vector;
    DROP TABLE IF EXISTS design;
    CREATE TABLE design (
        id          BIGSERIAL PRIMARY KEY,
        title       TEXT,
        description TEXT,
        embedding   VECTOR({dim})
    );
    """
    with conn.cursor() as cur:
        cur.execute(ddl)

def ensure_extension_only(conn):
    """
    INIT_RESET=0 인 경우: 확장만 보장 (테이블 드롭/생성은 하지 않음)
    """
    with conn.cursor() as cur:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

# -----------------------------
# 3) 요청/응답 모델
# -----------------------------
class RegisterDesignRequest(BaseModel):
    title: str = Field(..., description="디자인 제목")
    description: str = Field(..., description="디자인 설명")
    embedding: Optional[List[float]] = Field(
        default=None,
        description=f"선택 입력. 제공 시 길이는 {EMBEDDING_DIM} 이어야 함."
    )

    @validator("embedding")
    def validate_embedding(cls, v):
        if v is None:
            return v
        if len(v) != EMBEDDING_DIM:
            raise ValueError(f"embedding length must be {EMBEDDING_DIM}, got {len(v)}")
        return [float(x) for x in v]

class RegisterDesignResponse(BaseModel):
    id: int
    title: str
    description: str
    dim: int = EMBEDDING_DIM

# -----------------------------
# 4) FastAPI 앱 & CORS
# -----------------------------
app = FastAPI(title="Design API (A안)", version="1.0.0")

# Streamlit(보통 8501) 등에서 호출 허용 (개발 편의)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 개발용: 전체 허용 (운영에서는 특정 도메인만)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# 5) 앱 시작 시(A안) 스키마 초기화
# -----------------------------
@app.on_event("startup")
def on_startup():
    # DB 연결 시도
    try:
        conn = psycopg.connect(
            host=PGHOST,
            port=PGPORT,
            dbname=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD,
            row_factory=tuple_row,
            autocommit=True,  # DDL은 autocommit로 안전하게
        )
    except Exception as e:
        # 시작 단계에서 실패하면 서버 자체가 쓸모 없으니 로그를 올리고 통과(엔드포인트 호출 시 다시 실패)
        print(f"[STARTUP] DB 연결 실패: {e}")
        return

    try:
        if INIT_RESET:
            print("[STARTUP] INIT_RESET=1 → A안 적용: design 테이블 드롭 후 재생성")
            reset_schema_drop_and_create(conn, EMBEDDING_DIM)
        else:
            print("[STARTUP] INIT_RESET=0 → 드롭/재생성 생략, 확장만 보장")
            ensure_extension_only(conn)
        print("[STARTUP] 스키마 준비 완료")
    except Exception as e:
        print(f"[STARTUP] 스키마 초기화 중 오류: {e}")
    finally:
        conn.close()

# -----------------------------
# 6) 라우트: /register_design
# -----------------------------
@app.post("/register_design", response_model=RegisterDesignResponse)
def register_design(payload: RegisterDesignRequest):
    """
    1) DB 연결
    2) 임베딩 결정(입력 없으면 description으로 생성)
    3) 트랜잭션 시작 → INSERT → COMMIT
      - 예외 발생 시 ROLLBACK
    """
    # 6-1) DB 연결
    try:
        conn = psycopg.connect(
            host=PGHOST,
            port=PGPORT,
            dbname=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD,
            row_factory=tuple_row,
            autocommit=False,  # 트랜잭션 수동 제어
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB 연결 실패: {e}")

    try:
        # 6-2) 임베딩 결정
        emb = payload.embedding or generate_embedding_from_text(payload.description, EMBEDDING_DIM)
        emb_sql = to_sql_vector(emb)

        # 6-3) INSERT (트랜잭션)
        with conn.cursor() as cur:
            insert_sql = """
            INSERT INTO design (title, description, embedding)
            VALUES (%s, %s, %s::vector)
            RETURNING id;
            """
            cur.execute(insert_sql, (payload.title, payload.description, emb_sql))
            new_id = cur.fetchone()[0]

        conn.commit()  # 성공 시 확정 저장
        return RegisterDesignResponse(id=new_id, title=payload.title, description=payload.description)

    except Exception as e:
        conn.rollback()  # 문제 발생 시 되돌리기
        # 개발 중 원인 파악을 돕기 위해 상세 메시지 노출(운영에서는 일반화 권장)
        raise HTTPException(status_code=500, detail=f"등록 실패(롤백됨): {type(e).__name__}: {e}")

    finally:
        conn.close()
