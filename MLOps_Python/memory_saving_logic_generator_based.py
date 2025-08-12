# generator_memory_comparison_time_series_smooth.py
# 작성자 : 신민석
# 작성일 : 2025.08.12
# 팀 명 : SKALA, SK AX AI Leader Academy 2nd
# 분 반 : 1반
# 번 호 : 15번
# ------------------------------------------------------------
# 과제명: Generator Based Memory 절약형 Logic (시간축 + 부드러운 선)
# 목표:
#   1) 제너레이터(generator)의 개념 및 필요성 이해
#   2) 메모리를 효율적으로 사용하는 코드 작성법 익히기
#   3) yield, next(), for 루프를 이용한 generator 활용
#   4) 시간(ms) 축으로 10초 간격을 둔 두 라인을 "부드러운 선"으로 시각화
# ------------------------------------------------------------

import sys                      # sys.getsizeof()로 객체 메모리 크기 확인
import time                     # 시간 측정(밀리초) 및 지연(sleep)
import matplotlib.pyplot as plt # 그래프 그리기

# ------------------------------------------------------------
# 0) 그래프 스타일(부드러운 선 연출용) 설정
# ------------------------------------------------------------
plt.rcParams["lines.antialiased"] = True   # 선의 계단 느낌을 줄이는 안티에일리어싱
plt.rcParams["path.simplify"] = True       # 경로 단순화(자잘한 각종 끊김 완화)
plt.rcParams["path.simplify_threshold"] = 0.0  # 단순화 임계값(0이면 원형에 가깝게)

# ------------------------------------------------------------
# 1) 리스트 방식: 0 ~ 999,999를 담은 리스트와 메모리 사용량
# ------------------------------------------------------------
numbers_list = list(range(1_000_000))      # 모든 정수를 메모리에 저장(메모리 사용량 큼)
list_sum = sum(numbers_list)               # 합계 계산
list_mem = sys.getsizeof(numbers_list)     # "리스트 객체 자체"의 바이트 크기

print("=" * 60)
print("1단계) 일반 리스트 방식")
print(f"합계: {list_sum}")
print(f"메모리 사용량: {list_mem} bytes")

# ------------------------------------------------------------
# 2) 제너레이터 방식: 필요할 때마다 하나씩 값 생성(메모리 사용량 작음)
# ------------------------------------------------------------
def number_generator(n):
    """0부터 n-1까지 숫자를 하나씩 '즉석에서' 만들어 내는 제너레이터 함수"""
    for i in range(n):
        yield i

numbers_gen = number_generator(1_000_000)  # 제너레이터 객체 생성(데이터를 들고 있지 않음)
gen_sum = sum(numbers_gen)                 # 순회하며 합계를 계산(사용하면 소모됨)

# 메모리 측정은 새 제너레이터로 수행(이미 소모되었기 때문)
gen_for_size = number_generator(1_000_000)
gen_mem = sys.getsizeof(gen_for_size)      # 제너레이터 객체 자체의 바이트 크기(아주 작음)

print("=" * 60)
print("2단계) 제너레이터 방식")
print(f"합계: {gen_sum}")
print(f"메모리 사용량: {gen_mem} bytes")

# ------------------------------------------------------------
# 3) 시간축 그래프(부드러운 선)
#   - x축: 시간(ms), y축: bytes
#   - 리스트 측정 후 10초 쉬고 제너레이터 측정 (요구사항 반영)
#   - 선을 부드럽게 보이도록: 샘플 수↑(촘촘히), 마커 제거, 라인 굵기 적당히
# ------------------------------------------------------------

t0 = time.perf_counter()   # 공통 기준 시작 시각(두 시리즈 모두 같은 기준 사용)

# ----- 리스트(List) 비교군 -----
list_times_ms = []         # x축 값(밀리초)
list_values   = []         # y축 값(바이트)
samples = 200              # 포인트를 촘촘히 찍어 선을 부드럽게
interval = 0.01            # 10ms 간격으로 측정

for _ in range(samples):
    now_ms = (time.perf_counter() - t0) * 1000.0  # 기준 시각 대비 경과 시간(ms)
    list_times_ms.append(now_ms)                  # 시간 기록
    list_values.append(list_mem)                  # 리스트 객체 자체 크기(고정값)
    time.sleep(interval)                          # 다음 포인트까지 10ms 대기

# ----- 10초 대기 -----
time.sleep(10)

# 10ms 간격 -----
gen_times_ms = []          # x축(밀리초)
gen_values   = []          # y축(바이트)

gen_for_plot = number_generator(1_000_000)   # 의미상 새 객체 생성
gen_mem_plot = sys.getsizeof(gen_for_plot)   # 제너레이터 객체 자체 크기(작고 일정)

for _ in range(samples):
    now_ms = (time.perf_counter() - t0) * 1000.0  # 같은 기준으로 시간 계산
    gen_times_ms.append(now_ms)                   # 시간 기록
    gen_values.append(gen_mem_plot)               # 제너레이터 객체 크기(고정값)
    time.sleep(interval)                          # 다음 포인트까지 10ms 대기

# ------------------------------------------------------------
# 4) 그래프 시각화
# ------------------------------------------------------------
plt.figure(figsize=(11, 6))                                         # 그림 크기
plt.plot(list_times_ms, list_values, linewidth=2.2,                 # 굵은 선으로 부드럽게
         color="red", label="List (object size)")                    # 빨간색: 리스트
plt.plot(gen_times_ms,  gen_values,  linewidth=2.2,
         color="blue", label="Generator (object size)")              # 파란색: 제너레이터

plt.title("Memory Usage over Time (List vs Generator) — 10s gap, smoother lines")
plt.xlabel("Time (ms)")                                             # x축: 시간(ms)
plt.ylabel("Memory Usage (bytes)")                                  # y축: 바이트
plt.legend()                                                        # 범례 표시
plt.grid(True, linewidth=0.4, alpha=0.6)                            # 그리드

plt.tight_layout()                                                  # 여백 자동 조정
plt.show()                                                          # 그래프 띄우기

