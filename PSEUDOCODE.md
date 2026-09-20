# PART E — Pseudocode and Algorithm Representation
DSA521S Group Mini-Project 2026 — Group 11
NUST Campus Service Centre Simulation

Every algorithm below corresponds directly to the submitted Java implementation.
The Java file and method that implements each one is named above the pseudocode.

---

## 1. QUEUE

### enqueue(student) — `StudentQueue.enqueue()`

```
ALGORITHM enqueue(student)
INPUT : student record to be added to the waiting line
OUTPUT: the student is placed at the rear of the queue

1.  newNode <- new QNode holding student
2.  newNode.next <- NULL
3.  IF front = NULL THEN            // the queue is empty
4.      front <- newNode
5.      rear  <- newNode
6.  ELSE
7.      rear.next <- newNode        // link behind the current last node
8.      rear      <- newNode        // the new node becomes the rear
9.  END IF
10. size <- size + 1
END
```
Time complexity: O(1)

### dequeue() — `StudentQueue.dequeue()`

```
ALGORITHM dequeue()
OUTPUT: the student at the front (the next to be served), or NULL

1.  IF front = NULL THEN
2.      PRINT "Queue is empty"
3.      RETURN NULL
4.  END IF
5.  served <- front.data
6.  front  <- front.next            // move the front pointer forward
7.  IF front = NULL THEN            // the queue has just become empty
8.      rear <- NULL
9.  END IF
10. size <- size - 1
11. RETURN served
END
```
Time complexity: O(1)

### peek(), isEmpty(), displayQueue()

```
ALGORITHM peek()
1.  IF front = NULL THEN RETURN NULL
2.  RETURN front.data
END

ALGORITHM isEmpty()
1.  RETURN (front = NULL)
END

ALGORITHM displayQueue()
1.  IF isEmpty() THEN PRINT "queue is empty"; RETURN
2.  current  <- front
3.  position <- 1
4.  WHILE current <> NULL DO
5.      PRINT position, current.data
6.      current  <- current.next
7.      position <- position + 1
8.  END WHILE
END
```

---

## 2. STACK

### push(value) — `IntStack.push()`

```
ALGORITHM push(value)
1.  IF top = capacity - 1 THEN          // the array is full
2.      bigger <- new array of size capacity * 2
3.      FOR i <- 0 TO capacity - 1 DO
4.          bigger[i] <- items[i]
5.      END FOR
6.      items <- bigger
7.  END IF
8.  top <- top + 1
9.  items[top] <- value
END
```

### pop() — `IntStack.pop()`

```
ALGORITHM pop()
1.  IF top = -1 THEN ERROR "stack underflow"
2.  value <- items[top]
3.  top   <- top - 1
4.  RETURN value
END

ALGORITHM peek()
1.  IF top = -1 THEN ERROR "stack is empty"
2.  RETURN items[top]
END
```

### evaluatePostfix(expression) — `PostfixEvaluator.evaluate()`

```
ALGORITHM evaluatePostfix(expression)
INPUT : a postfix expression whose tokens are separated by spaces
OUTPUT: the numeric value of the expression

1.  CREATE empty stack S
2.  tokens <- split expression on spaces
3.  FOR EACH token IN tokens DO
4.      IF token is a number THEN
5.          S.push(token as number)
6.      ELSE                                  // token is + - * /
7.          IF S.size < 2 THEN ERROR "malformed expression"
8.          right <- S.pop()                  // second operand comes off first
9.          left  <- S.pop()
10.         result <- apply(left, token, right)
11.         S.push(result)
12.     END IF
13. END FOR
14. IF S.size <> 1 THEN ERROR "malformed expression"
15. answer <- S.peek()
16. RETURN S.pop()
END
```
Time complexity: O(n) for n tokens.

---

## 3. SINGLY LINKED LIST

### insertNode — at the beginning, at the end, at a position (`ServiceRecordList`)

