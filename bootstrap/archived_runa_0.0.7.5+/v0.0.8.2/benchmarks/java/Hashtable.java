import java.util.HashMap;

public class Hashtable {
    public static void main(String[] args) {
        HashMap<Integer, Integer> table = new HashMap<>();

        // Insert 10000 key-value pairs
        for (int i = 0; i < 10000; i++) {
            table.put(i, i * 2);
        }

        // Lookup 10000 values
        int total = 0;
        for (int i = 0; i < 10000; i++) {
            if (table.containsKey(i)) {
                int value = table.get(i);
                total += value;
            }
        }

        System.exit(0);
    }
}
