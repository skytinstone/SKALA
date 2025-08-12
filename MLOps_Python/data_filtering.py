# data_filtering.py
# 작성자 : 신민석 
# 작성일 : 2025.08.12
# 팀 명 : SKALA,SK AX AI Leader Academy 2nd 
# 분 반 : 1반
# 번 호 : 15번
# ------------------------------------------------------------
# 과제명: Data Filtering (Python / List + Dictionary 실습)
# 목표:
#   1) 리스트 안의 딕셔너리에서 조건에 맞는 데이터 필터링
#   2) for, if, list comprehension, filter() 등을 고루 활용
# 출력:
#   - 문제 1: 부서가 "Engineering"이고 salary >= 80000인 직원 이름 리스트
#   - 문제 2: 30세 이상 직원의 (name, department) 튜플 리스트
#   - 문제 3: salary 내림차순 정렬 후 상위 3명의 (name, salary)
#   - 문제 4: 모든 부서별 평균 급여를 출력하는 코드 작성
# ------------------------------------------------------------

# 실습에 사용할 직원 데이터(리스트 내부에 딕셔너리들이 들어있는 형태)
employees = [
    {"name": "Alice",   "department": "Engineering", "age": 30, "salary": 85000},  # 직원 1
    {"name": "Bob",     "department": "Marketing",   "age": 25, "salary": 60000},  # 직원 2
    {"name": "Charlie", "department": "Engineering", "age": 35, "salary": 95000},  # 직원 3
    {"name": "David",   "department": "HR",          "age": 45, "salary": 70000},  # 직원 4
    {"name": "Eve",     "department": "Engineering", "age": 28, "salary": 78000},  # 직원 5
]

# 문제 1 ------------------------------------------------------
# 조건: 부서가 "Engineering" 이고, salary >= 80000 인 직원들의 "이름"만 리스트로 만들기

# [방법 A] 전통적인 for + if 사용 예시
eng_high_paid_names_for = []  # 결과를 담을 비어있는 리스트 생성
for emp in employees:  # 직원 리스트를 처음부터 끝까지 순회
    if emp["department"] == "Engineering" and emp["salary"] >= 80000:  # 부서/급여 조건 체크
        eng_high_paid_names_for.append(emp["name"])  # 조건 만족 시 이름만 결과 리스트에 추가

# [방법 B] 리스트 컴프리헨션(list comprehension) 사용 예시 (짧고 간결하게 같은 로직 구현)
eng_high_paid_names_comp = [
    emp["name"]  # 사후에 남길 값(이름)
    for emp in employees  # 순회 대상
    if emp["department"] == "Engineering" and emp["salary"] >= 80000  # 필터 조건
]

# [방법 C] filter() + lambda 사용 예시 (filter로 걸러낸 뒤, map/list로 이름만 추출)
eng_high_paid_filtered = filter(  # filter는 조건을 만족하는 요소만 걸러줌(이터레이터 반환)
    lambda e: e["department"] == "Engineering" and e["salary"] >= 80000,  # 필터 조건
    employees,  # 대상 리스트
)
eng_high_paid_names_filter = [e["name"] for e in eng_high_paid_filtered]  # 걸러진 직원들에서 이름만 리스트로 뽑기

# 문제 2 ------------------------------------------------------
# 조건: 30세 이상인 직원의 (name, department) 튜플 리스트 만들기

# [방법 A] 전통적인 for + if 사용
age30_tuples_for = []  # 결과 저장 리스트
for emp in employees:  # 전체 직원 순회
    if emp["age"] >= 30:  # 나이 조건 확인
        age30_tuples_for.append((emp["name"], emp["department"]))  # (이름, 부서) 튜플 추가

# [방법 B] 리스트 컴프리헨션 사용
age30_tuples_comp = [
    (emp["name"], emp["department"])  # 최종적으로 남길 (이름, 부서) 튜플
    for emp in employees  # 순회 대상
    if emp["age"] >= 30  # 필터 조건
]

