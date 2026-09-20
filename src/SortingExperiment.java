/*
 * DSA521S - PART C: Algorithm Experiment
 *
 * SortingExperiment.java
 * Compares Selection Sort, Insertion Sort, Merge Sort and Quick Sort on
 * randomly generated arrays of 20, 50, 100 and 500 integers, and on an
 * almost-sorted version of the 100-element array.
 *
 * Fairness rules applied:
 *   - one original array is generated per input size;
 *   - every algorithm receives its own COPY of exactly the same values;
 *   - only data-value comparisons are counted;
 *   - System.nanoTime() is taken immediately before and after the sorting call,
 *     so generation, copying and printing are excluded from the timing.
 *
 * A fixed random seed (2026) is used so that the printed table can be
 * reproduced exactly and matches the table in the project report.
 */
public class SortingExperiment {

    private static final long SEED = 2026L;

    /* Simple linear-congruential generator so the test data is reproducible
       on any machine without relying on a library random class. */
    private static class SimpleRandom {
        private long state;
        SimpleRandom(long seed) { this.state = seed; }
        int nextInt(int bound) {
            state = (state * 6364136223846793005L + 1442695040888963407L);
            long x = (state >>> 17) & 0x7FFFFFFFL;
            return (int) (x % bound);
        }
    }

    /* Generates one array of the requested size with values in 1..999. */
    public static int[] generateArray(int size, SimpleRandom rnd) {
        int[] a = new int[size];
        for (int i = 0; i < size; i++) {
            a[i] = rnd.nextInt(999) + 1;
        }
        return a;
    }

    /* Runs one algorithm on a copy of the given array and times only the sort. */
    private static Sorters.Stats runOne(String algorithm, int[] original) {
        int[] work = ArrayUtil.copy(original);   // copying is done before timing starts
        Sorters.Stats st;
        long start, end;
        switch (algorithm) {
            case "Selection Sort":
                start = System.nanoTime();
                st = Sorters.selectionSort(work);
                end = System.nanoTime();
                break;
            case "Insertion Sort":
                start = System.nanoTime();
                st = Sorters.insertionSort(work);
                end = System.nanoTime();
                break;
            case "Merge Sort":
                start = System.nanoTime();
                st = Sorters.mergeSort(work);
                end = System.nanoTime();
                break;
            default:
                start = System.nanoTime();
                st = Sorters.quickSort(work);
                end = System.nanoTime();
                break;
        }
        st.timeNanos = end - start;
        if (!ArrayUtil.isSortedAscending(work)) {
            System.out.println("WARNING: " + algorithm + " did not sort correctly!");
        }
        return st;
    }

    public static void run() {
        int[] sizes = {20, 50, 100, 500};
        String[] algorithms = {"Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"};
        SimpleRandom rnd = new SimpleRandom(SEED);
        int[] hundredElementArray = null;

        System.out.println("===============================================================");
        System.out.println("  PART C - SORTING ALGORITHM EXPERIMENT");
        System.out.println("===============================================================");
        System.out.println("Random values 1..999, fixed seed " + SEED
                + ". Each algorithm sorts an identical copy of the same array.");
        System.out.println();
        System.out.printf("%-16s %-11s %-22s %s%n", "Algorithm", "Input Size", "Number of Comparisons", "Execution Time (ns)");
        System.out.println("---------------------------------------------------------------------------");

        for (int s = 0; s < sizes.length; s++) {
            int size = sizes[s];
            int[] original = generateArray(size, rnd);
            if (size == 100) {
                hundredElementArray = ArrayUtil.copy(original);
            }
            for (String algorithm : algorithms) {
                Sorters.Stats st = runOne(algorithm, original);
                System.out.printf("%-16s %-11d %-22d %d%n", algorithm, size, st.comparisons, st.timeNanos);
            }
            System.out.println("---------------------------------------------------------------------------");
        }

        /* ---------------- almost-sorted test ---------------- */
        System.out.println();
        System.out.println("ADDITIONAL TEST - ALMOST-SORTED 100-ELEMENT ARRAY");
        System.out.println("The 100-element array is first sorted ascending, then five pairs of");
        System.out.println("neighbouring values are swapped. All four algorithms receive the same array.");
        System.out.println();

        int[] almostSorted = ArrayUtil.copy(hundredElementArray);
        Sorters.insertionSort(almostSorted);              // fully sort it first
        int[] swapPositions = {10, 25, 40, 60, 80};       // swap a[p] with a[p+1]
        for (int p : swapPositions) {
            int temp = almostSorted[p];
            almostSorted[p] = almostSorted[p + 1];
            almostSorted[p + 1] = temp;
        }
        System.out.println("Five neighbouring pairs swapped at indices 10/11, 25/26, 40/41, 60/61, 80/81.");
        System.out.println();
        System.out.printf("%-16s %-11s %-22s %s%n", "Algorithm", "Input Size", "Number of Comparisons", "Execution Time (ns)");
        System.out.println("---------------------------------------------------------------------------");
        for (String algorithm : algorithms) {
            Sorters.Stats st = runOne(algorithm, almostSorted);
            System.out.printf("%-16s %-11s %-22d %d%n", algorithm, "100 (almost)", st.comparisons, st.timeNanos);
        }
        System.out.println("---------------------------------------------------------------------------");
        System.out.println();
        System.out.println("Note: measured times on the first run of a Java program are affected by");
        System.out.println("JIT warm-up, so the comparison counts are the more reliable measure.");
        System.out.println();
    }

    public static void main(String[] args) {
        run();
    }
}
