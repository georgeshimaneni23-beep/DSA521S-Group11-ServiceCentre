/*
 * DSA521S - Task A3: Stack used for postfix evaluation
 *
 * IntStack.java
 * A LIFO stack of double values implemented from scratch on a plain array
 * that grows when it becomes full. No built-in Stack class is used.
 */
public class IntStack {

    private double[] items;
    private int top;   // index of the top element; -1 when the stack is empty

    public IntStack() {
        this(16);
    }

    public IntStack(int capacity) {
        items = new double[capacity];
        top = -1;
    }

    public boolean isEmpty() {
        return top == -1;
    }

    public int size() {
        return top + 1;
    }

    /* -------- push -------- */
    public void push(double value) {
        if (top == items.length - 1) {   // stack full: grow the backing array manually
            double[] bigger = new double[items.length * 2];
            for (int i = 0; i < items.length; i++) {
                bigger[i] = items[i];
            }
            items = bigger;
        }
        top++;
        items[top] = value;
    }

    /* -------- pop -------- */
    public double pop() {
        if (isEmpty()) {
            throw new IllegalStateException("Stack underflow: pop() called on an empty stack.");
        }
        double value = items[top];
        top--;
        return value;
    }

    /* -------- peek -------- */
    public double peek() {
        if (isEmpty()) {
            throw new IllegalStateException("Stack is empty: nothing to peek().");
        }
        return items[top];
    }

    /* Bottom-to-top contents, for the required stack trace. */
    public String contents() {
        if (isEmpty()) return "[ ]  (empty)";
        StringBuilder sb = new StringBuilder("[ ");
        for (int i = 0; i <= top; i++) {
            sb.append(format(items[i]));
            if (i < top) sb.append(", ");
        }
        sb.append(" ]  <- top");
        return sb.toString();
    }

    public static String format(double v) {
        if (v == Math.rint(v) && !Double.isInfinite(v)) {
            return String.valueOf((long) v);
        }
        return String.valueOf(v);
    }
}
