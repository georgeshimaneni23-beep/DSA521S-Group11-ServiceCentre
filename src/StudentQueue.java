/*
 * DSA521S - Task A1: Waiting Line (Queue)
 *
 * StudentQueue.java
 * A FIFO queue of Student objects, implemented from scratch using a
 * singly linked chain of QNode objects with a front and a rear pointer.
 * No built-in Java collection class is used.
 *
 * enqueue()  - O(1), adds at the rear
 * dequeue()  - O(1), removes from the front
 * peek()     - O(1)
 * isEmpty()  - O(1)
 * displayQueue() - O(n) traversal from front to rear
 */
public class StudentQueue {

    /* Internal node of the queue. */
    private static class QNode {
        Student data;
        QNode next;
        QNode(Student data) {
            this.data = data;
            this.next = null;
        }
    }

    private QNode front; // where students leave (are served)
    private QNode rear;  // where students join
    private int size;

    public StudentQueue() {
        front = null;
        rear = null;
        size = 0;
    }

    /* ---------------- enqueue ---------------- */
    public void enqueue(Student s) {
        QNode newNode = new QNode(s);
        if (isEmpty()) {              // empty queue: front and rear are the same node
            front = newNode;
            rear = newNode;
        } else {                      // link the new node behind the current rear
            rear.next = newNode;
            rear = newNode;
        }
        size++;
    }

    /* ---------------- dequeue ---------------- */
    public Student dequeue() {
        if (isEmpty()) {
            System.out.println("Queue is empty - there is no student to serve.");
            return null;
        }
        Student served = front.data;
        front = front.next;           // move the front pointer forward
        if (front == null) {          // the queue has just become empty
            rear = null;
        }
        size--;
        return served;
    }

    /* ---------------- peek ---------------- */
    public Student peek() {
        if (isEmpty()) {
            return null;
        }
        return front.data;
    }

    /* ---------------- isEmpty ---------------- */
    public boolean isEmpty() {
        return front == null;
    }

    public int size() {
        return size;
    }

    /* ---------------- displayQueue ---------------- */
    public void displayQueue() {
        System.out.println("--- WAITING QUEUE (front to rear) ---");
        if (isEmpty()) {
            System.out.println("(the waiting queue is empty)");
            return;
        }
        System.out.println("Pos  " + Student.tableHeader());
        QNode current = front;
        int position = 1;
        while (current != null) {      // traversal
            System.out.printf("%-4d %s%n", position, current.data.toString());
            current = current.next;
            position++;
        }
        System.out.println("Front of queue : " + front.data.shortLabel());
        System.out.println("Rear of queue  : " + rear.data.shortLabel());
        System.out.println("Students waiting: " + size);
    }

    /* Text queue diagram, e.g.  FRONT -> [Maria] -> [Tomas] -> REAR */
    public String diagram() {
        StringBuilder sb = new StringBuilder("FRONT -> ");
        QNode current = front;
        if (current == null) {
            return "FRONT -> (empty) -> REAR";
        }
        while (current != null) {
            sb.append("[").append(current.data.getName()).append("]");
            sb.append(" -> ");
            current = current.next;
        }
        sb.append("REAR");
        return sb.toString();
    }
}
