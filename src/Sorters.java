/*
 * DSA521S - PART B: the four sorting algorithms.
 *
 * Sorters.java
 * Selection Sort, Insertion Sort, Merge Sort and Quick Sort, all written from
 * scratch. Each algorithm sorts an int array into ascending order and reports
 * the number of DATA-VALUE comparisons it made (loop-index and boundary tests
 * are deliberately not counted) together with its own movement counter
 * (swaps for Selection/Quick Sort, shifts for Insertion Sort, merge moves for
 * Merge Sort).
 *
 * Every algorithm has two versions:
 *   xxxSort(int[] a)                  - plain version used by the experiment
 *   xxxSortTraced(int[] a)            - prints the trace required by Part B
 */
public class Sorters {

    /* Simple counter object carried through the recursive algorithms. */
    public static class Stats {
        public long comparisons = 0;  // comparisons between two data values
        public long movements = 0;    // swaps / shifts / merge moves
        public long timeNanos = 0;    // measured around the sorting call only
        public String name = "";

        public Stats(String name) { this.name = name; }

        @Override
        public String toString() {
            return String.format("%-15s comparisons=%-10d movements=%-10d time=%d ns",
                    name, comparisons, movements, timeNanos);
        }
    }

    /* ==========================================================
     * B1 - SELECTION SORT
     * Repeatedly finds the smallest value in the unsorted part and
     * swaps it into the next sorted position.
     * Comparisons: O(n^2) always.  Swaps: at most n-1.
     * ========================================================== */
    public static Stats selectionSort(int[] a) {
        Stats st = new Stats("Selection Sort");
        for (int i = 0; i < a.length - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < a.length; j++) {
                st.comparisons++;                 // data comparison
                if (a[j] < a[minIndex]) {
                    minIndex = j;
                }
            }
            if (minIndex != i) {                  // one swap per pass at most
                int temp = a[i];
                a[i] = a[minIndex];
                a[minIndex] = temp;
                st.movements++;
            }
        }
        return st;
    }

    public static Stats selectionSortTraced(int[] a, int passesToShow) {
        Stats st = new Stats("Selection Sort");
        System.out.println("Initial array : " + ArrayUtil.toText(a));
        for (int i = 0; i < a.length - 1; i++) {
            int minIndex = i;
            for (int j = i + 1; j < a.length; j++) {
                st.comparisons++;
                if (a[j] < a[minIndex]) {
                    minIndex = j;
                }
            }
            boolean swapped = false;
            if (minIndex != i) {
                int temp = a[i];
                a[i] = a[minIndex];
                a[minIndex] = temp;
                st.movements++;
                swapped = true;
            }
            if (i < passesToShow) {
                System.out.printf("Pass %d: smallest in unsorted part = %d, %s%n",
                        i + 1, a[i], swapped ? "swapped into index " + i : "already in place");
                System.out.println("        array = " + ArrayUtil.toTextWithBoundary(a, i + 1)
                        + "   (values left of | are sorted)");
                System.out.println("        running totals: comparisons = " + st.comparisons
                        + ", swaps = " + st.movements);
            }
        }
        System.out.println("Sorted array  : " + ArrayUtil.toText(a));
        System.out.println("TOTAL comparisons = " + st.comparisons + ", TOTAL swaps = " + st.movements);
        return st;
    }

    /* ==========================================================
     * B2 - INSERTION SORT
     * Takes the next value and shifts the larger sorted values one place
     * right until the correct position for it is found.
     * Best case O(n) comparisons on sorted data; worst case O(n^2).
     * ========================================================== */
    public static Stats insertionSort(int[] a) {
        Stats st = new Stats("Insertion Sort");
        for (int i = 1; i < a.length; i++) {
            int key = a[i];
            int j = i - 1;
            while (j >= 0) {
                st.comparisons++;                 // data comparison a[j] > key
                if (a[j] > key) {
                    a[j + 1] = a[j];              // shift right
                    st.movements++;
                    j--;
                } else {
                    break;                        // correct position found
                }
            }
            a[j + 1] = key;
        }
        return st;
    }

    public static Stats insertionSortTraced(int[] a, int passesToShow) {
        Stats st = new Stats("Insertion Sort");
        System.out.println("Initial array : " + ArrayUtil.toText(a));
        for (int i = 1; i < a.length; i++) {
            int key = a[i];
            long shiftsBefore = st.movements;
            int j = i - 1;
            while (j >= 0) {
                st.comparisons++;
                if (a[j] > key) {
                    a[j + 1] = a[j];
                    st.movements++;
                    j--;
                } else {
                    break;
                }
            }
            a[j + 1] = key;
            if (i <= passesToShow) {
                System.out.printf("Pass %d: key = %d inserted at index %d (%d shift(s) in this pass)%n",
                        i, key, j + 1, st.movements - shiftsBefore);
                System.out.println("        array = " + ArrayUtil.toTextWithBoundary(a, i + 1)
                        + "   (values left of | are sorted)");
                System.out.println("        running totals: comparisons = " + st.comparisons
                        + ", shifts = " + st.movements);
            }
        }
        System.out.println("Sorted array  : " + ArrayUtil.toText(a));
        System.out.println("TOTAL comparisons = " + st.comparisons + ", TOTAL shifts = " + st.movements);
        return st;
    }

    /* ==========================================================
     * B3 - MERGE SORT
     * Divide the array into halves until each piece holds one element
     * (the BASE CASE: an array of size 0 or 1 is already sorted), then
     * merge the sorted halves back together.
     * O(n log n) comparisons in every case.
     * ========================================================== */
    public static Stats mergeSort(int[] a) {
        Stats st = new Stats("Merge Sort");
        mergeSortRec(a, 0, a.length - 1, st, false, 0);
        return st;
    }

    public static Stats mergeSortTraced(int[] a) {
        Stats st = new Stats("Merge Sort");
        System.out.println("Initial array : " + ArrayUtil.toText(a));
        System.out.println();
        System.out.println("DIVIDE and MERGE trace (indentation shows the recursion depth):");
        mergeSortRec(a, 0, a.length - 1, st, true, 0);
        System.out.println();
        System.out.println("Sorted array  : " + ArrayUtil.toText(a));
        System.out.println("TOTAL comparisons = " + st.comparisons + ", TOTAL merge moves = " + st.movements);
        return st;
    }

    private static void mergeSortRec(int[] a, int low, int high, Stats st, boolean trace, int depth) {
        if (low >= high) {                         // BASE CASE: 0 or 1 element
            if (trace && low == high) {
                System.out.println(pad(depth) + "BASE CASE: [" + a[low] + "] - a single element is already sorted.");
            }
            return;
        }
        int mid = low + (high - low) / 2;
        if (trace) {
            System.out.println(pad(depth) + "DIVIDE " + ArrayUtil.toText(ArrayUtil.copyRange(a, low, high + 1))
                    + " into " + ArrayUtil.toText(ArrayUtil.copyRange(a, low, mid + 1))
                    + " and " + ArrayUtil.toText(ArrayUtil.copyRange(a, mid + 1, high + 1)));
        }
        mergeSortRec(a, low, mid, st, trace, depth + 1);
        mergeSortRec(a, mid + 1, high, st, trace, depth + 1);
        merge(a, low, mid, high, st);
        if (trace) {
            System.out.println(pad(depth) + "MERGE  -> " + ArrayUtil.toText(ArrayUtil.copyRange(a, low, high + 1)));
        }
    }

    private static void merge(int[] a, int low, int mid, int high, Stats st) {
        int[] left = ArrayUtil.copyRange(a, low, mid + 1);
        int[] right = ArrayUtil.copyRange(a, mid + 1, high + 1);
        int i = 0, j = 0, k = low;
        while (i < left.length && j < right.length) {
            st.comparisons++;                      // data comparison
            if (left[i] <= right[j]) {
                a[k] = left[i];
                i++;
            } else {
                a[k] = right[j];
                j++;
            }
            st.movements++;
            k++;
        }
        while (i < left.length) {                  // copy the rest of the left half
            a[k] = left[i];
            i++; k++; st.movements++;
        }
        while (j < right.length) {                 // copy the rest of the right half
            a[k] = right[j];
            j++; k++; st.movements++;
        }
    }

    private static String pad(int depth) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < depth; i++) sb.append("   ");
        return sb.toString();
    }

    /* ==========================================================
     * B4 - QUICK SORT
     * PIVOT-SELECTION RULE: the LAST element of the current sub-array is the
     * pivot (Lomuto partition scheme). Values smaller than or equal to the
     * pivot are moved to the left partition, larger values stay on the right,
     * and the pivot is then placed between the two partitions.
     * Average O(n log n); worst case O(n^2) on already sorted data with this rule.
     * ========================================================== */
    public static Stats quickSort(int[] a) {
        Stats st = new Stats("Quick Sort");
        quickSortRec(a, 0, a.length - 1, st, false, 0, new int[]{0});
        return st;
    }

    public static Stats quickSortTraced(int[] a, int stagesToShow) {
        Stats st = new Stats("Quick Sort");
        System.out.println("Initial array : " + ArrayUtil.toText(a));
        System.out.println("Pivot rule    : the LAST element of the sub-array (Lomuto partitioning).");
        System.out.println();
        quickSortRec(a, 0, a.length - 1, st, true, stagesToShow, new int[]{0});
        System.out.println();
        System.out.println("Sorted array  : " + ArrayUtil.toText(a));
        System.out.println("TOTAL comparisons = " + st.comparisons + ", TOTAL swaps = " + st.movements);
        return st;
    }

    private static void quickSortRec(int[] a, int low, int high, Stats st,
                                     boolean trace, int stagesToShow, int[] stageCounter) {
        if (low >= high) {                          // BASE CASE: 0 or 1 element
            return;
        }
        int pivotValue = a[high];
        boolean showThis = trace && stageCounter[0] < stagesToShow;
        int[] before = showThis ? ArrayUtil.copyRange(a, low, high + 1) : null;

        int pivotIndex = partition(a, low, high, st);

        if (showThis) {
            stageCounter[0]++;
            System.out.println("Partition stage " + stageCounter[0] + "  (sub-array indices " + low + ".." + high + ")");
            System.out.println("  sub-array before : " + ArrayUtil.toText(before));
            System.out.println("  pivot            : " + pivotValue + " (last element)");
            System.out.println("  left partition   : " + ArrayUtil.toText(ArrayUtil.copyRange(a, low, pivotIndex))
                    + "   (values <= pivot)");
            System.out.println("  pivot final pos  : index " + pivotIndex);
            System.out.println("  right partition  : " + ArrayUtil.toText(ArrayUtil.copyRange(a, pivotIndex + 1, high + 1))
                    + "   (values > pivot)");
            System.out.println("  whole array now  : " + ArrayUtil.toText(a));
            System.out.println();
        }

        quickSortRec(a, low, pivotIndex - 1, st, trace, stagesToShow, stageCounter);
        quickSortRec(a, pivotIndex + 1, high, st, trace, stagesToShow, stageCounter);
    }

    private static int partition(int[] a, int low, int high, Stats st) {
        int pivot = a[high];
        int i = low - 1;                            // end of the "smaller than pivot" region
        for (int j = low; j < high; j++) {
            st.comparisons++;                       // data comparison a[j] <= pivot
            if (a[j] <= pivot) {
                i++;
                if (i != j) {
                    int temp = a[i];
                    a[i] = a[j];
                    a[j] = temp;
                    st.movements++;
                }
            }
        }
        int temp = a[i + 1];                        // put the pivot in its final place
        a[i + 1] = a[high];
        a[high] = temp;
        st.movements++;
        return i + 1;
    }
}
