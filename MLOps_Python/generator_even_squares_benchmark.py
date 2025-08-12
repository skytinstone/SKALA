# generator_even_squares_benchmark.py
# 작성자 : 신민석
# 작성일 : 2025.08.12
# 팀 명 : SKALA, SK AX AI Leader Academy 2nd
# 분 반 : 1반
# 번 호 : 15번
# ------------------------------------------------------------
# 미니 프로그램 목표
# 1) even_square_gen(n): 0 이상 n 미만 짝수의 제곱을 '하나씩' 생성(yield)
# 2) 제너레이터로 0~1,000,000 미만 짝수 제곱 총합 계산 + 시간/메모리 비교
# 3) 0~999,999 정수 총합: 리스트 방식 vs 제너레이터 방식 비교(시간/메모리)
# ------------------------------------------------------------

import sys   # sys.getsizeof()로 '객체 자체'의 메모리 바이트 크기를 확인
import time  # 실행 시간 측정을 위해 perf_counter()와 sleep 등 사용

# ------------------------------------------------------------
# [Generator] 0 이상 n 미만 정수 중 "짝수"만 골라 그 제곱을 '하나씩' 넘겨주는 함수
#  - 제너레이터는 모든 값을 메모리에 올려 두지 않고, 필요할 때마다 값을 '즉석 생성'
#  - 메모리 절약에 유리 (특히 대용량 데이터 처리 시)
# ------------------------------------------------------------
def even_square_gen(n: int):
    """0 이상 n 미만의 짝수 i에 대해 i*i(=i의 제곱)를 하나씩 생성(yield)한다."""
    # range(0, n, 2): 0부터 n-1까지 2씩 증가(=짝수만 순회)
    for i in range(0, n, 2):
        # i가 0,2,4,...일 때 i*i 값을 '하나씩' 바깥으로 전달
        yield i * i

# ------------------------------------------------------------
# [보조 제너레이터] 0 이상 n 미만의 정수를 하나씩 생성 (총합 비교용)
# ------------------------------------------------------------
def number_gen(n: int):
    """0 이상 n 미만의 정수 i를 하나씩 생성하는 제너레이터."""
    for i in range(n):
        yield i

# ------------------------------------------------------------
# [유틸] 시간 측정용 데코 없이, 블록별로 간단히 측정하는 헬퍼
# ------------------------------------------------------------
def time_block(fn, *args, **kwargs):
    """
    함수 fn(*args, **kwargs)를 실행하여 (결과, 경과초) 튜플로 반환
    - 실행 전후 time.perf_counter()로 고해상도 시간 측정
    """
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - t0
    return result, elapsed

# ------------------------------------------------------------
# Print 측정 결과 함수
# ------------------------------------------------------------
def print_measure(title: str, total, seconds: float, obj_for_size, note: str = ""):
    """
    title: 측정 제목
    total: 계산 결과(총합)
    seconds: 걸린 시간(초)
    obj_for_size: sys.getsizeof()로 메모리 크기를 확인할 '객체'
    note: 부가 설명(선택)
    """
    size = sys.getsizeof(obj_for_size)  # 주의: '객체 자체'의 크기만 측정
    print("-" * 70)
    print(title)
    print(f"  총합: {total}")
    print(f"  시간: {seconds:.6f} sec")
    print(f"  메모리(객체 자체): {size} bytes")
    if note:
        print(f"  참고: {note}")

