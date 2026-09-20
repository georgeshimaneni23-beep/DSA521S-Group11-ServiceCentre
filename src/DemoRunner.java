/*
 * DSA521S - DemoRunner.java
 *
 * Runs every demonstration required by Parts A, B and C in one go, without
 * needing keyboard input. The printed output is what is used as the evidence
 * and the traces in the project report.
 *
 * Run:  java DemoRunner        (or:  java ServiceCentreApp --demo)
 */
public class DemoRunner {

    private static void banner(String title) {
        System.out.println();
        System.out.println("===============================================================");
        System.out.println("  " + title);
        System.out.println("===============================================================");
    }

    public static void runAll() {
        taskA1();
        taskA2();
        PostfixEvaluator.demo();
        taskA4();
        taskA5();
        partB();
        SortingExperiment.run();
        System.out.println("=== END OF DEMONSTRATION RUN ===");
    }

    /* ---------------- TASK A1: Queue ---------------- */
    private static void taskA1() {
        banner("TASK A1 - WAITING LINE (QUEUE)");
        StudentQueue q = new StudentQueue();
        Student[] arrivals = {
            new Student("221045678", "Maria",   "Registration",     12),
            new Student("222034512", "Tomas",   "Student Card",      5),
            new Student("223041876", "Ndapewa", "Fees",              8),
            new Student("221067341", "Simon",   "Documents",         4),
            new Student("224011290", "Johanna", "Academic Enquiry",  9),
            new Student("223098455", "Petrus",  "Document Collect", 15)
        };

        System.out.println("SIX ARRIVALS (enqueue):");
        for (int i = 0; i < arrivals.length; i++) {
            q.enqueue(arrivals[i]);
            System.out.println("  arrival " + (i + 1) + ": enqueue(" + arrivals[i].shortLabel() + ")");
        }
        System.out.println();
        System.out.println("isEmpty() = " + q.isEmpty());
        System.out.println("peek()    = " + q.peek().shortLabel() + "  (first to be served)");
        System.out.println();
        q.displayQueue();
        System.out.println();
        System.out.println("Queue diagram after 6 arrivals:");
        System.out.println("  " + q.diagram());

        System.out.println();
        System.out.println("THREE STUDENTS SERVED (dequeue):");
        for (int i = 1; i <= 3; i++) {
            Student served = q.dequeue();
            System.out.println("  service " + i + ": dequeue() removed " + served.shortLabel()
                    + " - " + served.getServiceType() + " (" + served.getEstimatedServiceTime() + " min)");
            System.out.println("            queue now: " + q.diagram());
        }
        System.out.println();
        q.displayQueue();
        System.out.println();
        System.out.println("isEmpty() = " + q.isEmpty() + ", peek() = " + q.peek().shortLabel());
        System.out.println();
        System.out.println("WHY A QUEUE: students must be assisted in arrival order. A queue is");
        System.out.println("first-in-first-out, so the student who has waited longest is always at the");
        System.out.println("front and is served next. enqueue() and dequeue() are both O(1).");
    }

    /* ---------------- TASK A2: Singly Linked List ---------------- */
    private static void taskA2() {
        banner("TASK A2 - STUDENT SERVICE RECORDS (SINGLY LINKED LIST)");
        ServiceRecordList list = new ServiceRecordList();

        Student maria   = new Student("221045678", "Maria",   "Registration", 12);
        Student tomas   = new Student("222034512", "Tomas",   "Student Card",  5);
        Student ndapewa = new Student("223041876", "Ndapewa", "Fees",          8);
        Student simon   = new Student("221067341", "Simon",   "Documents",     4);
        Student johanna = new Student("224011290", "Johanna", "Academic Enq.", 9);

        System.out.println("1) insertStudent at the END (building the list):");
        list.insertAtEnd(maria);   System.out.println("   after insertAtEnd(Maria)   : " + list.diagram());
        list.insertAtEnd(tomas);   System.out.println("   after insertAtEnd(Tomas)   : " + list.diagram());
        list.insertAtEnd(ndapewa); System.out.println("   after insertAtEnd(Ndapewa) : " + list.diagram());

        System.out.println();
        System.out.println("2) insertStudent at the BEGINNING");
        System.out.println("   LIST BEFORE : " + list.diagram());
        list.insertAtBeginning(simon);
        System.out.println("   LIST AFTER  : " + list.diagram());
        System.out.println("   Link change : new node Simon.next now points to the old head (Maria),");
        System.out.println("                 and head now points to Simon.");

        System.out.println();
        System.out.println("3) insertStudent at a SPECIFIED POSITION (position 3)");
        System.out.println("   LIST BEFORE : " + list.diagram());
        list.insertAtPosition(johanna, 3);
        System.out.println("   LIST AFTER  : " + list.diagram());
        System.out.println("   Link change : node 2 (Maria).next now points to Johanna, and");
        System.out.println("                 Johanna.next points to the node that followed Maria (Tomas).");

        System.out.println();
        System.out.println("4) displayStudents() - full traversal");
        list.displayStudents();

        System.out.println();
        System.out.println("5) searchStudent() - linear search");
        System.out.print("   searchStudent(\"223041876\") : ");
        Student found = list.searchStudent("223041876");
        System.out.println("   -> " + (found == null ? "not found" : found.toString()));
        System.out.print("   searchStudent(\"999999999\") : ");
        list.searchStudent("999999999");

        System.out.println();
        System.out.println("6) deleteStudent() - deleting Tomas (222034512)");
        System.out.println("   LIST BEFORE : " + list.diagram());
        list.deleteStudent("222034512");
        System.out.println("   LIST AFTER  : " + list.diagram());
        System.out.println("   Link change : the predecessor node now points past the deleted node,");
        System.out.println("                 so Tomas is no longer reachable from the head.");

        System.out.println();
        list.displayStudents();
    }

