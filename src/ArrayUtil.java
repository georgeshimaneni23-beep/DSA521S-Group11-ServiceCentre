/*
 * DSA521S - small helper used for printing and copying arrays.
 * Only manual loops are used: no Arrays.toString(), Arrays.copyOf() or sort().
 */
public class ArrayUtil {

    /* Manual copy of an int array. */
    public static int[] copy(int[] source) {
        int[] target = new int[source.length];
        for (int i = 0; i < source.length; i++) {
            target[i] = source[i];
        }
        return target;
    }

    /* Manual copy of a sub-range [from, to) of an int array. */
    public static int[] copyRange(int[] source, int from, int to) {
        int[] target = new int[to - from];
        for (int i = from; i < to; i++) {
            target[i - from] = source[i];
        }
        return target;
    }

    /* Renders an array as [a, b, c] using a loop. */
    public static String toText(int[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            sb.append(a[i]);
            if (i < a.length - 1) sb.append(", ");
        }
        sb.append("]");
        return sb.toString();
    }

    /* Renders an array and marks the sorted prefix, used in the sorting traces. */
    public static String toTextWithBoundary(int[] a, int sortedCount) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            sb.append(a[i]);
            if (i < a.length - 1) {
                if (i == sortedCount - 1) {
                    sb.append(" | ");   // boundary between the sorted and unsorted parts
                } else {
                    sb.append(", ");
                }
            }
        }
        sb.append("]");
        return sb.toString();
    }

    /* Verifies ascending order without using a built-in check. */
    public static boolean isSortedAscending(int[] a) {
        for (int i = 1; i < a.length; i++) {
            if (a[i - 1] > a[i]) return false;
        }
        return true;
    }
}