```
ALGORITHM insertAtBeginning(student)
1.  newNode <- new Node holding student
2.  newNode.next <- head
3.  head <- newNode
4.  count <- count + 1
END

ALGORITHM insertAtEnd(student)
1.  newNode <- new Node holding student
2.  IF head = NULL THEN
3.      head <- newNode
4.  ELSE
5.      current <- head
6.      WHILE current.next <> NULL DO
7.          current <- current.next          // walk to the last node
8.      END WHILE
9.      current.next <- newNode
10. END IF
11. count <- count + 1
END

ALGORITHM insertAtPosition(student, position)      // position is 1-based
1.  IF position < 1 OR position > count + 1 THEN
2.      PRINT "invalid position"; RETURN FALSE
3.  END IF
4.  IF position = 1 THEN insertAtBeginning(student); RETURN TRUE
5.  newNode <- new Node holding student
6.  current <- head
7.  FOR i <- 1 TO position - 2 DO
8.      current <- current.next              // stop at the node BEFORE the position
9.  END FOR
10. newNode.next <- current.next
11. current.next <- newNode
12. count <- count + 1
13. RETURN TRUE
END
```

### deleteNode(studentNo) — `ServiceRecordList.deleteStudent()`

```
ALGORITHM deleteNode(studentNo)
1.  IF head = NULL THEN PRINT "list is empty"; RETURN FALSE
2.  IF head.data.studentNo = studentNo THEN     // deleting the head node
3.      head  <- head.next
4.      count <- count - 1
5.      RETURN TRUE
6.  END IF
7.  previous <- head
8.  current  <- head.next
9.  WHILE current <> NULL DO
10.     IF current.data.studentNo = studentNo THEN
11.         previous.next <- current.next        // bypass the deleted node
12.         count <- count - 1
13.         RETURN TRUE
14.     END IF
15.     previous <- current
16.     current  <- current.next
17. END WHILE
18. PRINT "student not found"
19. RETURN FALSE
END
```

### searchNode(studentNo) — `ServiceRecordList.searchStudent()`

```
ALGORITHM searchNode(studentNo)            // sequential / linear search
1.  current  <- head
2.  position <- 1
3.  WHILE current <> NULL DO
4.      IF current.data.studentNo = studentNo THEN
5.          PRINT "found at node", position
6.          RETURN current.data
7.      END IF
8.      current  <- current.next
9.      position <- position + 1
10. END WHILE
11. PRINT "not found"
12. RETURN NULL
END
```
Time complexity: O(n) — a linked list cannot be searched by index jumps.

### traverseList() — `ServiceRecordList.displayStudents()`

```
ALGORITHM traverseList()
1.  current  <- head
2.  position <- 1
3.  WHILE current <> NULL DO
4.      PRINT position, current.data.studentNo, name, serviceType, estimatedTime
5.      current  <- current.next
6.      position <- position + 1
7.  END WHILE
8.  PRINT "total records =", count
END
```

---

## 4. ARRAY STATISTICS — `DailyStatistics`

```
ALGORITHM computeDailyStatistics(serviceTimes, n)
1.  total <- 0; served <- 0
2.  highest <- serviceTimes[0]; lowest <- serviceTimes[0]; longerThanTen <- 0
3.  FOR i <- 0 TO n - 1 DO
4.      served <- served + 1
5.      total  <- total + serviceTimes[i]
6.      IF serviceTimes[i] > highest THEN highest <- serviceTimes[i]
7.      IF serviceTimes[i] < lowest  THEN lowest  <- serviceTimes[i]
8.      IF serviceTimes[i] > 10      THEN longerThanTen <- longerThanTen + 1
9.  END FOR
10. average <- total / served
11. RETURN served, total, average, highest, lowest, longerThanTen
END
```
Time complexity: O(n), a single traversal. No built-in max, min or sum is used.

---

## 5. SORTING ALGORITHMS

