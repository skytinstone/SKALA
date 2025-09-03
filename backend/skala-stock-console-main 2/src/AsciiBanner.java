import static java.lang.System.out;

/** Renders an ASCII banner for the app */
public final class AsciiBanner {
    private AsciiBanner() {}

    public static void show() {
        String cyan = ConsoleColors.CYAN;
        String bold = ConsoleColors.BOLD;
        String reset = ConsoleColors.RESET;
        out.println();
        out.println(cyan + bold +
            "  ██████  ██   ██  █████  ██      █████  " + reset);
        out.println(cyan + bold +
            "  ██   ██ ██   ██ ██   ██ ██     ██   ██ " + reset);
        out.println(cyan + bold +
            "  ██████  ███████ ███████ ██     ███████ " + reset);
        out.println(cyan + bold +
            "  ██      ██   ██ ██   ██ ██     ██   ██ " + reset);
        out.println(cyan + bold +
            "  ██      ██   ██ ██   ██ ██████ ██   ██ " + reset);
        out.println(ConsoleColors.DIM + "         SKALA · Stock Console" + reset);
        out.println();
    }
}
