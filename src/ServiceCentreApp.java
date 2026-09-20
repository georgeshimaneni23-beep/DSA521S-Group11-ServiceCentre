/*
 * DSA521S - PART D: Integrated Service-Centre System
 *
 * ServiceCentreApp.java
 * Main program. The Queue (Task A1), the Singly Linked List (Task A2), the
 * Array statistics (Task A4) and the four sorting algorithms (Part B) all
 * operate inside this one menu-driven program.
 * The postfix Stack exercise (Task A3) stays a separate exercise and is run
 * from PostfixEvaluator / DemoRunner.
 *
 * Run:  java ServiceCentreApp            -> interactive menu
 *       java ServiceCentreApp --demo     -> runs every Part A-C demonstration
 */
import java.util.Scanner;

public class ServiceCentreApp {

    private StudentQueue waitingQueue = new StudentQueue();
    private ServiceRecordList records = new ServiceRecordList();
    private DailyStatistics statistics = new DailyStatistics();
    private Scanner in = new Scanner(System.in);

    public static void main(String[] args) {
        if (args.length > 0 && (args[0].equals("--demo") || args[0].equals("-d"))) {
            DemoRunner.runAll();
            return;
        }
        ServiceCentreApp app = new ServiceCentreApp();
        app.loadSampleData();
        app.menuLoop();
    }

    /* The four students from the project brief are loaded so the program is
       immediately usable; more can be added from the menu. */
    private void loadSampleData() {
        Student[] sample = {
            new Student("221045678", "Maria",   "Registration", 12),
            new Student("222034512", "Tomas",   "Student Card",  5),
            new Student("223041876", "Ndapewa", "Fees",          8),
            new Student("221067341", "Simon",   "Documents",     4)
        };
        for (Student s : sample) {
            waitingQueue.enqueue(s);
            records.insertAtEnd(s);
        }
    }

    private void printMenu() {
        System.out.println();
        System.out.println("========================================");
        System.out.println("        CAMPUS SERVICE CENTRE");
        System.out.println("========================================");
        System.out.println(" 1. Add student to waiting queue");
        System.out.println(" 2. Serve next student (remove from queue)");
        System.out.println(" 3. Display waiting students");
        System.out.println(" 4. Add student service record (Linked List - insertStudent())");
        System.out.println(" 5. Display student service records");
        System.out.println(" 6. Search for student record");
        System.out.println(" 7. Remove student record");
        System.out.println(" 8. Display daily statistics");
        System.out.println(" 9. Sort service times");
        System.out.println("10. Run sorting experiment");
        System.out.println("11. Exit");
        System.out.println("========================================");
        System.out.print("Select option: ");
    }

    private void menuLoop() {
        boolean running = true;
        while (running) {
            printMenu();
            String choice = in.hasNextLine() ? in.nextLine().trim() : "11";
            System.out.println();
            switch (choice) {
                case "1":  optionAddToQueue();       break;
                case "2":  optionServeNext();        break;
                case "3":  waitingQueue.displayQueue();
                           System.out.println("Queue diagram: " + waitingQueue.diagram());
                           break;
                case "4":  optionAddRecord();        break;
                case "5":  records.displayStudents();
                           System.out.println("List diagram: " + records.diagram());
                           break;
                case "6":  optionSearchRecord();     break;
                case "7":  optionRemoveRecord();     break;
                case "8":  statistics.displayStatistics(); break;
                case "9":  optionSortServiceTimes(); break;
                case "10": SortingExperiment.run();  break;
                case "11": System.out.println("Closing the Campus Service Centre. Goodbye.");
                           running = false;          break;
                default:   System.out.println("Invalid option. Please enter a number from 1 to 11.");
            }
        }
    }

    /* ---- Option 1: Queue - enqueue ---- */
    private void optionAddToQueue() {
        Student s = readStudent();
        if (s == null) return;
        waitingQueue.enqueue(s);
        System.out.println(s.getName() + " joined the queue at position " + waitingQueue.size() + ".");
        System.out.println("Queue diagram: " + waitingQueue.diagram());
    }

