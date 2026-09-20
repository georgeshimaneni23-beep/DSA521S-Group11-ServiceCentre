/*
 * DSA521S - Task A4: Daily Statistics (Array)
 *
 * DailyStatistics.java
 * The service times of every student served during the simulated day are kept in
 * a plain int array. The array is grown manually when it becomes full.
 * All six statistics are computed by traversing the array with a loop; no
 * built-in max(), min(), sum() or average helper is used anywhere.
 */
public class DailyStatistics {

    private int[] serviceTimes;
    private int count;   // number of values actually stored

    public DailyStatistics() {
        this(20);
    }

    public DailyStatistics(int capacity) {
        serviceTimes = new int[capacity];
        count = 0;
    }

    /* Record the service time of one student who has just been served. */
    public void recordService(int minutes) {
        if (count == serviceTimes.length) {      // grow the array by hand
            int[] bigger = new int[serviceTimes.length * 2];
            for (int i = 0; i < serviceTimes.length; i++) {
                bigger[i] = serviceTimes[i];
            }
            serviceTimes = bigger;
        }
        serviceTimes[count] = minutes;
        count++;
    }

    public int getCount() { return count; }

    /* A copy of only the filled part of the array. */
    public int[] getServiceTimes() {
        int[] copy = new int[count];
        for (int i = 0; i < count; i++) {
            copy[i] = serviceTimes[i];
        }
        return copy;
    }

    /* ---- 1. total students served ---- */
    public int totalStudentsServed() {
        int total = 0;
        for (int i = 0; i < count; i++) {   // counted by traversal, not by using count directly
            total = total + 1;
        }
        return total;
    }

    /* ---- 2. total service time ---- */
    public int totalServiceTime() {
        int total = 0;
        for (int i = 0; i < count; i++) {
            total = total + serviceTimes[i];
        }
        return total;
    }

    /* ---- 3. average service time ---- */
    public double averageServiceTime() {
        if (count == 0) return 0.0;
        return (double) totalServiceTime() / count;
    }

    /* ---- 4. highest service time ---- */
    public int highestServiceTime() {
        if (count == 0) return 0;
        int highest = serviceTimes[0];
        for (int i = 1; i < count; i++) {
            if (serviceTimes[i] > highest) {
                highest = serviceTimes[i];
            }
        }
        return highest;
    }

    /* ---- 5. lowest service time ---- */
    public int lowestServiceTime() {
        if (count == 0) return 0;
        int lowest = serviceTimes[0];
        for (int i = 1; i < count; i++) {
            if (serviceTimes[i] < lowest) {
                lowest = serviceTimes[i];
            }
        }
        return lowest;
    }

    /* ---- 6. number of services longer than 10 minutes ---- */
    public int countLongerThanTen() {
        int longer = 0;
        for (int i = 0; i < count; i++) {
            if (serviceTimes[i] > 10) {
                longer++;
            }
        }
        return longer;
    }

    /* Print all statistics in the report format. */
    public void displayStatistics() {
        System.out.println("--- DAILY STATISTICS (computed from the service-time array) ---");
        if (count == 0) {
            System.out.println("No students have been served yet, so there are no statistics.");
            return;
        }
        System.out.println("Array contents          : " + ArrayUtil.toText(getServiceTimes()));
        System.out.println("Total students served   : " + totalStudentsServed());
        System.out.println("Total service time      : " + totalServiceTime() + " minutes");
        System.out.printf ("Average service time    : %.2f minutes%n", averageServiceTime());
        System.out.println("Highest service time    : " + highestServiceTime() + " minutes");
        System.out.println("Lowest service time     : " + lowestServiceTime() + " minutes");
        System.out.println("Services over 10 min    : " + countLongerThanTen());
    }
}
