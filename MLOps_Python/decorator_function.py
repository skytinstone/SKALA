# Decoration Function.py
# 작성자 : 신민석
# 작성일 : 2025.08.13(수)
# 팀 명 : SKALA, SK AX AI Leader Academy 2nd
# 분 반 : 1반
# 번 호 : 15번
# ------------------------------------------------------------
# 과제 목표
# 1) 데코레이터 문법의 이해 : *args, **kwargs 활용
# 2) time module 활용
# 3) Decorator를 실제 함수에 적용하여, 실행 시간을 측정하고 출력.
# ------------------------------------------------------------
import time  # time 모듈 import

# 데코레이터 함수: measure_time
def measure_time(func):
    """
    이 데코레이터는 주어진 함수의 실행 시간을 측정하여 출력합니다.
    func: 실행 시간을 측정할 함수
    """
    def wrapper(*args, **kwargs):
        # 함수 실행 전 시간 기록
        start_time = time.time()

        # 주어진 함수(func)를 실행하고 그 결과를 result에 저장
        result = func(*args, **kwargs)

        # 함수 실행 후 시간 기록
        end_time = time.time()

        # 실행 시간 계산
        execution_time = end_time - start_time

        # 함수명과 실행 시간을 출력
        print(f"{func.__name__} took {execution_time:.4f} seconds")

        # 원래 함수의 결과를 그대로 반환
        return result

    return wrapper  # 데코레이터는 wrapper 함수를 반환

# 임의로 연산 지연을 일으키는 함수 slow_function
@measure_time  # measure_time 데코레이터를 slow_function에 적용
def slow_function():
    """
    이 함수는 일부러 2초 동안 지연이 발생하도록 하여 실행 시간을 확인하는 함수입니다.
    """
    print("작업을 시작합니다...")
    time.sleep(2)  # 2초간 대기 (연산 지연을 시뮬레이션)
    print("작업이 완료되었습니다!")

# slow_function 실행
slow_function()

