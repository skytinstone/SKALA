import java.nio.charset.StandardCharsets;
import java.util.List;

import static java.lang.System.out;

public class StockView {

    public void showBanner() {
        AsciiBanner.show();
    }

    public void showMenu() {
        out.println(ConsoleColors.BOLD + ConsoleColors.BLUE + "메인 메뉴" + ConsoleColors.RESET);
        out.println("  1) 주식 목록 보기");
        out.println("  2) 주식 구매");
        out.println("  3) 보유 포트폴리오");
        out.println("  4) 저장 및 종료");
        out.println();
        out.print(ConsoleColors.DIM + "선택 번호를 입력하세요 ▶ " + ConsoleColors.RESET);
    }

    public void showMessage(String message) {
        out.println(ConsoleColors.GREEN + "✔ " + ConsoleColors.RESET + message);
    }

    public void showError(String message) {
        out.println(ConsoleColors.RED + "✘ " + ConsoleColors.RESET + message);
    }

    public void showStocks(List<Stock> stockList) {
        String[] headers = {"#", "종목", "가격", "수량", "미니바"};
        java.util.ArrayList<String[]> rows = new java.util.ArrayList<>();
        int maxQty = 1;
        for (Stock s : stockList) maxQty = Math.max(maxQty, s.getQuantity());

        for (int i = 0; i < stockList.size(); i++) {
            Stock stock = stockList.get(i);
            rows.add(new String[]{
                    String.valueOf(i + 1),
                    ConsoleColors.BOLD + stock.getName() + ConsoleColors.RESET,
                    String.valueOf(stock.getPrice()),
                    String.valueOf(stock.getQuantity()),
                    TableUtil.bar(stock.getQuantity(), maxQty)
            });
        }
        out.println(TableUtil.render(headers, rows));
    }

    public void showPortfolio(Portfolio portfolio) {
        String[] headers = {"종목", "보유수량", "평가금액"};
        java.util.ArrayList<String[]> rows = new java.util.ArrayList<>();
        int maxQty = 1;
        for (Stock s : portfolio.getAllStocks()) maxQty = Math.max(maxQty, s.getQuantity());
        int total = 0;
        for (Stock s : portfolio.getAllStocks()) {
            int value = s.getPrice() * s.getQuantity();
            total += value;
            rows.add(new String[]{
                    ConsoleColors.CYAN + s.getName() + ConsoleColors.RESET,
                    String.valueOf(s.getQuantity()),
                    value + " (" + TableUtil.bar(s.getQuantity(), maxQty) + ")"
            });
        }
        out.println(TableUtil.render(headers, rows));
        out.println(ConsoleColors.BOLD + "총 평가금액: " + total + ConsoleColors.RESET);
    }
}
