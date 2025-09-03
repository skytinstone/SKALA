import java.util.List;
import java.util.function.Function;

/** Minimal Unicode table renderer */
public final class TableUtil {
    private static final String H = "─";
    private static final String V = "│";
    private static final String TL = "┌";
    private static final String TR = "┐";
    private static final String BL = "└";
    private static final String BR = "┘";
    private static final String TJ = "┬";
    private static final String MJ = "┼";
    private static final String BJ = "┴";

    private TableUtil() {}

    public static String render(String[] headers, List<String[]> rows) {
        int cols = headers.length;
        int[] widths = new int[cols];
        for (int c = 0; c < cols; c++) {
            widths[c] = Math.max(widths[c], displayLen(headers[c]));
        }
        for (String[] row : rows) {
            for (int c = 0; c < cols; c++) {
                widths[c] = Math.max(widths[c], displayLen(row[c]));
            }
        }

        StringBuilder sb = new StringBuilder();
        // top border
        sb.append(TL);
        for (int c = 0; c < cols; c++) {
            sb.append(H.repeat(widths[c] + 2));
            sb.append(c == cols - 1 ? TR : TJ);
        }
        sb.append("\n");

        // headers
        sb.append(V);
        for (int c = 0; c < cols; c++) {
            sb.append(" ").append(pad(headers[c], widths[c])).append(" ").append(V);
        }
        sb.append("\n");

        // mid border
        sb.append(BL.replace("└","├"));
        for (int c = 0; c < cols; c++) {
            sb.append(H.repeat(widths[c] + 2));
            sb.append(c == cols - 1 ? BR.replace("┘","┤") : MJ);
        }
        sb.append("\n");

        // rows
        for (String[] row : rows) {
            sb.append(V);
            for (int c = 0; c < cols; c++) {
                sb.append(" ").append(pad(row[c], widths[c])).append(" ").append(V);
            }
            sb.append("\n");
        }

        // bottom
        sb.append(BL);
        for (int c = 0; c < cols; c++) {
            sb.append(H.repeat(widths[c] + 2));
            sb.append(c == cols - 1 ? BR : BJ);
        }
        return sb.toString();
    }

    private static int displayLen(String s) {
        return s == null ? 0 : s.replaceAll("\u001B\\[[;\\d]*m","").length();
    }

    private static String pad(String s, int width) {
        if (s == null) s = "";
        int pad = width - displayLen(s);
        if (pad <= 0) return s;
        return s + " ".repeat(pad);
    }

    /** simple inline bar (▮) scaled to max */
    public static String bar(int value, int max) {
        if (max <= 0) return "";
        int count = Math.max(0, Math.round((float)value / (float)max * 10));
        return "▮".repeat(Math.max(1, count));
    }
}