# ------------------------------------------------------------
# 메인 실행부(__name__ == "__main__")
# ------------------------------------------------------------
if __name__ == "__main__":
    # ===== Goal: 짝수 제곱 총합: 리스트 방식 vs 제너레이터 방식 =====
    N_EVEN = 1_000_000  # 0 이상, 1,000,000 미만 -> 1번째 조건 부합

    print("=" * 70) # 구분선
    print("0 ~ 1,000,000 미만 짝수의 제곱 총합 (List vs Generator) 비교")

    # 리스트 방식: 짝수의 제곱들을 한 번에 메모리에 올려 총합
    #  - 메모리에 '값 전체'를 담는 리스트가 생김 → 메모리 사용량 큼
    def build_even_squares_list(n: int):
        # list comprehension: [i*i for i in range(0, n, 2)]
        return [i * i for i in range(0, n, 2)]

    # 리스트 생성과 총합 계산을 분리해 시간 오차를 줄일 수도 있지만,
    # 여기서는 "생성 후 바로 합계" 형태로 측정합니다.
    even_squares_list, t_list_build = time_block(build_even_squares_list, N_EVEN)
    sum_even_list, t_list_sum = time_block(sum, even_squares_list)
    
    # 결과 출력
    print_measure( 
        title="리스트 방식",
        total=sum_even_list,
        seconds=t_list_build + t_list_sum,
        obj_for_size=even_squares_list,
        note="리스트 자체 크기만 측정됩니다. 요소(정수 객체)들의 합산 메모리는 포함되지 않습니다."
    )

    # Generator 방식: 값을 '필요할 때마다' 하나씩 생성하여 총합
    #  - 메모리 사용량 매우 작음(Generator 객체 자체만 존재)
    #  - 이미 소비한 Generator는 재사용 불가 → 메모리 크기 측정용은 별도 생성
    gen_obj_for_sum = even_square_gen(N_EVEN)
    sum_even_gen, t_gen_sum = time_block(sum, gen_obj_for_sum)
    gen_obj_for_size = even_square_gen(N_EVEN)  # 메모리 측정용(소비하지 않은 새 객체)
    
    # 결과 출력
    print_measure(
        title="Generator 방식",
        total=sum_even_gen,
        seconds=t_gen_sum,
        obj_for_size=gen_obj_for_size,
        note="Generator는 값을 즉시 만들고 버려서 메모리가 매우 작습니다."
    )

    # ===== 0 ~ 999,999 정수 총합: 리스트 vs 제너레이터 =====
   
    N_ALL = 1_000_000 # 0 이상, 1,000,000 미만 -> 2번째 조건 부합

    print("=" * 70) # 구분선
    print("Step 2. 0 ~ 999,999 정수 총합 (List vs Generator)")

    # 리스트 방식: 0..999,999를 메모리에 '전부' 담은 뒤 합계
    def build_all_numbers_list(n: int):
        return list(range(n))  # list(range(...))는 모든 숫자를 메모리에 저장

    all_numbers_list, t_build_all = time_block(build_all_numbers_list, N_ALL)
    sum_all_list, t_sum_all_list = time_block(sum, all_numbers_list)
    
    # 결과 출력
    print_measure(
        title="List 방식",
        total=sum_all_list,
        seconds=t_build_all + t_sum_all_list,
        obj_for_size=all_numbers_list,
        note="리스트 객체의 크기만 표시됩니다(요소 메모리는 포함되지 않음)."
    )

    # 제너레이터 방식: 0..999,999를 '하나씩' 만들어 합계
    gen_all_for_sum = number_gen(N_ALL)     # 합계 계산용(소비됨)
    sum_all_gen, t_sum_all_gen = time_block(sum, gen_all_for_sum)
    gen_all_for_size = number_gen(N_ALL)    # 메모리 측정용(소비안한 새 객체)
    
    # 결과 출력
    print_measure(
        title="Generator 방식",
        total=sum_all_gen,
        seconds=t_sum_all_gen,
        obj_for_size=gen_all_for_size,
        note="Generator 객체 자체의 크기만 측정됩니다."
    )

    # ===== 요약/안내 =====
    print("=" * 70) # 구분선
    print("[안내] sys.getsizeof()는 '객체 자체'의 크기만 반환합니다.")
    print(" - 리스트의 요소(정수 객체)들이 차지하는 메모리 총합은 포함되지 않습니다.")
    print(" - 제너레이터는 데이터를 보관하지 않아 객체 자체 크기가 매우 작게 나타납니다.")
    print(" - 대용량 데이터에서는 제너레이터가 메모리 측면에서 특히 유리합니다.")
