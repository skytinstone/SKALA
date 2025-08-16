# pandas_seaborn_analysis_report.py
# 작성자 : 신민석
# 작성일 : 2025.08.14(목)
# 팀 : SKALA,SK AX AI Leader Academy 2nd
# 반 : 1반
# 번호 : 15번
# ------------------------------------------------------------
# 목적: typing과 mypy를 이용한 타입 검사 및 성능 비교
# 구조:
#   -   Phase 1: Pretraining
#   -   Phase 2: Visualization
#   -   Phase 3: AI analysis
#   -   Phase 4: Reporting
# 동작:
#   -   1. reviews.csv 파일을 불러와 데이터 전처리
#   -   2. seaborn을 이용하여 데이터 시각화
#   -   3. AI 분석을 위한 인사이트 도출
#   -   4. 분석 결과를 리포트로 작성
#   -   5. 리포트를 Markdown 형식으로 저장
#   -   6. 필요시 PDF로 변환 가능
#   -   7. 각 단계별로 주석을 추가하여 코드 이해를 돕기
#   -   8. 이상치 탐지 및 결측치 처리
#   -   9. 카테고리별 분석 및 시각화
#   -   10. 감성 점수와 평점 간의 관계 분석
#   -   11. 텍스트 길이와 평점 간의 관계 분석
#   -   12. 결과 리포트를 Markdown 형식으로 작성 및 저장
#   -   13. 리포트는 Markdown 형식으로 작성되며,
#       필요시 PDF로 변환 가능
#   -   14. 각 단계별로 필요한 라이브러리와 함수들을
#       import하여 사용
#   -   15. 데이터 분석 및 시각화에 필요한 라이브러리
#       (pandas, seaborn, matplotlib 등)을 사용
#   -   16. 데이터 전처리, 시각화, AI 분석,
#       리포트 작성 등 각 단계별로 명확하게 구분
#   -   17. 각 단계별로 필요한 함수와 메서드를 사용하여
#       데이터 분석 및 시각화를 수행
#   -   18. 최종적으로 분석 결과를 리포트로 작성하여
#       저장하는 구조로 작성
# ------------------------------------------------------------
# import necessary libraries
# pandas, seaborn, matplotlib.pyplot 등 데이터 분석 및 시각화에 필요한 라이브
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# Phase 1 : Pretraining
# ----------------------------------------------------------

# 1. reviews.csv 파일 불러오기
data = pd.read_csv('/Users/minseok/workspace/basic/MLOps_Python/reviews.csv')

# 2. 데이터 확인: 상위 5개 데이터 출력
print(data.head())

# 3. 결측치 확인
print(data.isnull().sum())  # 각 열에서 결측치가 얼마나 있는지 확인

# 결측치 처리: 예시로 평균으로 채우기
data['review_length'].fillna(data['review_length'].mean(), inplace=True)

# 4. 분포 시각화: 'review_length'와 'rating'의 분포를 히스토그램으로 확인
sns.histplot(data['review_length'], kde=True)
plt.title('Review Length Distribution')
plt.show()

# 이상치 탐지: IQR 방식으로 'review_length'의 이상치 확인
Q1 = data['review_length'].quantile(0.25)
Q3 = data['review_length'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# 이상치 필터링
outliers = data[(data['review_length'] < lower_bound) | (data['review_length'] > upper_bound)]
print(f"이상치 데이터:\n{outliers}")

# ----------------------------------------------------------
# Phase 2 : Visualization
# ----------------------------------------------------------

# 1. review_length와 rating에 대한 기술 통계 요약
print(data[['review_length', 'rating']].describe())

# 2. category별 평균 평점 시각화
sns.barplot(x='category', y='rating', data=data)
plt.title('Category-wise Average Rating')
plt.xticks(rotation=45)
plt.show()

# 3. 평점과 감성 점수 관계 시각화
sns.scatterplot(x='rating', y='sentiment_score', data=data)
plt.title('Rating vs Sentiment Score')
plt.show()

# 4. 텍스트 길이와 평점의 관계 (Violin plot)
sns.violinplot(x='rating', y='review_length', data=data)
plt.title('Review Length vs Rating')
plt.show()


#-----------------------------------------------------------
# Phase 3 : AI analysis
#-----------------------------------------------------------

# 1. sentiment_score가 높을수록 평점이 높나?
sns.boxplot(x='rating', y='sentiment_score', data=data)
plt.title('Sentiment Score vs Rating')
plt.show()

# 2. Review_length와 AI 임베딩 유사도 관계 확인 (예시로 review_length가 유사도에 영향을 줄 수 있는지 탐지)
# 여기서는 단순히 review_length와 rating 간의 관계를 보겠습니다.
sns.scatterplot(x='review_length', y='sentiment_score', data=data)
plt.title('Review Length vs Sentiment Score')
plt.show()

# 3. 카테고리별 감성 점수 평균 차이
sns.barplot(x='category', y='sentiment_score', data=data)
plt.title('Category-wise Sentiment Score')
plt.xticks(rotation=45)
plt.show()

#-----------------------------------------------------------
# Phase 4 : Reoporting
#-----------------------------------------------------------

# 결과 리포트 작성 예시 (Markdown으로 작성 가능)
# report = """
# # 고객 리뷰 분석 리포트

# ## 1. 데이터 전처리
# - 결측치: 'review_length'의 결측치는 평균값으로 채워졌습니다.
# - 이상치 탐지: 'review_length'에 대한 IQR 기반 이상치를 탐지하였습니다.

# ## 2. 기술 통계
# - 'review_length'와 'rating'에 대한 기술 통계 분석이 완료되었습니다.
# - 카테고리별 평균 평점과 평점, 감성 점수의 관계가 시각화되었습니다.

# ## 3. AI 분석을 위한 인사이트
# - 높은 감성 점수가 평점에 영향을 미칠 수 있음을 확인하였습니다.
# - 텍스트 길이와 평점 간의 관계를 분석하였으며, 감성 점수 평균 차이를 카테고리별로 확인했습니다.

# ## 4. 결론
# - 텍스트 길이나 감성 점수는 임베딩 분석에 중요한 영향을 미칠 것으로 예상됩니다.
# """

# # 리포트를 파일로 저장
# with open('analysis_report.md', 'w') as f:
#     f.write(report)

# PDF로 저장하려면 fpdf 라이브러리 등을 사용하여 리포트를 PDF로 변환 가능

#------------------------------------------------------
#End of the project
#------------------------------------------------------