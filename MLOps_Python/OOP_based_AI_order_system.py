# OOP_based_AI_order_system.py
# 작성자 : 신민석
# 작성일 : 2025.08.13(수)
# 팀 : SKALA,SK AX AI Leader Academy 2nd
# 반 : 1반
# 번호 : 15번
# 과제명: 객체지향 프로그래밍 기반의 AI 주문 시스템 구현
# ------------------------------------------------------------
# 목적: 객체지향 프로그래밍(OOP) 기반의 AI 주문 시스템 구현
# 구조:
#   - MenuItem: 메뉴 아이템의 기본 클래스
#   - Beverage: 음료 아이템 클래스 (MenuItem 상속)
#   - Dessert: 디저트 아이템 클래스 (MenuItem 상속)
#   - Order: 주문 클래스 (메뉴 아이템 추가, 총 금액 계산,
#             추천 음료 제공 기능 포함)
#   - menu: 메뉴 아이템 목록 (Beverage와 Dessert 인스턴스들로 구성)
#   - order: Order 인스턴스 생성 후 메뉴 아이템 추가
#   - 추천 음료: 최근 주문된 음료의 태그를 기반으로 추천
#   - 총 주문 금액 출력 기능 포함
# 동작:
#   - 주문을 추가하고 총 금액을 계산
#   - 최근 주문된 음료의 태그를 기반으로 추천 음료 제공
# ------------------------------------------------------------

# 필요한 모듈 임포트(random 모듈)
import random

# 메뉴 아이템 클래스 정의
class MenuItem:
    def __init__(self, name, price, tags):  # 초기화 메서드
        self.name = name    # 메뉴 이름
        self.price = price  # 메뉴 가격
        self.tags = tags    # 메뉴 태그

# 음료 아이템 클래스 정의 (MenuItem 상속)
class Beverage(MenuItem):
    pass  # Beverage는 MenuItem을 그대로 상속받기만 함

# 디저트 아이템 클래스 정의 (MenuItem 상속)
class Dessert(MenuItem):
    pass  # Dessert도 MenuItem을 그대로 상속받기만 함

# 주문 클래스 정의!
class Order:
    def __init__(self):  # 초기화 메서드 -> 주문 초기화
        self.items = []
        self.total_price = 0

    def add_item(self, item):  # 주문에 메뉴 아이템 추가 메서드
        self.items.append(item)
        self.total_price += item.price

    def recommend_drinks(self):  # 최근 주문된 음료 기반 추천 음료 제공
        recent_tags = [tag for item in self.items if isinstance(item, Beverage) for tag in item.tags]
        return [item for item in menu if isinstance(item, Beverage) and any(tag in recent_tags for tag in item.tags)]

    def display_total(self):  # 총 금액 출력
        print("=" * 60)
        print(f"총 주문 금액: {self.total_price}원")

# 메뉴 아이템 목록 list
menu = [
    Beverage("아이스 아메리카노", 1700, ["커피", "시원한"]),
    Beverage("핫 아메리카노", 1600, ["커피", "시원한"]),
    Beverage("녹차", 2000, ["차", "따뜻한"]),
    Beverage("말차", 3500, ["차", "따뜻한"]),
    Beverage("허브티", 3000, ["차", "따뜻한"]),
    Dessert("크로와상", 3300, ["빵"]),
    Dessert("파니니", 4500, ["샌드위치"]),
    Dessert("BLT", 5600, ["샌드위치", ""])
]

# 주문 객체 생성
order = Order()

# 음료 추천
recommended_beverage = random.choice([item for item in menu if isinstance(item, Beverage)])  # 음료 랜덤 추천
order.add_item(recommended_beverage)  # 음료 주문 추가
print("=" * 60) # 구분선
print(f"추천 음료: {recommended_beverage.name} - {recommended_beverage.price}원") # 추천 음료 출력

# 음식 주문 여부 묻기
order_more = input("음식을 주문하시겠습니까? (y/n): ").strip().lower()

if order_more == "y": # 음식 주문을 진행
    # 디저트 랜덤 추천
    recommended_dessert = random.choice([item for item in menu if isinstance(item, Dessert)])  # 디저트 랜덤 추천
    order.add_item(recommended_dessert)  # 디저트 주문 추가
    print("=" * 60) # 구분선
    print(f"추천 디저트: {recommended_dessert.name} - {recommended_dessert.price}원") # 추천 디저트 출력
    
    # 총 합산 금액 출력
    order.display_total()

    # 결제 안내
    print("=" * 60)
    print("결제를 진행하겠습니다...")
    print("키오스크에 카드를 삽입해 주세요.")
else:
    # 음식을 주문하지 않았을 때
    order.display_total() # 총 금액 출력
    print("=" * 60)
    print("결제를 진행하겠습니다...")
    print("키오스크에 카드를 삽입해 주세요.")
# 프로그램 종료 안내    
print("결제가 완료되었습니다. 좋은하루 되세요!")
print("=" * 60)