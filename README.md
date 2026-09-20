# DSA521S — Data Structures and Algorithms 1
## Group Mini-Project 2026 — NUST Campus Service Centre Simulation

**Group Number: 11**

| # | Full Name | Student Number | Role |
|---|-----------|----------------|------|
| 1 | George Shimaneni | 225018497 | Group leader |
| 2 | Dipundhi Paul Peter | 225058146 | Member |
| 3 | Mangulukeni Kayoko | 227074404 | Member |
| 4 | Nelumbu Rachel | 225049511 | Member |
| 5 | Enerist T Shilumbu | 222093951 | Member |

**Submitted by: 225018497 – George Shimaneni**

**GitHub repository: https://github.com/georgeshimaneni23-beep/DSA521S-Group11-ServiceCentre**

---

## 1. What this project is

A menu-driven Java simulation of the NUST student service centre. It demonstrates
the selection, implementation and analysis of core data structures and algorithms:

| Component | Structure / Algorithm | Java file |
|-----------|----------------------|-----------|
| Waiting line (Task A1) | Queue (linked, FIFO) | `StudentQueue.java` |
| Student service records (Task A2) | Singly linked list | `ServiceRecordList.java` |
| Postfix expression evaluation (Task A3) | Stack (array-based, LIFO) | `IntStack.java`, `PostfixEvaluator.java` |
| Daily statistics (Task A4) | Array with manual traversal | `DailyStatistics.java` |
| Four sorting algorithms (Part B) | Selection, Insertion, Merge, Quick | `Sorters.java` |
| Algorithm experiment (Part C) | Comparison and timing harness | `SortingExperiment.java` |
| Integrated system (Part D) | Menu tying all of the above together | `ServiceCentreApp.java` |
| Supporting data / helpers | Student record, array helpers | `Student.java`, `ArrayUtil.java` |
| Non-interactive demonstration | Prints every required trace | `DemoRunner.java` |

Every data structure and every sorting algorithm is written from scratch.
No built-in `Queue`, `Stack`, `LinkedList`, `Arrays.sort()`, `Collections.sort()`,
`Math.max()`, `Math.min()` or stream `sum()` is used anywhere in the solution.

## 2. Requirements

- Java Development Kit (JDK) 8 or newer (`javac` and `java` on the PATH).
- A terminal / command prompt. No GUI, no external libraries, no build tool needed.

Check your installation with:

```
java -version
javac -version
```

## 3. How to compile and run

From the folder that contains this README:

```
# 1. compile every source file into the out/ folder
javac -d out src/*.java

# 2a. run the integrated service-centre system (Part D, interactive menu)
java -cp out ServiceCentreApp

# 2b. run every Part A, B and C demonstration in one pass (no typing needed)
java -cp out DemoRunner
#    (identical to:  java -cp out ServiceCentreApp --demo)

# 2c. run only the postfix stack exercise (Task A3)
java -cp out PostfixEvaluator
java -cp out PostfixEvaluator 12 5 8 4 - "*" +      # evaluate your own expression

# 2d. run only the sorting experiment (Part C)
java -cp out SortingExperiment
```

On Windows Command Prompt the same commands work; use `javac -d out src\*.java`.

### The menu (Part D)

```
========================================
        CAMPUS SERVICE CENTRE
========================================
 1. Add student to waiting queue            -> Queue: enqueue
 2. Serve next student (remove from queue)  -> Queue: peek + dequeue
 3. Display waiting students                -> Queue: traversal
 4. Add student service record              -> Linked list: insertStudent()
 5. Display student service records         -> Linked list: traversal
 6. Search for student record               -> Linked list: linear search
 7. Remove student record                   -> Linked list: deletion
 8. Display daily statistics                -> Array processing
 9. Sort service times                      -> Selection/Insertion/Merge/Quick
10. Run sorting experiment                  -> Part C experiment
11. Exit
```

The four students from the project brief (Maria, Tomas, Ndapewa, Simon) are
pre-loaded when the program starts, so options 2, 3, 5, 6, 7 and 9 work
immediately. Option 2 also records the served student's service time in the
statistics array, which is what option 8 then reports on.

## 4. Files in this submission

```
DSA521S_Group11_Project2026/
├── README.md                       this file
├── PSEUDOCODE.md                   Part E pseudocode (also inside the report)
├── DSA521S_Group11_Project_Report.pdf   the project report (Part F)
├── src/                            all Java source files
├── screenshots/                    console evidence used in the report
├── demo_output.txt                 full captured output of DemoRunner
└── menu_session.txt                full captured output of a menu session
```

## 5. Task allocation

| Member | Student number | Assigned responsibility | Main files |
| --- | --- | --- | --- |
| George Shimaneni (leader) | 225018497 | Repository setup, integration of all components into the menu system, group testing, final report and submission | `ServiceCentreApp.java` |
| Mangulukeni Kayoko | 227074404 | Queue: enqueue, dequeue, peek, isEmpty, displayQueue, waiting-line simulation, queue diagrams and justification | `StudentQueue.java`, `Student.java` |
| Dipundhi Paul Peter | 225058146 | Singly linked list: insertStudent, deleteStudent, searchStudent, displayStudents, memory pointer diagrams and justification | `ServiceRecordList.java` |
| Nelumbu Rachel | 225049511 | Stack and postfix evaluation: push, pop, peek, step-by-step stack traces, pseudocode and justification | `IntStack.java`, `PostfixEvaluator.java` |
| Enerist T Shilumbu | 222093951 | Sorting algorithms: Selection, Insertion, Merge and Quick Sort without built-in functions, traces and comparison counters | `Sorters.java`, `SortingExperiment.java`, `ArrayUtil.java`, `DailyStatistics.java` |

Every member reviewed the complete project and is able to explain any section of
the code, pseudocode, diagrams or algorithm choices, as required by Section 11
of the project specification.

## 6. Notes for the marker

- `DemoRunner` prints every trace the brief asks for: six arrivals and three
  students served, linked-list diagrams before and after insertion and deletion,
  the postfix stack contents after each step, the array statistics, the first
  three passes of Selection and Insertion Sort, the full merge-sort divide and
  merge tree with the base case, the first two Quick Sort partitioning stages,
  and the complete Part C experiment tables.
- The Part C experiment uses a fixed random seed (2026) so the tables in the
  report can be reproduced exactly. Execution times will differ from machine to
  machine; the comparison counts will not.
- The postfix stack exercise (Task A3) is kept separate from the service-centre
  menu, as the brief requires.

## 7. Academic integrity

All group members participated in the development, understand the submitted
data structures, algorithms, pseudocode and source code, and can explain and
defend any part of the solution.
