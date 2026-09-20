/*
 * DSA521S - Data Structures and Algorithms 1
 * NUST Campus Service Centre Simulation
 *
 * Student.java
 * Plain data holder for one student arriving at the service centre.
 * This is the "data part" that is stored inside the queue nodes and
 * inside the singly linked list nodes.
 */
public class Student {

    private String studentNo;       // e.g. "221045678"
    private String name;            // e.g. "Maria"
    private String serviceType;     // e.g. "Registration"
    private int estimatedServiceTime; // in minutes

    public Student(String studentNo, String name, String serviceType, int estimatedServiceTime) {
        this.studentNo = studentNo;
        this.name = name;
        this.serviceType = serviceType;
        this.estimatedServiceTime = estimatedServiceTime;
    }

    public String getStudentNo() { return studentNo; }
    public String getName() { return name; }
    public String getServiceType() { return serviceType; }
    public int getEstimatedServiceTime() { return estimatedServiceTime; }

    public void setServiceType(String serviceType) { this.serviceType = serviceType; }
    public void setEstimatedServiceTime(int t) { this.estimatedServiceTime = t; }

    /* Single-line representation used by the display operations. */
    @Override
    public String toString() {
        return String.format("%-10s %-10s %-18s %3d min",
                studentNo, name, serviceType, estimatedServiceTime);
    }

    /* Short representation used inside the queue diagram. */
    public String shortLabel() {
        return name + "(" + studentNo + ")";
    }

    public static String tableHeader() {
        return String.format("%-10s %-10s %-18s %s", "StudentNo", "Name", "Service", "Est.Time");
    }
}