# [방법 C] filter() + lambda + 리스트 변환
age30_filtered = filter(  # 조건에 맞는 직원만 남김
    lambda e: e["age"] >= 30,  # 나이 조건
    employees,  # 대상 리스트
)
age30_tuples_filter = [(e["name"], e["department"]) for e in age30_filtered]  # (이름, 부서) 튜플로 변환

# 문제 3 ------------------------------------------------------
# 조건: 급여(salary) 기준으로 직원 리스트를 "내림차순" 정렬하고, 상위 3명의 (name, salary) 출력
# 주의: 원본 리스트를 보존하고 싶다면 sorted()를 사용(새 리스트 생성)

# [방법 A] sorted() + lambda로 내림차순 정렬 (원본 보존)
sorted_by_salary_desc = sorted(  # 새로운 정렬된 리스트를 반환
    employees,  # 대상 리스트
    key=lambda e: e["salary"],  # 정렬 기준: salary 값
    reverse=True,  # 내림차순 정렬 옵션
)
top3_by_salary_a = [(e["name"], e["salary"]) for e in sorted_by_salary_desc[:3]]  # 상위 3명만 (이름, 급여)로 추출

# [방법 B] list.copy()로 복사 후 .sort() 사용 (제자리 정렬, 복사본만 변경)
employees_copy = employees.copy()  # 원본 보호를 위해 얕은 복사본 생성
employees_copy.sort(  # 복사본 리스트를 직접 정렬(반환값 없음)
    key=lambda e: e["salary"],  # 정렬 기준: salary
    reverse=True,  # 내림차순
)
top3_by_salary_b = [(e["name"], e["salary"]) for e in employees_copy[:3]]  # 상위 3명 추출

# ------------------- 문제 4 코드 시작 -------------------

# 부서별 급여 합계와 직원 수를 저장할 딕셔너리 생성
dept_salary_data = {}

# 전체 직원 순회
for emp in employees:
    dept = emp["department"]      # 현재 직원의 부서
    salary = emp["salary"]        # 현재 직원의 급여
    
    # 부서가 딕셔너리에 없으면 초기값 설정
    if dept not in dept_salary_data:
        dept_salary_data[dept] = {"sum": 0, "count": 0}
    
    # 해당 부서의 합계와 직원 수 누적
    dept_salary_data[dept]["sum"] += salary
    dept_salary_data[dept]["count"] += 1

# ---------------- 출력부 ----------------
# 보기 좋게 구분선을 출력하여 결과를 확인하기 쉽게 함
print("=" * 60)  # 구분선 출력
print("문제 1) 부서가 'Engineering' 이고 salary >= 80000 인 직원 이름 리스트")  # 문제1 제목 출력
print("- for+if :", eng_high_paid_names_for)  # 방법 A 결과 출력
print("- list comprehension :", eng_high_paid_names_comp)  # 방법 B 결과 출력
print("- filter() :", eng_high_paid_names_filter)  # 방법 C 결과 출력

print("=" * 60)  # 구분선 출력
print("문제 2) 30세 이상 직원의 (name, department) 튜플 리스트")  # 문제2 제목 출력
print("- for+if :", age30_tuples_for)  # 방법 A 결과 출력
print("- list comprehension :", age30_tuples_comp)  # 방법 B 결과 출력
print("- filter() :", age30_tuples_filter)  # 방법 C 결과 출력

print("=" * 60)  # 구분선 출력
print("문제 3) salary 내림차순 정렬 후 상위 3명의 (name, salary)")  # 문제3 제목 출력
print("- sorted() 사용 :", top3_by_salary_a)  # 방법 A 결과 출력
print("- sort() 사용   :", top3_by_salary_b)  # 방법 B 결과 출력

print("=" * 60)  # 구분선 출력
print("문제 4) 모든 부서별 평균 급여를 출력하는 코드를 작성해보세요.") # 문제 4 제목 출력
for dept, data in dept_salary_data.items():  # 부서별로 순회
    avg_salary = data["sum"] / data["count"] if data["count"] > 0 else 0  # 평균 급여 계산
    print(f"{dept} 부서의 평균 급여: {avg_salary:.2f}")  # 결과 출력 (소수점 둘째 자리까지)
print("=" * 60)  # 구분선 출력