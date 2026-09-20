/*
 * DSA521S - Task A3: Postfix Expression Evaluation using a Stack
 *
 * PostfixEvaluator.java
 * Independent stack exercise (not part of the service-centre menu).
 * Supported operators: +  -  *  /   (also accepts the symbols x and / written as
 * the multiplication sign and the division sign used in the project brief).
 *
 * Algorithm:
 *   scan the tokens from left to right
 *     if the token is a number  -> push it
 *     if the token is an operator -> pop two operands (right then left),
 *                                    apply the operator, push the result
 *   at the end the single value left on the stack is the answer.
 */
public class PostfixEvaluator {

    /* Evaluate quietly and return the result. */
    public static double evaluate(String expression) {
        return evaluate(expression, false);
    }

    /* Evaluate and, when trace is true, print the stack after each step. */
    public static double evaluate(String expression, boolean trace) {
        IntStack stack = new IntStack();
        String[] tokens = expression.trim().split("\\s+");

        if (trace) {
            System.out.println("Evaluating postfix expression: " + expression);
            System.out.println();
            System.out.printf("%-6s %-28s %s%n", "Token", "Action", "Stack (bottom -> top)");
            System.out.println("-------------------------------------------------------------------");
        }

        for (String token : tokens) {
            if (isOperator(token)) {
                if (stack.size() < 2) {
                    throw new IllegalArgumentException("Malformed expression: not enough operands for '" + token + "'.");
                }
                double right = stack.pop();   // second operand popped first
                double left = stack.pop();
                double result = apply(left, right, token);
                stack.push(result);
                if (trace) {
                    String action = "pop " + IntStack.format(right) + ", pop " + IntStack.format(left)
                            + ", push " + IntStack.format(left) + normalise(token) + IntStack.format(right)
                            + "=" + IntStack.format(result);
                    System.out.printf("%-6s %-28s %s%n", token, action, stack.contents());
                }
            } else {
                double value = Double.parseDouble(token);
                stack.push(value);
                if (trace) {
                    System.out.printf("%-6s %-28s %s%n", token, "push " + token, stack.contents());
                }
            }
        }

        if (stack.size() != 1) {
            throw new IllegalArgumentException("Malformed expression: " + stack.size() + " values left on the stack.");
        }
        double answer = stack.peek();   // peek() used before the final pop
        if (trace) {
            System.out.println("-------------------------------------------------------------------");
            System.out.println("peek() on the stack gives the final result = " + IntStack.format(answer));
        }
        return stack.pop();
    }

    private static boolean isOperator(String t) {
        return t.equals("+") || t.equals("-") || t.equals("*") || t.equals("/")
                || t.equals("x") || t.equals("X") || t.equals("\u00D7") || t.equals("\u00F7")
                || t.equals("\u2212");
    }

    private static String normalise(String op) {
        if (op.equals("x") || op.equals("X") || op.equals("\u00D7")) return "*";
        if (op.equals("\u00F7")) return "/";
        if (op.equals("\u2212")) return "-";
        return op;
    }

    private static double apply(double left, double right, String op) {
        String o = normalise(op);
        switch (o) {
            case "+": return left + right;
            case "-": return left - right;
            case "*": return left * right;
            case "/":
                if (right == 0) {
                    throw new ArithmeticException("Division by zero in the postfix expression.");
                }
                return left / right;
            default:
                throw new IllegalArgumentException("Unknown operator: " + op);
        }
    }

    /* Standalone demonstration, also callable from the demo runner. */
    public static void demo() {
        System.out.println("===============================================================");
        System.out.println("  TASK A3 - POSTFIX EXPRESSION EVALUATION USING A STACK");
        System.out.println("===============================================================");
        System.out.println();
        double r1 = evaluate("5 3 + 2 *", true);
        System.out.println("Result of \"5 3 + 2 *\"  =  " + IntStack.format(r1) + "   (expected 16)");
        System.out.println();
        System.out.println("Further checks (no trace printed):");
        System.out.println("  \"12 5 8 4 - * +\"      = " + IntStack.format(evaluate("12 5 8 4 - * +")));
        System.out.println("  \"20 4 / 3 +\"          = " + IntStack.format(evaluate("20 4 / 3 +")));
        System.out.println("  \"7 2 - 3 *\"           = " + IntStack.format(evaluate("7 2 - 3 *")));
        System.out.println();
    }

    public static void main(String[] args) {
        if (args.length > 0) {
            StringBuilder sb = new StringBuilder();
            for (String a : args) sb.append(a).append(' ');
            System.out.println("Result = " + IntStack.format(evaluate(sb.toString().trim(), true)));
        } else {
            demo();
        }
    }
}
