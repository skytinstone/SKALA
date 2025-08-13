# typing_mypy_benchmark.py
# 작성자 : 신민석
# 작성일 : 2025.08.13(수)
# 팀 : SKALA,SK AX AI Leader Academy 2nd
# 반 : 1반
# 번호 : 15번
# ------------------------------------------------------------
# 목적: typing과 mypy를 이용한 타입 검사 및 성능 비교
# 구조:
#   - sum_of_squares: 타입 힌트 없이 작성된 함수
#   - sum_of_squares_with_hint: 타입 힌트를 사용하여 작성된 함수
#   - timeit: 두 버전의 성능을 비교하기 위한 모듈
#   - 실행: 두 버전의 함수 실행 시간 측정 및 비교
# 동작:
#   - A Version과 B Version의 성능을 비교하여 타입 힌트의 효과를 분석
#   - A Version은 타입 힌트 없이 작성된 함수, B Version은 타입 힌트를 사용하여 작성된 함수
#   - mypy를 사용하여 타입 검사를 수행할 수 있으며, 코드의 가독성과 유지보수성을 높임
#   - 실행 시간 비교 결과를 출력
# ------------------------------------------------------------
# A Version: 타입 힌트 없이 함수 작성

import timeit
import matplotlib.pyplot as plt
from typing import List

# A Version (타입 힌트 없이 작성된 함수)
def sum_of_squares(numbers):
    total = 0
    for num in numbers:
        total += num ** 2  # 각 숫자의 제곱을 더함
    return total

# B Version (타입 힌트를 사용한 함수)
def sum_of_squares_with_hint(numbers: List[int]) -> int:
    total = 0
    for num in numbers:
        total += num ** 2  # 각 숫자의 제곱을 더함
    return total

# 예시로 사용할 입력
input_list = [4, 7, 9, 14, 25]

# Timeit을 사용하여 두 버전의 성능 비교
a_version_time = timeit.timeit('sum_of_squares(input_list)', globals=globals(), number=100000) #without type hint
b_version_time = timeit.timeit('sum_of_squares_with_hint(input_list)', globals=globals(), number=100000) #with type hint

# 결과 출력
print(f"Without Type Hint Run Time: {a_version_time:.6f} seconds")
print(f"With Type Hint Run Time: {b_version_time:.6f} seconds")
print(f"B Version is faster then A Version {a_version_time / b_version_time:.2f}times.")

# 그래프를 그리기
versions = ['Without Type Hint(Ver.A)', 'With Type Hint(Ver.B)']
times = [a_version_time, b_version_time]

# 막대 그래프 그리기
plt.bar(versions, times, color=['red', 'blue'])  # A Version : Red, B Version : Blue

# 그래프 제목 및 레이블 설정
plt.title('Bench Mark: Without Type Hint(Ver.A) vs With Type Hint(Ver.B)')
plt.xlabel('Version')
plt.ylabel('Running Time (Seconds)')

# 그래프 출력
plt.show()

print("Bench Mark is Complete.")
