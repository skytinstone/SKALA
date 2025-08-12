# log_out.py
# 작성자 : 신민석
# 작성일 : 2025.08.12
# 팀 명 : SKALA, SK AX AI Leader Academy 2nd
# 분 반 : 1반
# 번 호 : 15번  
# ------------------------------------------------------------
# 목적: ".env + logging" 실습용 폴더/파일 자동 생성 + 실행
# 구조: ./env_logging_test/{ .env, main.py, app.log(실행 후 생성) }
# 동작:
#   - env_logging_test 폴더가 없으면 생성(있으면 건너뜀)
#   - .env, main.py 파일이 없으면 생성(있으면 보존)
#   - python-dotenv 미설치 시 자동 설치 시도
#   - main.py 실행하여 콘솔+파일 로깅 확인(app.log 생성)
# ------------------------------------------------------------

import os               # 폴더/파일 존재 확인 및 경로 조작용(표준 라이브러리)
import sys              # 현재 파이썬 경로/인터프리터 확인 및 하위 프로세스 실행용
import subprocess       # 현재 인터프리터로 다른 파이썬 파일 실행(popen)
from pathlib import Path  # 경로를 다루기 쉽게 해주는 표준 라이브러리

# 1) 실습 폴더 이름을 정의
TARGET_DIR = Path("env_logging_test")  # 생성될 폴더 이름

# 2) 생성할 파일 경로(.env / main.py / app.log)를 미리 준비
ENV_PATH = TARGET_DIR / ".env"         # .env 파일 경로
MAIN_PATH = TARGET_DIR / "main.py"     # 실행용 메인 스크립트 경로
LOG_PATH  = TARGET_DIR / "app.log"     # 로그 파일 경로(실행 후 생성 예정)

# 3) 폴더가 존재하는지 확인하고, 없으면 생성
#    - "최초 실행 시에만" 폴더가 만들어지고, 이미 있으면 아무 것도 하지 않음
if not TARGET_DIR.exists():            # 폴더가 없다면
    TARGET_DIR.mkdir(parents=True, exist_ok=True)  # 폴더 생성(중간폴더까지)
    print(f"[INFO] Created folder: {TARGET_DIR}")
else:
    print(f"[INFO] Folder already exists: {TARGET_DIR} (skip creating)")

# 4) .env 파일이 없으면 기본 내용으로 생성 (있으면 건너뜀)
#    - 요구사항: LOG_LEVEL=DEBUG, APP_NAME=MyCoolApp
if not ENV_PATH.exists():              # .env가 없다면
    ENV_CONTENT = (
        "LOG_LEVEL=DEBUG\n"            # 로그 레벨(예: DEBUG/INFO/WARNING/ERROR/CRITICAL)
        "APP_NAME=MyCoolApp\n"         # 앱 이름
    )
    ENV_PATH.write_text(ENV_CONTENT, encoding="utf-8")  # utf-8형태의 파일 생성/쓰기
    print(f"[INFO] Created .env at: {ENV_PATH}") #  생성 완료 메시지
else:
    print(f"[INFO] .env already exists: {ENV_PATH} (skip writing)") #  존재 메시지