    /* ---------------- TASK A4: Array statistics ---------------- */
    private static void taskA4() {
        banner("TASK A4 - DAILY STATISTICS (ARRAY)");
        DailyStatistics stats = new DailyStatistics();
        int[] servedTimes = {12, 5, 8, 4, 9, 15, 3, 11};
        System.out.println("Service times of the students served during the simulated day are");
        System.out.println("appended to the array one by one as each student is served:");
        for (int t : servedTimes) {
            stats.recordService(t);
            System.out.println("   recordService(" + t + ") -> array = " + ArrayUtil.toText(stats.getServiceTimes()));
        }
        System.out.println();
        stats.displayStatistics();
        System.out.println();
        System.out.println("All six values are obtained by traversing the array with loops.");
        System.out.println("No built-in max(), min(), sum() or average helper is used.");
    }

    /* ---------------- TASK A5: Justification ---------------- */
    private static void taskA5() {
        banner("TASK A5 - DATA-STRUCTURE JUSTIFICATION");
        System.out.println("QUEUE (waiting line)");
        System.out.println("  Students must be helped in the order they arrived. A queue removes only");
        System.out.println("  from the front and adds only at the rear, so the arrival order is enforced");
        System.out.println("  by the structure itself and cannot be broken by mistake. Both operations");
        System.out.println("  are O(1), so a busy queue never slows the program down.");
        System.out.println();
        System.out.println("SINGLY LINKED LIST (service records)");
        System.out.println("  The number of records for a day is not known in advance and records are");
        System.out.println("  inserted and removed in the middle. A linked list grows one node at a time");
        System.out.println("  and a deletion only requires re-pointing one next reference - O(1) once the");
        System.out.println("  node is located - whereas an array would need every later element shifted.");
        System.out.println();
        System.out.println("STACK (postfix evaluation)");
        System.out.println("  In a postfix expression, the operands an operator needs are always the two");
        System.out.println("  most recently produced values. That is exactly last-in-first-out behaviour,");
        System.out.println("  so push() and pop() give the right operands automatically with no searching.");
        System.out.println();
        System.out.println("ARRAY (daily statistics)");
        System.out.println("  The statistics pass over a fixed set of completed service times and never");
        System.out.println("  insert in the middle. An array stores the values contiguously with O(1)");
        System.out.println("  index access, which makes a single traversal for total, average, highest,");
        System.out.println("  lowest and the over-10-minute count both simple and cache-friendly. It is");
        System.out.println("  also the natural input form for the sorting algorithms in Part B.");
    }

    /* ---------------- PART B: four sorting algorithms ---------------- */
    private static void partB() {
        int[] base = {17, 5, 23, 8, 14, 3, 11, 20, 6, 9};

        banner("TASK B1 - SELECTION SORT");
        Sorters.selectionSortTraced(ArrayUtil.copy(base), 3);

        banner("TASK B2 - INSERTION SORT");
        Sorters.insertionSortTraced(ArrayUtil.copy(base), 3);

        banner("TASK B3 - MERGE SORT");
        Sorters.mergeSortTraced(ArrayUtil.copy(base));

        banner("TASK B4 - QUICK SORT");
        Sorters.quickSortTraced(ArrayUtil.copy(base), 2);
    }

    public static void main(String[] args) {
        runAll();
    }
}