### selectionSort(A) — `Sorters.selectionSort()`

```
ALGORITHM selectionSort(A, n)
1.  FOR i <- 0 TO n - 2 DO
2.      minIndex <- i
3.      FOR j <- i + 1 TO n - 1 DO
4.          comparisons <- comparisons + 1
5.          IF A[j] < A[minIndex] THEN minIndex <- j
6.      END FOR
7.      IF minIndex <> i THEN
8.          SWAP A[i] WITH A[minIndex]
9.          swaps <- swaps + 1
10.     END IF
11. END FOR
END
```
Comparisons: always n(n-1)/2. Best = average = worst = O(n^2). Swaps at most n-1.

### insertionSort(A) — `Sorters.insertionSort()`

```
ALGORITHM insertionSort(A, n)
1.  FOR i <- 1 TO n - 1 DO
2.      key <- A[i]
3.      j   <- i - 1
4.      WHILE j >= 0 DO
5.          comparisons <- comparisons + 1
6.          IF A[j] > key THEN
7.              A[j + 1] <- A[j]              // shift the larger value right
8.              shifts <- shifts + 1
9.              j <- j - 1
10.         ELSE
11.             EXIT WHILE                    // correct position found
12.         END IF
13.     END WHILE
14.     A[j + 1] <- key
15. END FOR
END
```
Best case O(n) on sorted/almost-sorted data; worst and average O(n^2).

### mergeSort(A, low, high) — `Sorters.mergeSort()`

```
ALGORITHM mergeSort(A, low, high)
1.  IF low >= high THEN RETURN              // BASE CASE: 0 or 1 element is sorted
2.  mid <- low + (high - low) / 2
3.  mergeSort(A, low, mid)                  // divide: left half
4.  mergeSort(A, mid + 1, high)             // divide: right half
5.  merge(A, low, mid, high)                // conquer: combine the sorted halves
END

ALGORITHM merge(A, low, mid, high)
1.  L <- copy of A[low .. mid]
2.  R <- copy of A[mid + 1 .. high]
3.  i <- 0; j <- 0; k <- low
4.  WHILE i < length(L) AND j < length(R) DO
5.      comparisons <- comparisons + 1
6.      IF L[i] <= R[j] THEN A[k] <- L[i]; i <- i + 1
7.      ELSE                 A[k] <- R[j]; j <- j + 1
8.      END IF
9.      k <- k + 1
10. END WHILE
11. WHILE i < length(L) DO A[k] <- L[i]; i <- i + 1; k <- k + 1 END WHILE
12. WHILE j < length(R) DO A[k] <- R[j]; j <- j + 1; k <- k + 1 END WHILE
END
```
O(n log n) comparisons in every case; needs O(n) extra memory.

### quickSort(A, low, high) — `Sorters.quickSort()`

```
ALGORITHM quickSort(A, low, high)
1.  IF low >= high THEN RETURN              // BASE CASE: 0 or 1 element
2.  p <- partition(A, low, high)
3.  quickSort(A, low, p - 1)                // left partition (values <= pivot)
4.  quickSort(A, p + 1, high)               // right partition (values > pivot)
END

ALGORITHM partition(A, low, high)           // Lomuto scheme
PIVOT RULE: the LAST element of the sub-array, A[high]
1.  pivot <- A[high]
2.  i <- low - 1
3.  FOR j <- low TO high - 1 DO
4.      comparisons <- comparisons + 1
5.      IF A[j] <= pivot THEN
6.          i <- i + 1
7.          IF i <> j THEN SWAP A[i] WITH A[j]; swaps <- swaps + 1
8.      END IF
9.  END FOR
10. SWAP A[i + 1] WITH A[high]              // place the pivot in its final position
11. swaps <- swaps + 1
12. RETURN i + 1
END
```
Average O(n log n); worst case O(n^2) when the pivot is always the smallest or
largest value, which happens with this pivot rule on already-sorted input.
