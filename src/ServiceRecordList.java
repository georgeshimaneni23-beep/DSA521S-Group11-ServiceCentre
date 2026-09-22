/*
 * DSA521S - Task A2: Student Service Records (Singly Linked List)
 *
 * ServiceRecordList.java
 * A singly linked list built from scratch. Every node holds a data part
 * (Student: student number, name, service type, estimated service time)
 * and a next pointer to the following node.
 *
 * Operations:
 *   insertStudent(...)  - at the beginning, at the end, at a given position
 *   deleteStudent(...)  - by student number
 *   searchStudent(...)  - linear search by student number or by name
 *   displayStudents()   - traversal from head to the last node
 * Author: Dipundhi Paul Peter (225058146) - Singly linked list and memory pointer programs
 */
public class ServiceRecordList {

    /* Node of the singly linked list. */
    public static class Node {
        Student data;   // data part
        Node next;      // pointer to the next node
        Node(Student data) {
            this.data = data;
            this.next = null;
        }
    }

    private Node head;
    private int count;

    public ServiceRecordList() {
        head = null;
        count = 0;
    }

    public boolean isEmpty() { return head == null; }
    public int size() { return count; }

    /* -------- insertStudent: insertion at the BEGINNING -------- */
    public void insertAtBeginning(Student s) {
        Node newNode = new Node(s);
        newNode.next = head;   // new node points to the old first node
        head = newNode;        // head now points to the new node
        count++;
    }

    /* -------- insertStudent: insertion at the END -------- */
    public void insertAtEnd(Student s) {
        Node newNode = new Node(s);
        if (head == null) {
            head = newNode;
        } else {
            Node current = head;
            while (current.next != null) {  // walk to the last node
                current = current.next;
            }
            current.next = newNode;         // link the last node to the new node
        }
        count++;
    }

    /*
     * -------- insertStudent: insertion at a SPECIFIED POSITION --------
     * position is 1-based: position 1 means the new node becomes the head.
     */
    public boolean insertAtPosition(Student s, int position) {
        if (position < 1 || position > count + 1) {
            System.out.println("Invalid position. Valid positions are 1 to " + (count + 1) + ".");
            return false;
        }
        if (position == 1) {
            insertAtBeginning(s);
            return true;
        }
        Node newNode = new Node(s);
        Node current = head;
        for (int i = 1; i < position - 1; i++) {  // stop at the node BEFORE the position
            current = current.next;
        }
        newNode.next = current.next;   // new node points to the rest of the list
        current.next = newNode;        // previous node points to the new node
        count++;
        return true;
    }

    /* Generic entry point matching the required method name insertStudent(). */
    public boolean insertStudent(Student s, int mode, int position) {
        // mode 1 = beginning, 2 = end, 3 = at position
        if (mode == 1) { insertAtBeginning(s); return true; }
        if (mode == 2) { insertAtEnd(s); return true; }
        return insertAtPosition(s, position);
    }

    /* -------- deleteStudent: delete by student number -------- */
    public boolean deleteStudent(String studentNo) {
        if (head == null) {
            System.out.println("The record list is empty - nothing to delete.");
            return false;
        }
        if (head.data.getStudentNo().equals(studentNo)) {  // deleting the head
            head = head.next;
            count--;
            return true;
        }
        Node previous = head;
        Node current = head.next;
        while (current != null) {
            if (current.data.getStudentNo().equals(studentNo)) {
                previous.next = current.next;  // bypass the deleted node
                count--;
                return true;
            }
            previous = current;
            current = current.next;
        }
        System.out.println("Student number " + studentNo + " was not found.");
        return false;
    }

    /* -------- searchStudent: linear search by student number -------- */
    public Student searchStudent(String studentNo) {
        Node current = head;
        int position = 1;
        while (current != null) {
            if (current.data.getStudentNo().equals(studentNo)) {
                System.out.println("Found at node position " + position
                        + " after " + position + " comparison(s).");
                return current.data;
            }
            current = current.next;
            position++;
        }
        System.out.println("Student number " + studentNo + " is not in the record list ("
                + (position - 1) + " comparison(s) made).");
        return null;
    }

    /* -------- searchStudent by name (case-insensitive linear search) -------- */
    public Student searchByName(String name) {
        Node current = head;
        int position = 1;
        while (current != null) {
            if (current.data.getName().equalsIgnoreCase(name)) {
                System.out.println("Found at node position " + position + ".");
                return current.data;
            }
            current = current.next;
            position++;
        }
        System.out.println("No record found for name \"" + name + "\".");
        return null;
    }

    /* -------- displayStudents: full traversal -------- */
    public void displayStudents() {
        System.out.println("--- STUDENT SERVICE RECORDS (linked list, head to tail) ---");
        if (head == null) {
            System.out.println("(no service records yet)");
            return;
        }
        System.out.println("Node " + Student.tableHeader());
        Node current = head;
        int position = 1;
        while (current != null) {
            System.out.printf("%-4d %s%n", position, current.data.toString());
            current = current.next;
            position++;
        }
        System.out.println("Total records: " + count);
    }

    /* Text diagram, e.g. HEAD -> [Maria|next] -> [Tomas|next] -> NULL */
    public String diagram() {
        StringBuilder sb = new StringBuilder("HEAD -> ");
        Node current = head;
        if (current == null) return "HEAD -> NULL";
        while (current != null) {
            sb.append("[").append(current.data.getName()).append(" | next]").append(" -> ");
            current = current.next;
        }
        sb.append("NULL");
        return sb.toString();
    }

    /*
     * Copies the estimated service times of all records into a plain int array.
     * Used by the Array statistics task and by the sorting menu option.
     */
    public int[] serviceTimesAsArray() {
        int[] times = new int[count];
        Node current = head;
        int i = 0;
        while (current != null) {
            times[i] = current.data.getEstimatedServiceTime();
            i++;
            current = current.next;
        }
        return times;
    }
}