    /* ---- Option 2: Queue - dequeue ---- */
    private void optionServeNext() {
        if (waitingQueue.isEmpty()) {
            System.out.println("No students are waiting.");
            return;
        }
        System.out.println("Next in line (peek): " + waitingQueue.peek().shortLabel());
        Student served = waitingQueue.dequeue();
        statistics.recordService(served.getEstimatedServiceTime());   // stored in the Array
        System.out.println("Now serving: " + served);
        System.out.println("Service time recorded in the daily statistics array.");
        System.out.println("Queue diagram: " + waitingQueue.diagram());
    }

    /* ---- Option 4: Linked List - insertStudent ---- */
    private void optionAddRecord() {
        Student s = readStudent();
        if (s == null) return;
        System.out.println("Insert where?  1 = beginning   2 = end   3 = at a position");
        System.out.print("Choice: ");
        String mode = in.nextLine().trim();
        if (mode.equals("1")) {
            records.insertAtBeginning(s);
        } else if (mode.equals("3")) {
            System.out.print("Position (1 to " + (records.size() + 1) + "): ");
            int pos = readInt();
            records.insertAtPosition(s, pos);
        } else {
            records.insertAtEnd(s);
        }
        System.out.println("Record added. List diagram: " + records.diagram());
    }

    /* ---- Option 6: Linked List - search ---- */
    private void optionSearchRecord() {
        System.out.print("Enter the student number to search for: ");
        String no = in.nextLine().trim();
        Student found = records.searchStudent(no);
        if (found != null) {
            System.out.println(Student.tableHeader());
            System.out.println(found);
        }
    }

    /* ---- Option 7: Linked List - delete ---- */
    private void optionRemoveRecord() {
        System.out.print("Enter the student number to remove: ");
        String no = in.nextLine().trim();
        System.out.println("List before deletion: " + records.diagram());
        if (records.deleteStudent(no)) {
            System.out.println("Record " + no + " removed.");
        }
        System.out.println("List after deletion : " + records.diagram());
    }

    /* ---- Option 9: sorting the service times of the records ---- */
    private void optionSortServiceTimes() {
        int[] times = records.serviceTimesAsArray();
        if (times.length < 2) {
            System.out.println("At least two service records are needed before sorting.");
            return;
        }
        System.out.println("Service times taken from the linked list: " + ArrayUtil.toText(times));
        System.out.println("Choose an algorithm: 1 = Selection  2 = Insertion  3 = Merge  4 = Quick");
        System.out.print("Choice: ");
        String c = in.nextLine().trim();
        int[] work = ArrayUtil.copy(times);
        Sorters.Stats st;
        long start = System.nanoTime();
        switch (c) {
            case "1": st = Sorters.selectionSort(work); break;
            case "2": st = Sorters.insertionSort(work); break;
            case "3": st = Sorters.mergeSort(work);     break;
            default:  st = Sorters.quickSort(work);     break;
        }
        long end = System.nanoTime();
        st.timeNanos = end - start;
        System.out.println("Sorted ascending: " + ArrayUtil.toText(work));
        System.out.println(st);
    }

    /* ---- input helpers ---- */
    private Student readStudent() {
        System.out.print("Student number: ");
        String no = in.nextLine().trim();
        if (no.isEmpty()) { System.out.println("Cancelled: a student number is required."); return null; }
        System.out.print("Name          : ");
        String name = in.nextLine().trim();
        System.out.print("Service type  : ");
        String type = in.nextLine().trim();
        System.out.print("Estimated service time (minutes): ");
        int minutes = readInt();
        if (minutes < 0) { System.out.println("Cancelled: invalid service time."); return null; }
        return new Student(no, name, type, minutes);
    }

    private int readInt() {
        String line = in.hasNextLine() ? in.nextLine().trim() : "";
        try {
            return Integer.parseInt(line);
        } catch (NumberFormatException e) {
            System.out.println("\"" + line + "\" is not a whole number.");
            return -1;
        }
    }
}