# 5) main.py가 없으면 생성(있으면 보존)
#    - 이 파일이 실제 서비스 코드 예시: .env 읽고, logging 설정 후 메시지 출력
if not MAIN_PATH.exists():
    MAIN_SOURCE = r''' # main.py
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

# 파일 핸들러: 파일로 로그를 남김
#     - RotatingFileHandler 사용: 파일이 너무 커질 경우 자동으로 백업/순환(옵션)
file_handler = RotatingFileHandler(
    LOG_FILE,                 # 로그 파일 경로
    maxBytes=2_000_000,       # (선택) 2MB 넘으면 회전
    backupCount=3,            # (선택) 백업 3개 보관
    encoding="utf-8"          # 한글 로그 깨짐 방지
)
file_handler.setLevel(LOG_LEVEL)                      # 파일에 쓸 최소 레벨
file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

# 콘솔 핸들러: 화면(터미널)에도 출력
console_handler = logging.StreamHandler()             # 표준 출력으로 로그
console_handler.setLevel(LOG_LEVEL)                   # 콘솔에 쓸 최소 레벨
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))

# 루트 로거 구성: 두 핸들러를 모두 추가
logger = logging.getLogger(APP_NAME)                  # 앱 이름으로 로거 생성
logger.setLevel(LOG_LEVEL)                            # 로거 자체 레벨
# 중복 핸들러 추가 방지(재실행 시 여러 번 붙는 현상 방지)
if not logger.handlers:
    logger.addHandler(file_handler)                   # 파일로 로그
    logger.addHandler(console_handler)                # 콘솔로 로그
    logger.propagate = False                          # 상위 로거로 전파 방지

# === 4) 예시 로그 메시지 출력 (요구사항) ===
# [INFO] 앱 실행 시작
logger.info("앱 실행 시작")                           # 정보 레벨 메시지

# [DEBUG] 환경 변수 로딩 완료
logger.debug("환경 변수 로딩 완료 "
             f"(LOG_LEVEL={LOG_LEVEL_STR}, APP_NAME={APP_NAME})")

# [ERROR] 예외 발생 예시
try:
    # 일부러 1/0을 시도해서 ZeroDivisionError를 발생시킴(예시)
    _ = 1 / 0
except Exception as exc:
    # exc_info=True 로 스택트레이스(에러 위치)도 함께 남김
    logger.error("예외 발생 예시(의도적 ZeroDivisionError)", exc_info=True)

# === 5) 종료 안내(가독성용) ===
logger.info("앱 실행 종료")
print(f"[INFO] Log file created/updated at: {LOG_FILE.resolve()}")
'''
    MAIN_PATH.write_text(MAIN_SOURCE, encoding="utf-8")  # main.py 파일 생성
    print(f"[INFO] Created main.py at: {MAIN_PATH}")
else:
    print(f"[INFO] main.py already exists: {MAIN_PATH} (skip writing)")

# 6) python-dotenv이 설치되어 있는지 확인하고, 없으면 자동 설치 시도
#    - main.py에서 import 실패하지 않도록 사전 보장
def ensure_dotenv_installed() -> bool:
    """python-dotenv 설치 여부를 확인하고, 없으면 현재 인터프리터로 설치 시도"""
    try:
        import dotenv  # noqa: F401  # 실제 사용은 main.py가 함(여긴 존재 확인만)
        return True
    except Exception:
        print("[INFO] python-dotenv not found. Trying to install...")
        # 현재 파이썬 인터프리터로 pip 실행
        cmd = [sys.executable, "-m", "pip", "install", "python-dotenv"]
        try:
            subprocess.check_call(cmd)
            print("[INFO] Installed python-dotenv successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print("[ERROR] Failed to install python-dotenv. Please install manually:")
            print("       pip install python-dotenv")
            return False

dotenv_ok = ensure_dotenv_installed()
if not dotenv_ok:
    # 설치가 안되면 main.py 실행 시 import 에러가 날 수 있으므로 종료
    sys.exit(1)

# 7) main.py 실행
#    - 현재 인터프리터(sys.executable)로 main.py를 실행
#    - cwd를 env_logging_test로 잡아 app.log가 그 폴더에 생성되게 함
print("[INFO] Running main.py ...")
run_cmd = [sys.executable, str(MAIN_PATH.name)]  # ex) ["python", "main.py"]
proc = subprocess.run(run_cmd, cwd=str(TARGET_DIR))  # cwd를 대상 폴더로 지정
if proc.returncode == 0:
    print("[INFO] main.py finished successfully.")
    # 실행이 끝나면 app.log가 생성되어 있어야 함
    if LOG_PATH.exists():
        print(f"[INFO] OK: {LOG_PATH} exists.")
    else:
        print(f"[WARN] app.log not found at: {LOG_PATH}")
else:
    print(f"[ERROR] main.py exited with code {proc.returncode}")
