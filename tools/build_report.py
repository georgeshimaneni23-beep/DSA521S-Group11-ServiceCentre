"""Builds the DSA521S Group 11 project report PDF (Part F)."""
import os, re, urllib.request
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image, PageBreak, KeepTogether,
                                Preformatted)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE = "/home/user/workspace/DSA521S_Project"
SHOTS = os.path.join(BASE, "screenshots")
FONTS = os.path.join(BASE, "tools", "fonts")
os.makedirs(FONTS, exist_ok=True)

REPO_URL = open(os.path.join(BASE, "tools", "repo_url.txt")).read().strip()

# ---------------- fonts ----------------
FONT_URLS = {
    "DMSans": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz%2Cwght%5D.ttf",
}
BODY, BOLD, MONO = "Helvetica", "Helvetica-Bold", "Courier"
try:
    for name, url in FONT_URLS.items():
        p = os.path.join(FONTS, name + ".ttf")
        if not os.path.exists(p):
            urllib.request.urlretrieve(url, p)
    pdfmetrics.registerFont(TTFont("DMSans", os.path.join(FONTS, "DMSans.ttf")))
    BODY = "DMSans"
except Exception as e:
    print("font download skipped:", e)

for cand in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]:
    if os.path.exists(cand):
        pdfmetrics.registerFont(TTFont("DejaVuMono", cand))
        MONO = "DejaVuMono"
        break

INK = colors.HexColor("#28251D")
MUTED = colors.HexColor("#5F5D57")
TEAL = colors.HexColor("#01696F")
LINE = colors.HexColor("#D4D1CA")
SOFT = colors.HexColor("#F1EFE9")

S = {
    "title": ParagraphStyle("title", fontName=BOLD, fontSize=21, leading=26, textColor=INK, alignment=TA_CENTER),
    "sub": ParagraphStyle("sub", fontName=BODY, fontSize=12.5, leading=18, textColor=MUTED, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName=BOLD, fontSize=15, leading=19, textColor=TEAL, spaceBefore=6, spaceAfter=7),
    "h2": ParagraphStyle("h2", fontName=BOLD, fontSize=11.5, leading=15, textColor=INK, spaceBefore=9, spaceAfter=4),
    "h3": ParagraphStyle("h3", fontName=BOLD, fontSize=10, leading=13.5, textColor=MUTED, spaceBefore=7, spaceAfter=3),
    "body": ParagraphStyle("body", fontName=BODY, fontSize=9.7, leading=14.2, textColor=INK, spaceAfter=6),
    "bullet": ParagraphStyle("bullet", fontName=BODY, fontSize=9.7, leading=14.2, textColor=INK,
                             leftIndent=12, bulletIndent=3, spaceAfter=3),
    "cap": ParagraphStyle("cap", fontName=BODY, fontSize=8.2, leading=11, textColor=MUTED,
                          alignment=TA_CENTER, spaceBefore=3, spaceAfter=9),
    "cell": ParagraphStyle("cell", fontName=BODY, fontSize=9, leading=12.4, textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName=BOLD, fontSize=9, leading=12.4, textColor=colors.white),
    "code": ParagraphStyle("code", fontName=MONO, fontSize=7.4, leading=9.4, textColor=INK),
}

story = []
A = story.append


def P(t, s="body"):
    A(Paragraph(t, S[s]))


def H1(t):
    A(Paragraph(t, S["h1"]))
    A(Table([[""]], colWidths=[165 * mm], rowHeights=[1.1],
            style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), TEAL)])))
    A(Spacer(1, 7))


def H2(t): A(Paragraph(t, S["h2"]))
def H3(t): A(Paragraph(t, S["h3"]))


def bullets(items):
    for it in items:
        A(Paragraph(it, S["bullet"], bulletText="\u2022"))
    A(Spacer(1, 4))


def code(text, size=7.4):
    st = ParagraphStyle("c", parent=S["code"], fontSize=size, leading=size * 1.28)
    A(Table([[Preformatted(text.strip("\n"), st)]], colWidths=[165 * mm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ])))
    A(Spacer(1, 8))


