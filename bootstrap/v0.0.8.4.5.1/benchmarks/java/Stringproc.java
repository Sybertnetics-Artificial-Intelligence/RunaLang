public class Stringproc {
    static int stringLength(String str) {
        return str.length();
    }

    static String copyString(String src) {
        return new String(src);
    }

    public static void main(String[] args) {
        int iterations = 10000;
        String baseStr = "Hello";
        int totalLen = 0;

        for (int i = 0; i < iterations; i++) {
            String resultStr = copyString(baseStr);
            int len = stringLength(resultStr);
            totalLen += len;
        }

        System.exit(0);
    }
}
