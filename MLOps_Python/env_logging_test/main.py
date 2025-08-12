 # main.py
# ------------------------------------------------------------
# 목적:
#   - .env에서 환경변수(로그레벨, 앱이름)를 읽어온 뒤
#   - logging 모듈로 "콘솔 + 파일" 로깅을 동시에 설정하고
#   - 예시 로그(INFO/DEBUG/ERROR)를 출력한다.
# ------------------------------------------------------------

import os                                  # 환경변수 접근용(표준 라이브러리)
import sys                                 # 인터프리터 경로 확인용(진단)
from pathlib import Path                   # 경로 조작을 간단히
import logging                             # 표준 로깅 모듈
from logging.handlers import RotatingFileHandler  # (선택) 로그 파일 회전 핸들러
try:
    from dotenv import load_dotenv         # .env 파일 로더
except Exception as e:
    # python-dotenv가 없는 경우를 대비한 친절 메시지
    print("[ERROR] 'python-dotenv'가 설치되어 있지 않습니다.")
    print("        설치 후 다시 실행하세요:  pip install python-dotenv")
    raise

# === 1) .env 로드 (.env는 현재 파일과 동일한 폴더에 있다고 가정) ===
BASE_DIR = Path(__file__).resolve().parent         # main.py가 있는 폴더
ENV_FILE = BASE_DIR / ".env"                       # .env 파일 경로
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)                          # 지정 경로의 .env를 로드
else:
    # .env가 없으면 실습 취지에 맞게 경고만 출력하고 계속 진행
    print(f"[WARN] .env not found at {ENV_FILE}. Using default values.")

# === 2) 환경변수 읽기 (없을 경우 기본값 지정) ===
LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "INFO")     # 예: "DEBUG", "INFO" 등
APP_NAME = os.getenv("APP_NAME", "MyCoolApp")      # 앱 이름(기본: MyCoolApp)

# 문자열 LOG_LEVEL을 실제 logging 레벨 상수로 변환하는 헬퍼
LEVEL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR":    logging.ERROR,
    "WARNING":  logging.WARNING,
    "INFO":     logging.INFO,
    "DEBUG":    logging.DEBUG,
    "NOTSET":   logging.NOTSET,
}
LOG_LEVEL = LEVEL_MAP.get(LOG_LEVEL_STR.upper(), logging.INFO)  # 기본 INFO

# === 3) 로깅 설정 ===
# 포맷: 시간 | 로그레벨 | 메시지  (요구사항)
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"                   # 시간 포맷(가독성 위해 지정)

# 로그 파일 경로: env_logging_test/app.log (main.py와 동일 폴더 기준)
LOG_FILE = BASE_DIR / "app.log"

# (A) 파일 핸들러: 파일로 로그를 남김
#     - RotatingFileHandler 사용: 파일이 너무 커질 경우 자동으로 백업/순환(옵션)
file_handler = RotatingFileHandler(
    LOG_FILE,                 # 로그 파일 경로
    maxBytes=2_000_000,       # (선택) 2MB 넘으면 회전
    backupCount=3,            # (선택) 백업 3개 보관
    encoding="utf-8"          # 한글 로그 깨짐 방지
)
file_handler.setLevel(LOG_LEVEL)                      # 파일에 쓸 최소 레벨
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

# (B) 콘솔 핸들러: 화면(터미널)에도 출력
console_handler = logging.StreamHandler()             # 표준 출력으로 로그
console_handler.setLevel(LOG_LEVEL)                   # 콘솔에 쓸 최소 레벨
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

# (C) 루트 로거 구성: 두 핸들러를 모두 추가
logger = logging.getLogger(APP_NAME)                  # 앱 이름으로 로거 생성
logger.setLevel(LOG_LEVEL)                            # 로거 자체 레벨
# 중복 핸들러 추가 방지(재실행 시 여러 번 붙는 현상 방지)
if not logger.handlers:
    logger.addHandler(file_handler)                   # 파일로 로그
    logger.addHandler(console_handler)                # 콘솔로 로그
    logger.propagate = False                          # 상위 로거로 전파 방지

# === 4) 예시 로그 메시지 출력 (요구사항) ===
# (a) [INFO] 앱 실행 시작
logger.info("앱 실행 시작")                           # 정보 레벨 메시지

# (b) [DEBUG] 환경 변수 로딩 완료
logger.debug("환경 변수 로딩 완료 "
             f"(LOG_LEVEL={LOG_LEVEL_STR}, APP_NAME={APP_NAME})")

# (c) [ERROR] 예외 발생 예시
try:
    # 일부러 1/0을 시도해서 ZeroDivisionError를 발생시킴(예시)
    _ = 1 / 0
except Exception as exc:
    # exc_info=True 로 스택트레이스(에러 위치)도 함께 남김
    logger.error("예외 발생 예시(의도적 ZeroDivisionError)", exc_info=True)

# === 5) 종료 안내(가독성용) ===
logger.info("앱 실행 종료")
print(f"[INFO] Log file created/updated at: {LOG_FILE.resolve()}")
