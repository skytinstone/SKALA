# SKALA Stock Console — Fancy Edition

이 버전은 **ANSI 컬러**, **ASCII 배너**, **유니코드 표**(테이블), **미니 바 차트**를 추가해
콘솔에서 더 보기 좋게 만든 에디션입니다. 외부 라이브러리 없이 동작합니다.

## 추가된 파일
- `src/ConsoleColors.java` : ANSI 컬러 유틸
- `src/AsciiBanner.java` : 시작 배너
- `src/TableUtil.java` : 유니코드 테이블/미니바 렌더러
- `src/StockView.java` : 컬러/표/배너 적용 (패치)
- `src/SkalaStockMarket.java` : 시작 시 배너 호출, 에러 출력 개선 (패치)

## 빠른 실행 방법 (javac/java, 표준 JDK)
아래 명령은 프로젝트 루트(이 파일이 있는 폴더 상위)의 `skala-stock-console-main`에서 실행한다고 가정합니다.

```bash
# 1) 소스 컴파일
cd skala-stock-console-main
javac -encoding UTF-8 -d out src/*.java

# 2) 실행
cd out
java App
```

> **Tip**: Windows라면 PowerShell/Windows Terminal에서 실행하면 ANSI 컬러가 잘 보입니다.
> IntelliJ/VS Code에서 프로젝트로 열어 실행해도 됩니다.

## 사용법
- 실행 후 **메인 메뉴**에서 번호를 입력합니다.
- `주식 목록 보기` → 번호로 종목 선택 후 수량을 입력해 구매
- `보유 포트폴리오` → 보유 종목, 수량, 평가금액을 테이블로 확인
- `저장 및 종료` → 현재 상태를 저장하고 종료

## 스타일 미리보기
- 시작 시 `SKALA · Stock Console` ASCII 배너 표시
- 목록/포트폴리오를 유니코드 프레임(┌ ┬ ┐ …) 테이블로 출력
- 수량/비중은 `▮` 막대로 직관적으로 확인 가능
- 메시지는 `✔`(성공), `✘`(오류) 아이콘으로 가독성 향상

---

### 문제 해결(트러블슈팅)
- **문자가 깨져요**: `javac -encoding UTF-8` 옵션을 꼭 넣고, 터미널의 글꼴을 유니코드 지원 폰트로 설정하세요.
- **컬러가 안보여요**: 터미널이 ANSI 컬러를 지원하는지 확인하세요. (Windows cmd 기본창은 제한이 있을 수 있음)
- **실행이 안 돼요**: `out` 디렉터리에 `.class`가 생성되었는지, `java App`을 `out` 폴더에서 실행했는지 확인하세요.
