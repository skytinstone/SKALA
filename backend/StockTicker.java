// StockTicker.java
// 실행: javac StockTicker.java && java StockTicker
// 과정 : SKALA 2기 
// 작성자 : 신민석
// 반 : 1
// 번호 : 15
// -----------------------------------------------
public class StockTicker {

    // ====== 공통 주식 추상화 ======
    static abstract class Stock {
        private final String name;          // 종목명 (캡슐화)
        private int price;                  // 현재가 (원)
        private final boolean votingRight;  // 의결권
        private final boolean dividendPref; // 배당우선권

        protected Stock(String name, int price, boolean votingRight, boolean dividendPref) {
            this.name = name;
            setPrice(price);
            this.votingRight = votingRight;
            this.dividendPref = dividendPref;
        }

        public String getName() { return name; }
        public int getPrice() { return price; }
        public boolean hasVotingRight() { return votingRight; }
        public boolean hasDividendPref() { return dividendPref; }

        public final void setPrice(int price) {
            if (price <= 0) throw new IllegalArgumentException("price must be > 0");
            this.price = price;
        }

        public abstract String label();     // [일반주], [우선주] 등
        protected String votingText() { return votingRight ? "있음" : "없음"; }
        protected String divPrefText() { return dividendPref ? "있음" : "없음"; }

        // 공통 포맷 (하위에서 필요한 정보 추가)
        public String baseInfo() {
            return label() + " 종목: " + name +
                   " / 현재가: " + price + "원";
        }

        public abstract String infoLine();  // 한 줄 출력 문자열
    }

    // ====== 일반주 ======
    static class CommonStock extends Stock {
        public CommonStock(String name, int price) {
            super(name, price, true, false);
        }
        @Override public String label() { return "[일반주]"; }

        @Override
        public String infoLine() {
            return baseInfo() +
                   " / 의결권: " + votingText() +
                   " / 배당우선권: " + divPrefText();
        }
    }

    // ====== 우선주 ======
    static class PreferredStock extends Stock {
        private final double dividendRate; // 배당률(%)
        public PreferredStock(String name, int price, double dividendRate) {
            super(name, price, false, true);
            this.dividendRate = dividendRate;
        }
        @Override public String label() { return "[우선주]"; }

        @Override
        public String infoLine() {
            return baseInfo() +
                   " / 배당률: " + String.format("%.1f%%", dividendRate) +
                   " / 의결권: " + votingText() +
                   " / 배당우선권: " + divPrefText();
        }
    }

    // ====== 실행 ======
    public static void main(String[] args) {
        CommonStock edu = new CommonStock("스칼라 에듀", 15000);
        PreferredStock ai = new PreferredStock("스칼라 AI", 17500, 5.0);

        // 초기 정보
        System.out.println(edu.infoLine());
        System.out.println(ai.infoLine());

        // 가격 변경 안내
        edu.setPrice(15800);
        System.out.println("스칼라 에듀 가격이 15800원으로 변경되었습니다.");

        ai.setPrice(18000);
        System.out.println("스칼라 AI 가격이 18000원으로 변경되었습니다.");

        System.out.println();
        System.out.println("[가격 변경 후 정보]");
        System.out.println(edu.infoLine());
        System.out.println(ai.infoLine());
    }
}