def table(rows, widths, align_right=()):
    data = [[Paragraph(str(c), S["cellb"]) for c in rows[0]]]
    for r in rows[1:]:
        data.append([Paragraph(str(c), S["cell"]) for c in r])
    st = [("BACKGROUND", (0, 0), (-1, 0), TEAL),
          ("GRID", (0, 0), (-1, -1), 0.4, LINE),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F9F8F5")))
    for c in align_right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    A(Table(data, colWidths=widths, style=TableStyle(st), repeatRows=1))
    A(Spacer(1, 9))


def shot(name, caption, max_w=165 * mm, max_h=185 * mm):
    from PIL import Image as PILImage
    path = os.path.join(SHOTS, name)
    iw, ih = PILImage.open(path).size
    scale = min(max_w / iw, max_h / ih, 1.0)
    img = Image(path, iw * scale, ih * scale)
    A(KeepTogether([img, Paragraph(caption, S["cap"])]))


# ======================= COVER =======================
A(Spacer(1, 22 * mm))
P("NAMIBIA UNIVERSITY OF SCIENCE AND TECHNOLOGY", "sub")
P("DSA521S &mdash; DATA STRUCTURES AND ALGORITHMS 1", "sub")
A(Spacer(1, 12 * mm))
P("NUST Service Centre Simulation", "title")
P("Designing and Evaluating Data Structures and Algorithms", "title")
A(Spacer(1, 5 * mm))
P("Group Mini-Project 2026 &mdash; Project Report", "sub")
A(Spacer(1, 14 * mm))
P("<b>GROUP 11</b>", "sub")
A(Spacer(1, 4 * mm))
table([["#", "Full Name", "Student Number", "Role"],
       ["1", "George Shimaneni", "225018497", "Group leader"],
       ["2", "Dipundhi Paul Peter", "225058146", "Member"],
       ["3", "Mangulukeni Kayoko", "227074404", "Member"],
       ["4", "Nelumbu Rachel", "225049511", "Member"],
       ["5", "Enerist T Shilumbu", "222093951", "Member"]],
      [12 * mm, 68 * mm, 40 * mm, 45 * mm])
A(Spacer(1, 8 * mm))
table([["Item", "Detail"],
       ["Programming language", "Java (JDK 8 or newer), console based"],
       ["Submitted by", "225018497 &ndash; George Shimaneni"],
       ["Submission date", "25 September 2026"],
       ["GitHub repository", f'<a href="{REPO_URL}" color="#01696F">{REPO_URL}</a>'],
       ["Declaration", "All data structures and sorting algorithms in this project were implemented "
                       "by the group. No built-in Java collection or sorting method was used as a "
                       "replacement. Every member understands and can defend the submitted solution."]],
      [42 * mm, 123 * mm])
A(PageBreak())

# ======================= CONTENTS / OVERVIEW =======================
H1("1. Introduction and System Overview")
P("This report documents Group 11's solution to the DSA521S Campus Service Centre "
  "simulation. The program models a normal day at the NUST student service centre: "
  "students arrive for registration, fee enquiries, student-card replacement, academic "
  "enquiries and document collection, they wait in a single line, they are assisted in "
  "arrival order, a permanent service record is kept for each of them, and the day's "
  "service times are then analysed and sorted.")
P("The emphasis is not on a user interface. Every data structure and every sorting "
  "algorithm is implemented from first principles so that the behaviour, the cost and the "
  "suitability of each one can be demonstrated and measured.")
H2("Structure of the solution")
table([["Part", "Requirement", "Structure / algorithm", "Java file"],
       ["A1", "Waiting line", "Queue (FIFO, linked nodes)", "StudentQueue.java"],
       ["A2", "Student service records", "Singly linked list", "ServiceRecordList.java"],
       ["A3", "Postfix evaluation", "Stack (LIFO, array based)", "IntStack.java, PostfixEvaluator.java"],
       ["A4", "Daily statistics", "Array with manual traversal", "DailyStatistics.java"],
       ["B", "Four sorting algorithms", "Selection, Insertion, Merge, Quick", "Sorters.java"],
       ["C", "Algorithm experiment", "Comparison counting and timing", "SortingExperiment.java"],
       ["D", "Integrated system", "Menu driving all of the above", "ServiceCentreApp.java"],
       ["&mdash;", "Shared data and helpers", "Student record, array helpers", "Student.java, ArrayUtil.java"],
       ["&mdash;", "Automatic demonstration", "Prints every required trace", "DemoRunner.java"]],
      [14 * mm, 44 * mm, 52 * mm, 55 * mm])
P("<b>How to run:</b> <font name='%s' size='8.5'>javac -d out src/*.java</font> then "
  "<font name='%s' size='8.5'>java -cp out ServiceCentreApp</font> for the interactive "
  "menu, or <font name='%s' size='8.5'>java -cp out DemoRunner</font> to print every "
  "demonstration and trace shown in this report." % (MONO, MONO, MONO))

# ======================= PART A =======================
A(PageBreak())
H1("2. Part A &mdash; Data Structure Design")

H2("2.1 Task A1 &mdash; Waiting Line (Queue)")
P("The waiting line is a queue of <font name='%s' size='8.5'>Student</font> objects built "
  "from a chain of internal nodes with a <b>front</b> pointer (where students leave) and a "
  "<b>rear</b> pointer (where students join). Because both ends are tracked, "
  "<font name='%s' size='8.5'>enqueue()</font> and <font name='%s' size='8.5'>dequeue()</font> "
  "are both O(1) no matter how long the line becomes." % (MONO, MONO, MONO))
H3("Queue diagram &mdash; after six arrivals")
code("""
 front                                                              rear
   |                                                                  |
   v                                                                  v
+---------+   +---------+   +-----------+   +---------+   +-----------+   +----------+
|  Maria  |-->|  Tomas  |-->|  Ndapewa  |-->|  Simon  |-->|  Johanna  |-->|  Petrus  |--> NULL
| 12 min  |   |  5 min  |   |   8 min   |   |  4 min  |   |   9 min   |   |  15 min  |
+---------+   +---------+   +-----------+   +---------+   +-----------+   +----------+
  arrival 1     arrival 2      arrival 3      arrival 4      arrival 5       arrival 6

  enqueue(student) adds at the REAR  -->            <-- dequeue() removes from the FRONT
""", 7.0)
H3("Queue diagram &mdash; after three students have been served")
code("""
 front                              rear
   |                                  |
   v                                  v
+---------+   +-----------+   +----------+
|  Simon  |-->|  Johanna  |-->|  Petrus  |--> NULL      Maria, Tomas and Ndapewa were
|  4 min  |   |   9 min   |   |  15 min  |              removed from the front, in the
+---------+   +-----------+   +----------+              exact order in which they arrived.
""", 7.0)
P("Pseudocode for <font name='%s' size='8.5'>enqueue()</font> and "
  "<font name='%s' size='8.5'>dequeue()</font> is given in section 6.1." % (MONO, MONO))
shot("07_taskA1_queue_demo.png",
     "Figure 1 &mdash; Task A1: six arrivals (enqueue), peek(), isEmpty(), displayQueue() and three students served (dequeue).")
H3("Why a queue is appropriate")
P("Service-centre policy is that students are assisted in the order in which they arrived. "
  "A queue enforces that rule structurally: values can only be added at the rear and can "
  "only be removed from the front, so the student who has waited longest is always the next "
  "one served and no code path can accidentally jump the line. An array would need every "
  "remaining element shifted forward each time a student is served (O(n) per service), and a "
  "stack would serve the most recent arrival first, which is precisely the wrong behaviour.")

A(PageBreak())
H2("2.2 Task A2 &mdash; Student Service Records (Singly Linked List)")
P("Each node stores a data part (student number, name, service type, estimated service "
  "time) and a <b>next</b> pointer. The list supports insertion at the beginning, at the "
  "end and at a specified position, deletion by student number, linear search and full "
  "traversal. This same list and these same operations are used by menu options 4 to 7 of "
  "the integrated system in Part D.")
H3("Link change 1 &mdash; insertion at position 3 (Johanna)")
code("""
BEFORE
head
  |
  v
+---------+     +---------+     +---------+     +-----------+
|  Simon  |---->|  Maria  |---->|  Tomas  |---->|  Ndapewa  |----> NULL
+---------+     +---------+     +---------+     +-----------+
  node 1          node 2          node 3           node 4

AFTER  insertStudent(Johanna, position 3)
head
  |
  v
+---------+     +---------+     +-----------+     +---------+     +-----------+
|  Simon  |---->|  Maria  |---->|  Johanna  |---->|  Tomas  |---->|  Ndapewa  |----> NULL
+---------+     +---------+     +-----------+     +---------+     +-----------+
  node 1          node 2           NEW node 3       node 4           node 5

Two links change:  (1) Johanna.next  <- the node that followed Maria (Tomas)
                   (2) Maria.next    <- Johanna
No other node moves in memory, and nothing is shifted.
""", 7.0)
H3("Link change 2 &mdash; deletion of Tomas (222034512)")
code("""
BEFORE
head
  |
  v
+---------+     +---------+     +-----------+     +---------+     +-----------+
|  Simon  |---->|  Maria  |---->|  Johanna  |---->|  Tomas  |---->|  Ndapewa  |----> NULL
+---------+     +---------+     +-----------+     +---------+     +-----------+
                                   previous          target

AFTER  deleteStudent("222034512")
head
  |
  v
+---------+     +---------+     +-----------+     +-----------+
|  Simon  |---->|  Maria  |---->|  Johanna  |---->|  Ndapewa  |----> NULL
+---------+     +---------+     +-----------+     +-----------+
                                       \\
                                        `--> (Tomas node is bypassed and is no
                                              longer reachable from head)

One link changes:  previous.next <- target.next
""", 7.0)
shot("08_taskA2_linkedlist_demo.png",
     "Figure 2 &mdash; Task A2: insertion at the beginning, at the end and at position 3, showing the list before and after each link change.")
P("Insertion at the beginning is O(1); insertion at the end or at position k, deletion and "
  "search all require walking the chain, so they are O(n) in the worst case. The search in "
  "the demonstration run found student 223041876 at node 5 after 5 comparisons, and reported "
  "5 comparisons before concluding that 999999999 is absent &mdash; the expected behaviour of a "
  "sequential search on an unsorted list.")

A(PageBreak())
H2("2.3 Task A3 &mdash; Postfix Expression Evaluation (Stack)")
P("This is an independent exercise and is deliberately not part of the service-centre menu. "
  "The stack is array-based and grows by copying into a larger array when it becomes full. "
  "Operands are pushed; when an operator is read, the top two values are popped (the "
  "<i>second</i> operand is popped first), the operation is applied, and the result is pushed "
  "back. The operators +, &minus;, &times; and &divide; are supported.")
H3("Trace of 5 3 + 2 *")
table([["Step", "Token", "Action", "Stack (bottom &rarr; top)"],
       ["1", "5", "push 5", "[ 5 ]"],
       ["2", "3", "push 3", "[ 5, 3 ]"],
       ["3", "+", "pop 3, pop 5, push 5 + 3 = 8", "[ 8 ]"],
       ["4", "2", "push 2", "[ 8, 2 ]"],
       ["5", "*", "pop 2, pop 8, push 8 &times; 2 = 16", "[ 16 ]"],
       ["6", "&mdash;", "peek() reads the answer, then pop()", "[ ] &rarr; result = <b>16</b>"]],
      [13 * mm, 15 * mm, 82 * mm, 55 * mm])
shot("06_taskA3_postfix_stack.png",
     "Figure 3 &mdash; Task A3: the stack contents printed after every operation, with three further expressions verified.")
H3("Why a stack is appropriate")
P("In postfix notation the operands an operator needs are always the two most recently "
  "produced values, and results feed straight back into later operators. That is exactly "
  "last-in-first-out behaviour, so push() and pop() supply the correct operands with no "
  "searching and no index arithmetic. The whole expression is evaluated in a single O(n) pass.")

A(PageBreak())
H2("2.4 Task A4 &mdash; Daily Statistics (Array)")
P("Every time a student is served, the service time is appended to a plain "
  "<font name='%s' size='8.5'>int</font> array (the array is grown manually by copying into a "
  "larger one when it fills up). All six statistics are then produced by traversing that array "
  "with ordinary loops. No built-in max(), min(), sum(), average or stream helper is used." % MONO)
H3("Worked example &mdash; array [12, 5, 8, 4, 9, 15, 3, 11]")
table([["Statistic", "Method of calculation", "Result"],
       ["Total students served", "counter incremented once per array position", "8"],
       ["Total service time", "running total accumulated over one pass", "67 minutes"],
       ["Average service time", "total &divide; number of students", "8.38 minutes"],
       ["Highest service time", "first element kept, replaced whenever a larger value is met", "15 minutes"],
       ["Lowest service time", "first element kept, replaced whenever a smaller value is met", "3 minutes"],
       ["Services longer than 10 min", "counter incremented when element &gt; 10 (12, 15, 11)", "3"]],
      [42 * mm, 96 * mm, 27 * mm])
shot("02_option2_serve_option8_stats.png",
     "Figure 4 &mdash; menu option 2 (serving a student, whose service time is recorded in the array) followed by menu option 8 (the array statistics).")
H3("Why an array is appropriate")
P("The statistics are computed over a fixed set of completed service times: values are only "
  "appended at the end and read back in order, never inserted in the middle. An array stores "
  "those values contiguously with O(1) access by index, so a single traversal computes all six "
  "figures, and no memory is wasted on pointers. It is also the natural input form for the "
  "sorting algorithms in Part B, which need direct index access to swap values in place &mdash; "
  "something a singly linked list cannot provide efficiently.")

H2("2.5 Task A5 &mdash; Data-Structure Justification")
table([["Structure", "Assigned task", "Why its behaviour fits this task"],
       ["Queue", "Waiting line (A1)",
        "Students must be assisted in arrival order. FIFO removal from the front and insertion "
        "at the rear make that policy part of the structure itself, so the order cannot be "
        "broken by a coding mistake. Both operations are O(1), so the program does not slow "
        "down as the line grows, whereas serving from the front of an array would cost O(n) "
        "in shifting every time."],
       ["Singly linked list", "Student service records (A2)",
        "The number of records for a day is unknown in advance and records are inserted at "
        "chosen positions and removed from the middle. A linked list allocates one node at a "
        "time so it never has to be resized, and an insertion or deletion only re-points one "
        "or two next references instead of shifting every later element as an array would. "
        "Only a forward traversal is ever needed, so the extra memory of a doubly linked list "
        "would not be justified."],
       ["Stack", "Postfix evaluation (A3)",
        "The operands required by an operator are always the two most recently produced "
        "values, and each result is immediately available to the next operator. That is "
        "last-in-first-out access, so push() and pop() hand back exactly the right operands "
        "with no searching, letting the expression be evaluated in one O(n) pass."],
       ["Array", "Daily statistics (A4)",
        "The service times form a fixed, index-addressable block that is only appended to and "
        "then read in order. Contiguous storage with O(1) index access lets a single loop "
        "compute the total, average, highest, lowest and over-10-minute count, and gives the "
        "sorting algorithms the in-place element swapping they depend on."]],
      [30 * mm, 36 * mm, 99 * mm])

# ======================= PART B =======================
A(PageBreak())
H1("3. Part B &mdash; Sorting Algorithm Challenge")
P("All four algorithms sort the array given in the brief, "
  "<font name='%s' size='8.5'>[17, 5, 23, 8, 14, 3, 11, 20, 6, 9]</font>, into ascending order. "
  "Each one produced <font name='%s' size='8.5'>[3, 5, 6, 8, 9, 11, 14, 17, 20, 23]</font>. "
  "Only comparisons between data values are counted." % (MONO, MONO))
table([["Algorithm", "Comparisons", "Movements", "Movement type"],
       ["Selection Sort", "45", "7", "swaps"],
       ["Insertion Sort", "32", "25", "shifts"],
       ["Merge Sort", "23", "34", "merge moves"],
       ["Quick Sort", "20", "12", "swaps"]],
      [50 * mm, 38 * mm, 38 * mm, 39 * mm], align_right=(1, 2))

H2("3.1 Task B1 &mdash; Selection Sort")
P("Each pass scans the unsorted part of the array, finds the smallest remaining value and "
  "swaps it into the next sorted position. Totals for this array: <b>45 comparisons</b> "
  "(always n(n&minus;1)/2 = 45) and <b>7 swaps</b>.")
table([["Pass", "Smallest found", "Array state after the pass", "Comparisons so far", "Swaps so far"],
       ["Start", "&mdash;", "[17, 5, 23, 8, 14, 3, 11, 20, 6, 9]", "0", "0"],
       ["1", "3", "[<b>3</b> | 5, 23, 8, 14, 17, 11, 20, 6, 9]", "9", "1"],
       ["2", "5", "[3, <b>5</b> | 23, 8, 14, 17, 11, 20, 6, 9]", "17", "1"],
       ["3", "6", "[3, 5, <b>6</b> | 8, 14, 17, 11, 20, 23, 9]", "24", "2"]],
      [14 * mm, 22 * mm, 82 * mm, 26 * mm, 21 * mm])
P("The bar marks the boundary between the sorted prefix and the unsorted remainder. In pass 2 "
  "the value 5 was already in the correct position, so no swap was performed &mdash; but the "
  "8 comparisons of that pass still had to be made, which is why Selection Sort cannot benefit "
  "from partially sorted data.")

H2("3.2 Task B2 &mdash; Insertion Sort")
P("Each pass takes the next value (the key), shifts every larger value in the sorted prefix "
  "one place to the right, and drops the key into the gap. Totals for this array: "
  "<b>32 comparisons</b> and <b>25 shifts</b>.")
table([["Pass", "Key", "Array state after the pass", "Shifts in pass", "Comparisons so far", "Shifts so far"],
       ["Start", "&mdash;", "[17, 5, 23, 8, 14, 3, 11, 20, 6, 9]", "&mdash;", "0", "0"],
       ["1", "5", "[5, 17 | 23, 8, 14, 3, 11, 20, 6, 9]", "1", "1", "1"],
       ["2", "23", "[5, 17, 23 | 8, 14, 3, 11, 20, 6, 9]", "0", "2", "1"],
       ["3", "8", "[5, 8, 17, 23 | 14, 3, 11, 20, 6, 9]", "2", "5", "3"]],
      [13 * mm, 13 * mm, 74 * mm, 21 * mm, 24 * mm, 20 * mm])
P("Pass 2 is the informative one: 23 is already larger than everything before it, so a single "
  "comparison ends the pass with no shifting. This early exit is what gives Insertion Sort its "
  "O(n) best case on sorted and almost-sorted data, confirmed experimentally in Part C.")
shot("10_partB_selection_insertion.png",
     "Figure 5 &mdash; Tasks B1 and B2: program output showing the first three passes and the final comparison and movement counts.")

A(PageBreak())
H2("3.3 Task B3 &mdash; Merge Sort")
P("Merge Sort repeatedly divides the array in half until each piece holds a single element, "
  "then merges the sorted pieces back together in order. Totals: <b>23 comparisons</b> and "
  "<b>34 merge moves</b>.")
H3("Base case")
P("<b>A sub-array of length 0 or 1 is already sorted, so the recursion stops and returns "
  "immediately</b> (in code: <font name='%s' size='8.5'>if (low &gt;= high) return;</font>). "
  "Every branch of the tree below ends in such a single-element array." % MONO)
H3("Complete divide-and-merge process")
code("""
                          [17, 5, 23, 8, 14, 3, 11, 20, 6, 9]
                                         |
              DIVIDE ----------------------------------------------
              |                                                  |
     [17, 5, 23, 8, 14]                                 [3, 11, 20, 6, 9]
             |                                                   |
     -----------------                                  -------------------
     |               |                                  |                 |
 [17, 5, 23]      [8, 14]                          [3, 11, 20]          [6, 9]
     |               |                                  |                 |
  --------        --------                           --------          --------
  |      |        |      |                           |      |          |      |
[17, 5] [23]     [8]    [14]                      [3, 11]  [20]       [6]    [9]
  |                                                   |
 ----                                                ----
 |  |                                                |  |
[17][5]   <-- BASE CASE                             [3][11]   <-- BASE CASE

                                 MERGE UPWARDS
[17] + [5]        -> [5, 17]                    [3] + [11]      -> [3, 11]
[5,17] + [23]     -> [5, 17, 23]                [3,11] + [20]   -> [3, 11, 20]
[8] + [14]        -> [8, 14]                    [6] + [9]       -> [6, 9]
[5,17,23]+[8,14]  -> [5, 8, 14, 17, 23]         [3,11,20]+[6,9] -> [3, 6, 9, 11, 20]

              [5, 8, 14, 17, 23]  +  [3, 6, 9, 11, 20]
                              |
                              v
              [3, 5, 6, 8, 9, 11, 14, 17, 20, 23]      <-- fully sorted
""", 6.8)

H2("3.4 Task B4 &mdash; Quick Sort")
P("<b>Pivot-selection rule: the last element of the current sub-array</b> (Lomuto "
  "partitioning). Values less than or equal to the pivot are moved to the left of it, larger "
  "values stay to its right, and the pivot is then placed in its final position between the two "
  "partitions. Totals: <b>20 comparisons</b> and <b>12 swaps</b>.")
table([["Stage", "Sub-array (indices)", "Pivot", "Left partition (&le; pivot)", "Right partition (&gt; pivot)", "Array after the stage"],
       ["1", "[17, 5, 23, 8, 14, 3, 11, 20, 6, 9] (0&ndash;9)", "<b>9</b> (last)", "[5, 8, 3, 6]",
        "[23, 11, 20, 17, 14]", "[5, 8, 3, 6, <b>9</b>, 23, 11, 20, 17, 14]"],
       ["2", "[5, 8, 3, 6] (0&ndash;3)", "<b>6</b> (last)", "[5, 3]", "[8]",
        "[5, 3, <b>6</b>, 8, 9, 23, 11, 20, 17, 14]"]],
      [13 * mm, 44 * mm, 17 * mm, 26 * mm, 30 * mm, 35 * mm])
P("After stage 1 the pivot 9 is at index 4 and will never move again; the algorithm then "
  "recurses into the left partition (indices 0&ndash;3) and later the right partition "
  "(indices 5&ndash;9). The base case is again a sub-array of 0 or 1 element.")
shot("11_partB_merge_quick.png",
     "Figure 6 &mdash; Tasks B3 and B4: the merge-sort divide/merge trace with the base cases marked, and the first two Quick Sort partitioning stages.")

# ======================= PART C =======================
A(PageBreak())
H1("4. Part C &mdash; Algorithm Experiment")
H2("4.1 Method")
bullets([
    "Test values are generated programmatically in the range 1&ndash;999 using a reproducible "
    "generator with a fixed seed (2026), so the tables below can be reproduced exactly.",
    "For each input size one original array is generated, and every algorithm is given its own "
    "copy of exactly the same values, so the comparison is fair.",
    "Only comparisons between data values are counted; loop-index and boundary tests are not.",
    "<font name='%s' size='8.5'>System.nanoTime()</font> is read immediately before and "
    "immediately after the sorting call only, so array generation, copying and printing are "
    "excluded from the measured time." % MONO,
])
H2("4.2 Results &mdash; random arrays")
rows = [["Algorithm", "Input Size", "Number of Comparisons", "Execution Time (ns)"],
        ["Selection Sort", "20", "190", "7 919"],
        ["Insertion Sort", "20", "90", "6 974"],
        ["Merge Sort", "20", "68", "13 299"],
        ["Quick Sort", "20", "81", "7 211"],
        ["Selection Sort", "50", "1 225", "30 513"],
        ["Insertion Sort", "50", "652", "19 446"],
        ["Merge Sort", "50", "221", "31 005"],
        ["Quick Sort", "50", "271", "14 852"],
        ["Selection Sort", "100", "4 950", "109 052"],
        ["Insertion Sort", "100", "2 554", "73 402"],
        ["Merge Sort", "100", "548", "65 349"],
        ["Quick Sort", "100", "705", "31 024"],
        ["Selection Sort", "500", "124 750", "2 589 246"],
        ["Insertion Sort", "500", "61 625", "1 704 529"],
        ["Merge Sort", "500", "3 861", "403 080"],
        ["Quick Sort", "500", "4 878", "203 526"]]
table(rows, [48 * mm, 30 * mm, 45 * mm, 42 * mm], align_right=(1, 2, 3))
H2("4.3 Results &mdash; almost-sorted 100-element array")
P("The 100-element array was first sorted into ascending order and then five pairs of "
  "neighbouring values were swapped (at indices 10/11, 25/26, 40/41, 60/61 and 80/81). "
  "All four algorithms were given the same almost-sorted array.")
table([["Algorithm", "Input Size", "Number of Comparisons", "Execution Time (ns)"],
       ["Selection Sort", "100 (almost sorted)", "4 950", "99 104"],
       ["Insertion Sort", "100 (almost sorted)", "104", "4 198"],
       ["Merge Sort", "100 (almost sorted)", "357", "57 145"],
       ["Quick Sort", "100 (almost sorted)", "4 735", "106 823"]],
      [48 * mm, 40 * mm, 40 * mm, 37 * mm], align_right=(2, 3))
P("Compared with the random 100-element array, Insertion Sort fell from 2 554 comparisons to "
  "104 (a 96% reduction), Merge Sort fell slightly from 548 to 357, Selection Sort was "
  "unchanged at 4 950, and Quick Sort rose sharply from 705 to 4 735.")
shot("09_partC_experiment.png",
     "Figure 7 &mdash; Part C: the experiment output produced by the program, including the almost-sorted test.", max_h=150 * mm)

A(PageBreak())
H2("4.4 Answers to the Part C questions")
H3("1. Which algorithm performed the fewest comparisons?")
P("Merge Sort, in almost every case. On the random arrays it needed 68 (n=20), 221 (n=50), "
  "548 (n=100) and 3 861 (n=500) comparisons &mdash; the lowest at every size except n=20, where "
  "it was already lowest as well. On the almost-sorted array the fewest was Insertion Sort "
  "with only 104 comparisons, because that input is its best case.")
H3("2. Which algorithm performed the most comparisons?")
P("Selection Sort, at every input size (190, 1 225, 4 950 and 124 750). Its comparison count "
  "is fixed at n(n&minus;1)/2 regardless of how the data is arranged, so it can never do "
  "better than its worst case. On the almost-sorted array Quick Sort came close to it "
  "(4 735 versus 4 950) for the reason explained in question 3.")
H3("3. Which algorithm performed best on the almost-sorted array?")
P("Insertion Sort, by a very wide margin: 104 comparisons and about 4 200 ns, against 357 for "
  "Merge Sort, 4 950 for Selection Sort and 4 735 for Quick Sort. Each key needs only one "
  "comparison when it is already larger than its predecessor, so the inner loop exits "
  "immediately and the algorithm approaches its O(n) best case. Quick Sort, by contrast, "
  "degraded badly: with the last element as pivot, a nearly sorted array gives extremely "
  "unbalanced partitions, which drives it towards its O(n&sup2;) worst case.")
H3("4. Which algorithm appeared to scale best as the input became larger?")
P("Merge Sort scaled best and most predictably. Going from 100 to 500 elements (five times the "
  "data), its comparisons grew about 7-fold (548 to 3 861), close to the n log n prediction, "
  "while Selection Sort grew 25-fold (4 950 to 124 750) and Insertion Sort 24-fold, both "
  "matching the n&sup2; prediction. Quick Sort scaled almost as well as Merge Sort on random "
  "data (705 to 4 878) and had the fastest measured time at n=500, but it is not as reliable "
  "because its performance depends on the pivot happening to split the data evenly.")
H3("5. Did the experimental results generally agree with the theoretical time complexity?")
P("Yes. Selection Sort's counts were exactly n(n&minus;1)/2 &mdash; 190, 1 225, 4 950 and "
  "124 750 &mdash; confirming the O(n&sup2;) prediction in all cases. Insertion Sort averaged roughly "
  "n&sup2;/4 comparisons on random data (2 554 for n=100) and collapsed to about n on the "
  "almost-sorted array, matching its O(n&sup2;) average and O(n) best case. Merge Sort stayed "
  "near n log n in every test (3 861 against a predicted 4 483 for n=500), confirming "
  "O(n log n) in all cases. Quick Sort matched O(n log n) on random data but rose towards "
  "O(n&sup2;) on the almost-sorted array, which is the documented worst case for a last-element "
  "pivot. The one apparent disagreement is at n=20, where Merge Sort had the fewest comparisons "
  "but the slowest time (13 299 ns); that is the constant overhead of recursion and of "
  "allocating temporary arrays, which dominates on tiny inputs, plus JIT warm-up at the start "
  "of a run.")
H3("6. Is execution time alone enough to decide which algorithm is better?")
P("No. Execution time is machine- and run-dependent: it is affected by CPU speed and load, by "
  "the Java JIT compiler warming up during the run, by garbage collection and by cache "
  "behaviour, which is why Merge Sort was slowest at n=20 despite doing the fewest "
  "comparisons. Comparison counts are deterministic and reproducible, so they show the "
  "algorithm's actual work. A sound choice also weighs other factors: memory use (Merge Sort "
  "needs O(n) extra space, the other three sort in place), stability (Insertion and Merge Sort "
  "are stable, Selection and Quick Sort are not), worst-case guarantees (Merge Sort guarantees "
  "O(n log n); Quick Sort does not), behaviour on the data actually expected, and code "
  "simplicity. Time should be read together with comparison counts and complexity analysis, "
  "never on its own.")

# ======================= PART D =======================
A(PageBreak())
H1("5. Part D &mdash; Integrated Service-Centre System")
P("The queue, the singly linked list, the array statistics and the four sorting algorithms all "
  "run inside one program, <font name='%s' size='8.5'>ServiceCentreApp.java</font>. The four "
  "students from the brief are pre-loaded at start-up so every option can be exercised "
  "immediately. Serving a student (option 2) also appends that student's service time to the "
  "statistics array, which is what option 8 reports on and option 9 sorts &mdash; so the "
  "components genuinely interoperate rather than merely coexisting. The postfix stack exercise "
  "remains separate, as the brief requires." % MONO)
table([["Menu option", "Structure / operation invoked", "How it works"],
       ["1. Add student to waiting queue", "Queue &mdash; enqueue", "A new node is linked behind the rear pointer; O(1)."],
       ["2. Serve next student", "Queue &mdash; peek + dequeue", "peek() shows who is next, dequeue() advances the front pointer, and the service time is recorded in the array."],
       ["3. Display waiting students", "Queue &mdash; traversal", "Walks from front to rear printing each node, and draws the queue diagram."],
       ["4. Add student service record", "Linked list &mdash; insertStudent()", "Inserts at the beginning, at the end or at a chosen position by re-pointing next references."],
       ["5. Display student service records", "Linked list &mdash; traversal", "Follows next from the head to NULL, printing each node."],
       ["6. Search for student record", "Linked list &mdash; search", "Sequential search by student number; reports the node position and the number of comparisons."],
       ["7. Remove student record", "Linked list &mdash; deletion", "Finds the predecessor and points it past the target node; prints the list before and after."],
       ["8. Display daily statistics", "Array processing", "One traversal of the service-time array computes all six statistics."],
       ["9. Sort service times", "Selection / Insertion / Merge / Quick", "Copies the service times out of the linked list into an array and sorts the chosen way, reporting comparisons, movements and time."],
       ["10. Run sorting experiment", "Sorting experiment", "Runs the complete Part C experiment, including the almost-sorted test."],
       ["11. Exit", "&mdash;", "Ends the program."]],
      [42 * mm, 42 * mm, 81 * mm])
shot("01_menu_option3_queue.png",
     "Figure 8 &mdash; the integrated menu, and option 3 displaying the waiting queue by traversal.", max_h=120 * mm)
shot("03_option4_5_linkedlist.png",
     "Figure 9 &mdash; options 4 and 5: a record is inserted at the beginning of the linked list, then the whole list is traversed.")
shot("04_option6_7_search_delete.png",
     "Figure 10 &mdash; options 6 and 7: searching for student 223041876 (found at node 4 after 4 comparisons) and deleting record 222034512, with the list shown before and after.")
shot("05_option9_sort.png",
     "Figure 11 &mdash; option 9: the service times held in the linked list are sorted with Merge Sort, with comparisons, movements and execution time reported.")

# ======================= PART E =======================
A(PageBreak())
H1("6. Part E &mdash; Pseudocode and Algorithm Representation")
P("The pseudocode below corresponds directly to the submitted Java implementation; the file "
  "and method that implements each algorithm is named in the heading. The complete source "
  "code is in the <font name='%s' size='8.5'>src/</font> folder of the submission and is not "
  "reproduced in this report." % MONO)

H2("6.1 Queue")
H3("enqueue(student) &mdash; StudentQueue.enqueue()")
code("""
ALGORITHM enqueue(student)
1.  newNode <- new QNode holding student;  newNode.next <- NULL
2.  IF front = NULL THEN                  // the queue is empty
3.      front <- newNode;  rear <- newNode
4.  ELSE
5.      rear.next <- newNode              // link behind the current last node
6.      rear      <- newNode              // the new node becomes the rear
7.  END IF
8.  size <- size + 1
END                                        Time complexity: O(1)
""")
H3("dequeue() &mdash; StudentQueue.dequeue()")
code("""
ALGORITHM dequeue()
1.  IF front = NULL THEN PRINT "queue is empty"; RETURN NULL
2.  served <- front.data
3.  front  <- front.next                  // move the front pointer forward
4.  IF front = NULL THEN rear <- NULL     // the queue has just become empty
5.  size <- size - 1
6.  RETURN served
END                                        Time complexity: O(1)
""")

H2("6.2 Stack and postfix evaluation")
H3("push(value) and pop() &mdash; IntStack")
code("""
ALGORITHM push(value)
1.  IF top = capacity - 1 THEN            // the backing array is full
2.      bigger <- new array of size capacity * 2
3.      FOR i <- 0 TO capacity - 1 DO bigger[i] <- items[i] END FOR
4.      items <- bigger
5.  END IF
6.  top <- top + 1;  items[top] <- value
END

ALGORITHM pop()
1.  IF top = -1 THEN ERROR "stack underflow"
2.  value <- items[top];  top <- top - 1
3.  RETURN value
END

ALGORITHM peek()
1.  IF top = -1 THEN ERROR "stack is empty"
2.  RETURN items[top]
END
""")
H3("evaluatePostfix(expression) &mdash; PostfixEvaluator.evaluate()")
code("""
ALGORITHM evaluatePostfix(expression)
1.  CREATE empty stack S
2.  tokens <- split expression on spaces
3.  FOR EACH token IN tokens DO
4.      IF token is a number THEN
5.          S.push(token as number)
6.      ELSE                              // token is +, -, * or /
7.          IF S.size < 2 THEN ERROR "malformed expression"
8.          right <- S.pop()              // the second operand is popped first
9.          left  <- S.pop()
10.         S.push( apply(left, token, right) )
11.     END IF
12. END FOR
13. IF S.size <> 1 THEN ERROR "malformed expression"
14. answer <- S.peek()
15. RETURN S.pop()
END                                        Time complexity: O(n) tokens
""")

A(PageBreak())
H2("6.3 Singly linked list")
H3("insertNode &mdash; beginning, end and specified position")
code("""
ALGORITHM insertAtBeginning(student)
1.  newNode <- new Node holding student
2.  newNode.next <- head                  // point at the old first node
3.  head <- newNode
4.  count <- count + 1
END                                        O(1)

ALGORITHM insertAtEnd(student)
1.  newNode <- new Node holding student
2.  IF head = NULL THEN head <- newNode
3.  ELSE
4.      current <- head
5.      WHILE current.next <> NULL DO current <- current.next END WHILE
6.      current.next <- newNode
7.  END IF
8.  count <- count + 1
END                                        O(n)

ALGORITHM insertAtPosition(student, position)        // position is 1-based
1.  IF position < 1 OR position > count + 1 THEN PRINT "invalid"; RETURN FALSE
2.  IF position = 1 THEN insertAtBeginning(student); RETURN TRUE
3.  newNode <- new Node holding student
4.  current <- head
5.  FOR i <- 1 TO position - 2 DO current <- current.next END FOR
6.  newNode.next <- current.next           // link to the rest of the list
7.  current.next <- newNode                // link the predecessor to the new node
8.  count <- count + 1;  RETURN TRUE
END                                        O(n)
""")
H3("deleteNode(studentNo) &mdash; ServiceRecordList.deleteStudent()")
code("""
ALGORITHM deleteNode(studentNo)
1.  IF head = NULL THEN PRINT "list is empty"; RETURN FALSE
2.  IF head.data.studentNo = studentNo THEN          // deleting the head
3.      head <- head.next;  count <- count - 1;  RETURN TRUE
4.  END IF
5.  previous <- head;  current <- head.next
6.  WHILE current <> NULL DO
7.      IF current.data.studentNo = studentNo THEN
8.          previous.next <- current.next            // bypass the target node
9.          count <- count - 1;  RETURN TRUE
10.     END IF
11.     previous <- current;  current <- current.next
12. END WHILE
13. PRINT "student not found";  RETURN FALSE
END                                        O(n)
""")
H3("searchNode(studentNo) and traverseList()")
code("""
ALGORITHM searchNode(studentNo)            // sequential (linear) search
1.  current <- head;  position <- 1
2.  WHILE current <> NULL DO
3.      IF current.data.studentNo = studentNo THEN
4.          PRINT "found at node", position;  RETURN current.data
5.      END IF
6.      current <- current.next;  position <- position + 1
7.  END WHILE
8.  PRINT "not found";  RETURN NULL
END                                        O(n)

ALGORITHM traverseList()
1.  current <- head;  position <- 1
2.  WHILE current <> NULL DO
3.      PRINT position, current.data.studentNo, name, serviceType, estimatedTime
4.      current <- current.next;  position <- position + 1
5.  END WHILE
6.  PRINT "total records =", count
END                                        O(n)
""")

A(PageBreak())
H2("6.4 Array statistics &mdash; DailyStatistics")
code("""
ALGORITHM computeDailyStatistics(serviceTimes, n)
1.  total <- 0;  served <- 0;  longerThanTen <- 0
2.  highest <- serviceTimes[0];  lowest <- serviceTimes[0]
3.  FOR i <- 0 TO n - 1 DO
4.      served <- served + 1
5.      total  <- total + serviceTimes[i]
6.      IF serviceTimes[i] > highest THEN highest <- serviceTimes[i]
7.      IF serviceTimes[i] < lowest  THEN lowest  <- serviceTimes[i]
8.      IF serviceTimes[i] > 10      THEN longerThanTen <- longerThanTen + 1
9.  END FOR
10. average <- total / served
11. RETURN served, total, average, highest, lowest, longerThanTen
END                     One traversal, O(n). No built-in max, min or sum is used.
""")
H2("6.5 Sorting")
H3("selectionSort(A) &mdash; Sorters.selectionSort()")
code("""
ALGORITHM selectionSort(A, n)
1.  FOR i <- 0 TO n - 2 DO
2.      minIndex <- i
3.      FOR j <- i + 1 TO n - 1 DO
4.          comparisons <- comparisons + 1
5.          IF A[j] < A[minIndex] THEN minIndex <- j
6.      END FOR
7.      IF minIndex <> i THEN
8.          SWAP A[i] WITH A[minIndex];  swaps <- swaps + 1
9.      END IF
10. END FOR
END        Comparisons always n(n-1)/2;  best = average = worst = O(n^2)
""")
H3("insertionSort(A) &mdash; Sorters.insertionSort()")
code("""
ALGORITHM insertionSort(A, n)
1.  FOR i <- 1 TO n - 1 DO
2.      key <- A[i];  j <- i - 1
3.      WHILE j >= 0 DO
4.          comparisons <- comparisons + 1
5.          IF A[j] > key THEN
6.              A[j + 1] <- A[j]           // shift the larger value right
7.              shifts <- shifts + 1;  j <- j - 1
8.          ELSE
9.              EXIT WHILE                 // correct position found
10.         END IF
11.     END WHILE
12.     A[j + 1] <- key
13. END FOR
END        Best O(n) on (almost) sorted data;  average and worst O(n^2)
""")
H3("mergeSort(A, low, high) &mdash; Sorters.mergeSort()")
code("""
ALGORITHM mergeSort(A, low, high)
1.  IF low >= high THEN RETURN            // BASE CASE: 0 or 1 element is sorted
2.  mid <- low + (high - low) / 2
3.  mergeSort(A, low, mid)                // divide the left half
4.  mergeSort(A, mid + 1, high)           // divide the right half
5.  merge(A, low, mid, high)              // conquer: combine the sorted halves
END

ALGORITHM merge(A, low, mid, high)
1.  L <- copy of A[low .. mid];  R <- copy of A[mid + 1 .. high]
2.  i <- 0;  j <- 0;  k <- low
3.  WHILE i < length(L) AND j < length(R) DO
4.      comparisons <- comparisons + 1
5.      IF L[i] <= R[j] THEN A[k] <- L[i];  i <- i + 1
6.      ELSE                 A[k] <- R[j];  j <- j + 1
7.      END IF
8.      k <- k + 1
9.  END WHILE
10. WHILE i < length(L) DO A[k] <- L[i];  i <- i + 1;  k <- k + 1 END WHILE
11. WHILE j < length(R) DO A[k] <- R[j];  j <- j + 1;  k <- k + 1 END WHILE
END        O(n log n) in every case;  needs O(n) extra memory
""")
H3("quickSort(A, low, high) &mdash; Sorters.quickSort()")
code("""
ALGORITHM quickSort(A, low, high)
1.  IF low >= high THEN RETURN            // BASE CASE: 0 or 1 element
2.  p <- partition(A, low, high)
3.  quickSort(A, low, p - 1)              // left partition (values <= pivot)
4.  quickSort(A, p + 1, high)             // right partition (values > pivot)
END

ALGORITHM partition(A, low, high)         // Lomuto scheme
PIVOT RULE: the LAST element of the sub-array, A[high]
1.  pivot <- A[high];  i <- low - 1
2.  FOR j <- low TO high - 1 DO
3.      comparisons <- comparisons + 1
4.      IF A[j] <= pivot THEN
5.          i <- i + 1
6.          IF i <> j THEN SWAP A[i] WITH A[j];  swaps <- swaps + 1
7.      END IF
8.  END FOR
9.  SWAP A[i + 1] WITH A[high]            // pivot into its final position
10. swaps <- swaps + 1
11. RETURN i + 1
END        Average O(n log n);  worst O(n^2) on (almost) sorted input
""")

# ======================= CLOSING =======================
A(PageBreak())
H1("7. Conclusion")
P("The project shows that the choice of a data structure or algorithm follows from the "
  "operations a task actually performs. A queue enforces first-come-first-served service at "
  "O(1) per student; a singly linked list absorbs insertions and deletions in the middle of "
  "the service records without shifting data; a stack evaluates postfix expressions in one "
  "pass because the operands needed are always the most recent values; and an array gives the "
  "contiguous, index-addressable storage that statistics and in-place sorting require.")
P("The experiment confirmed the theory taught in class. Selection Sort's comparison count was "
  "exactly n(n&minus;1)/2 at every size and never benefited from ordered data. Insertion Sort "
  "matched O(n&sup2;) on random data but collapsed to near O(n) on the almost-sorted array. "
  "Merge Sort held to O(n log n) in every test and scaled best, at the cost of O(n) extra "
  "memory. Quick Sort was the fastest on large random arrays but degraded towards O(n&sup2;) "
  "on almost-sorted input because of the last-element pivot rule &mdash; a concrete reminder "
  "that an algorithm's average case is not a guarantee, and that execution time on its own is "
  "not a sufficient basis for choosing one.")
H2("Repository and submission")
table([["Item", "Detail"],
       ["GitHub repository", f'<a href="{REPO_URL}" color="#01696F">{REPO_URL}</a>'],
       ["eLearning submission", "DSA521S_Group11_Project2026.zip (report PDF, all source files, README)"],
       ["Submitted by", "225018497 &ndash; George Shimaneni"],
       ["Contents of the repository", "src/ Java source files, README.md, PSEUDOCODE.md, "
        "screenshots/, captured program output, and this report"]],
      [42 * mm, 123 * mm])
P("The repository history records the progressive development of the solution as a series of "
  "commits, each describing the component added at that step, and every group member commits "
  "under their own GitHub account. "
  "Every member "
  "understands the complete submitted work and can explain, trace and defend any data "
  "structure, algorithm, pseudocode listing or section of source code in it.")

# ======================= BUILD =======================
OUT = os.path.join(BASE, "DSA521S_Group11_Project_Report.pdf")


def decorate(canv, doc):
    canv.saveState()
    if doc.page > 1:
        canv.setFont(BODY, 7.6)
        canv.setFillColor(MUTED)
        canv.drawString(20 * mm, 12 * mm, "DSA521S Group Mini-Project 2026 \u2014 Group 11 \u2014 NUST Service Centre Simulation")
        canv.drawRightString(190 * mm, 12 * mm, "Page %d" % doc.page)
        canv.setStrokeColor(LINE)
        canv.setLineWidth(0.4)
        canv.line(20 * mm, 15.5 * mm, 190 * mm, 15.5 * mm)
    canv.restoreState()


doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=20 * mm, rightMargin=25 * mm,
                      topMargin=18 * mm, bottomMargin=20 * mm,
                      title="DSA521S Group 11 Project Report - NUST Service Centre Simulation",
                      author="Perplexity Computer")
frame = Frame(20 * mm, 20 * mm, 165 * mm, A4[1] - 38 * mm, id="f")
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=decorate)])
doc.build(story)
print("wrote", OUT)
