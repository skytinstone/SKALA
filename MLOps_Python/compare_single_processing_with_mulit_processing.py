# Compare_single_processing_with_multi_processing.py
# 작성자 : 신민석
# 작성일 : 2025.08.13(수)
# 팀 : SKALA,SK AX AI Leader Academy 2nd
# 반 : 1반
# 번호 : 15번
# ------------------------------------------------------------
# 목적: single Processing과 Multi Processing의 실행 시간 비교
# 구조:
#   - is_prime: 소수 판별 함수
#   - count_primes_single: 단일 프로세스 방식으로 소수 개수 세기
#   - count_primes_multiprocessing: 멀티 프로세스 방식으로 소수 개수 세기
#   - generate_random_numbers: 1,000만 개의 난수 생성
#   - run_experiment: 실행 시간 비교 함수
#   - 실행: run_experiment 함수 호출 및 결과 출력
#   - 실행 시간 비교 그래프 그리기
# 동작:
#   - 1,000만 개의 난수를 생성하고 단일 프로세스과 멀티 프로세스 방식으로 소수 개수를 세어 실행 시간을 비교
#   - 실행 시간 비교 결과를 그래프로 시각화
#   - 소수 판별 기능을 구현하여 소수 개수를 세는 프로그램
#   - 단일 프로세스과 멀티 프로세스 방식의 실행 시간을 비교하여 성능 차이를 분석
# ------------------------------------------------------------
# 필요한 Module import
import random                   # 난수 생성을 위한 모듈
import math                     # 수학적 연산을 위한 모듈
import time                     # 시간 측정을 위한 모듈
import multiprocessing          # 멀티 프로세싱을 위한 모듈

# 소수 판별 함수
def is_prime(n):
    """
    주어진 숫자 n이 소수인지 판별하는 함수
    소수는 1과 자기 자신만을 약수로 가지는 수입니다.
    """
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# 단일 프로세스 방식으로 소수 개수 세기
def count_primes_single(numbers):
    count = 0
    for num in numbers:
        if is_prime(num):
            count += 1
    return count

# 멀티 프로세스 방식으로 소수 개수 세기 (멀티프로세싱 풀 사용)
def count_primes_multiprocessing(numbers):
    # 멀티프로세싱 풀을 이용하여 여러 프로세스에서 작업을 병렬로 처리
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        result = pool.map(is_prime, numbers)
    return sum(result)

# 1,000만 개의 난수를 생성
def generate_random_numbers():
    return [random.randint(1, 10000000) for _ in range(10000000)]

# 실행 시간 비교 함수
def run_experiment():
    # 난수 생성
    numbers = generate_random_numbers()

    # 단일 프로세스 실행 시간 측정
    start_time = time.time()
    prime_count_single = count_primes_single(numbers)
    time_single = time.time() - start_time

    # 멀티 프로세스 실행 시간 측정
    start_time = time.time()
    prime_count_multi = count_primes_multiprocessing(numbers)
    time_multi = time.time() - start_time

    return time_single, time_multi, prime_count_single, prime_count_multi

# 실행
if __name__ == "__main__":  # 멀티프로세싱을 사용할 때 필요한 안전 장치
    time_single, time_multi, prime_count_single, prime_count_multi = run_experiment()

    # 결과 출력
    print(f"단일 프로세스 방식으로 소수 개수: {prime_count_single}")
    print(f"멀티 프로세스 방식으로 소수 개수: {prime_count_multi}")
    print(f"단일 프로세스 실행 시간: {time_single:.4f} 초")
    print(f"멀티 프로세스 실행 시간: {time_multi:.4f} 초")

# ----------------------------------------------------------------
