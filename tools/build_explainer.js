const fs = require('fs');
const docx = require('docx');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, WidthType, ShadingType, BorderStyle, Footer, PageNumber,
        ExternalHyperlink, HeadingLevel } = docx;

const REPO = 'https://github.com/georgeshimaneni23-beep/DSA521S-Group11-ServiceCentre';
const TEAL = '01696F';
const BORDER = { style: BorderStyle.SINGLE, size: 4, color: 'D4D1CA' };
const BORDERS = { top: BORDER, bottom: BORDER, left: BORDER, right: BORDER,
                  insideHorizontal: BORDER, insideVertical: BORDER };

const P = (text, opts = {}) => new Paragraph({
  spacing: { after: opts.after === undefined ? 140 : opts.after, line: 300 },
  alignment: opts.align,
  children: [new TextRun({ text, bold: opts.bold, italics: opts.italics,
                           size: opts.size || 22, color: opts.color || '28251D' })],
});

const H1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 320, after: 160 },
  children: [new TextRun({ text, bold: true, size: 30, color: TEAL })],
});

const H2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 240, after: 120 },
  children: [new TextRun({ text, bold: true, size: 24, color: '28251D' })],
});

const BULLET = (text) => new Paragraph({
  bullet: { level: 0 }, spacing: { after: 90, line: 300 },
  children: [new TextRun({ text, size: 22, color: '28251D' })],
});

const cell = (text, { head = false, bold = false, width } = {}) => new TableCell({
  width: width ? { size: width, type: WidthType.DXA } : undefined,
  shading: head ? { type: ShadingType.CLEAR, fill: TEAL } : undefined,
  margins: { top: 90, bottom: 90, left: 120, right: 120 },
  children: [new Paragraph({
    spacing: { after: 0, line: 280 },
    children: [new TextRun({ text, bold: head || bold, size: 20,
                             color: head ? 'FFFFFF' : '28251D' })],
  })],
});

const table = (rows, widths) => new Table({
  width: { size: 9026, type: WidthType.DXA },
  borders: BORDERS,
  rows: rows.map((r, i) => new TableRow({
    tableHeader: i === 0,
    cantSplit: true,
    children: r.map((c, j) => cell(c, { head: i === 0, width: widths[j] })),
  })),
});

const doc = new Document({
  creator: 'Perplexity Computer',
  title: 'DSA521S Group 11 Mini-Project — Plain-Language Explanation',
  styles: { default: { document: { run: { font: 'Calibri', size: 22 } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 },
                          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: 'DSA521S Group 11 — project explanation — page ', size: 16, color: '7A7974' }),
                 new TextRun({ children: [PageNumber.CURRENT], size: 16, color: '7A7974' })],
    })] }) },
    children: [

  new Paragraph({ spacing: { after: 60 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'DSA521S — DATA STRUCTURES AND ALGORITHMS 1', size: 20, color: '7A7974' })] }),
  new Paragraph({ spacing: { after: 80 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'Group 11 Mini-Project 2026', bold: true, size: 40, color: '28251D' })] }),
  new Paragraph({ spacing: { after: 320 }, alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: 'What we built, how we built it, and what we used — in plain language', size: 24, color: TEAL })] }),

  P('This document is a simple, non-technical companion to the formal project report. It explains the project in everyday terms so that anyone reading it — including a group member revising for a defence — can follow what was done and why.'),

  H1('1. What the project is'),
  P('Our task was to build a small Java program that simulates a normal working day at the NUST campus student service centre, and then to use that program to study how different ways of storing and sorting data actually behave.'),
  P('In the simulation, students arrive at the service centre for things like registration, fee enquiries, student-card replacement, academic enquiries and document collection. They join one waiting line, they are helped in the order they arrived, a permanent record is kept for each of them, and at the end the day\'s service times are analysed and sorted.'),
  P('The point of the project is not the service centre itself. The service centre is simply a realistic story that gives us a reason to use four different data structures and four different sorting algorithms, and to prove — with measurements, not opinions — which one suits which job.'),

  H2('The four data structures and what each one does for us'),
  table([
    ['Structure', 'What it does in our program', 'Why we chose it, simply put'],
    ['Queue', 'Holds the students waiting to be helped.', 'A queue only lets you join at the back and leave from the front, so nobody can jump the line. First come, first served is built into the structure itself.'],
    ['Singly linked list', 'Keeps the service record of every student.', 'We do not know in advance how many students will come. A linked list just adds one more link in the chain, and removing a record in the middle only means re-pointing one arrow instead of moving everything.'],
    ['Stack', 'Works out postfix sums such as "5 3 + 2 *".', 'A stack always gives you back the most recent thing you put on it, and that is exactly the pair of numbers an operator needs. This part is a separate exercise and is deliberately not in the main menu.'],
    ['Array', 'Stores the service times of everyone who was helped.', 'An array is a plain numbered block of values, so one loop through it gives us the total, average, highest, lowest and the count over 10 minutes.'],
  ], [1400, 3400, 4226]),

  H2('The four sorting algorithms'),
  P('We sort service times four different ways so we can compare them fairly: Selection Sort, Insertion Sort, Merge Sort and Quick Sort. Every one of them was written out by hand. We did not use Java\'s built-in sorting, and we did not use Java\'s ready-made Queue, Stack or LinkedList either — the brief forbids all of that, and writing them ourselves is the whole point of the module.'),

  H1('2. How we did it'),
  P('We worked through the brief in the same order it is written, and we tested each piece before moving to the next one.'),
  BULLET('Step 1 — We wrote a small Student class first. It simply holds one student\'s number, name, service type and estimated service time. Everything else in the program passes these objects around.'),
  BULLET('Step 2 — We built the queue, then the linked list, then the stack, then the statistics array, each in its own file, each with a short test to prove it worked. Six students were added to the queue and three were served, exactly as the brief asks, and we printed the line before and after so the effect is visible.'),
  BULLET('Step 3 — We wrote the four sorting algorithms and added counters inside them. Every time two data values are compared, a counter goes up by one; every time a value is moved or swapped, another counter goes up. This is what lets us make real measurements instead of guessing.'),
  BULLET('Step 4 — We ran the experiment. The program generates lists of 20, 50, 100 and 500 random values and gives every algorithm its own identical copy, so the comparison is fair. We time only the sorting call itself, using System.nanoTime(), so generating and printing the data does not pollute the result. We then repeated the test on an almost-sorted list of 100 values to see which algorithms benefit from data that is nearly in order.'),
  BULLET('Step 5 — We joined everything into one menu-driven program with eleven options, so the parts genuinely work together: serving a student from the queue records that student\'s service time in the statistics array, which is the same array the statistics option reports on and the sorting option sorts.'),
  BULLET('Step 6 — We captured the program\'s real output as screenshots, wrote the pseudocode for every algorithm, and assembled the report. Everything quoted in the report is actual output from the program, not typed in by hand.'),

  H2('What we found — the short version'),
  BULLET('Selection Sort always does the same amount of work no matter how the data is arranged. It made the most comparisons every single time.'),
  BULLET('Insertion Sort is ordinary on random data but outstanding on almost-sorted data: its comparisons dropped from 2 554 to just 104, a 96% reduction.'),
  BULLET('Merge Sort was the most consistent and scaled the best as the lists got bigger, but it needs extra memory to do it.'),
  BULLET('Quick Sort was the fastest on large random lists, but it got much worse on the almost-sorted list. That is because we pick the last value as the pivot, which splits nearly-ordered data very unevenly.'),
  BULLET('Execution time on its own is misleading. Merge Sort made the fewest comparisons on the smallest list yet recorded the slowest time, because Java was still warming up. Comparison counts are the reliable measure.'),

  H1('3. What we used'),
  table([
    ['Item', 'Detail'],
    ['Language', 'Java, console based, no graphical interface'],
    ['Development', 'Compiled with javac and run from the command line'],
    ['Files written', '11 Java source files in the src/ folder'],
    ['Built-in helpers used', 'None for the assessed work — no Queue, Stack, LinkedList, sort(), max(), min() or sum(). Only basic printing and keyboard input.'],
    ['Version control', 'One GitHub repository with a commit for each component added'],
    ['Deliverables', 'Project report PDF, the Java source code, a README, a pseudocode file, and this explanation'],
  ], [2600, 6426]),

  H2('The eleven Java files, in one line each'),
  table([
    ['File', 'What it contains'],
    ['Student.java', 'One student\'s details: number, name, service type, service time.'],
    ['StudentQueue.java', 'The waiting line: enqueue, dequeue, peek, isEmpty and a display method.'],
    ['ServiceRecordList.java', 'The linked list of service records: insert at the beginning, end or a position, delete, search and traverse.'],
    ['IntStack.java', 'A stack of whole numbers with push, pop and peek.'],
    ['PostfixEvaluator.java', 'Uses the stack to work out postfix expressions, printing the stack after every step.'],
    ['DailyStatistics.java', 'The service-time array and the six statistics calculated from it with plain loops.'],
    ['ArrayUtil.java', 'Small helpers for copying and printing arrays by hand.'],
    ['Sorters.java', 'The four sorting algorithms, each counting its own comparisons and movements.'],
    ['SortingExperiment.java', 'Runs the whole Part C experiment and prints the results tables.'],
    ['ServiceCentreApp.java', 'The eleven-option menu that ties everything together.'],
    ['DemoRunner.java', 'Prints every demonstration and trace the brief asks for, in one go.'],
  ], [2600, 6426]),

  H1('4. How to run it'),
  P('Open a terminal in the project folder and compile everything first:'),
  new Paragraph({ spacing: { after: 100 }, shading: { type: ShadingType.CLEAR, fill: 'F2F1ED' },
    children: [new TextRun({ text: '  javac -d out src/*.java', font: 'Consolas', size: 20 })] }),
  P('Then run whichever part you want to see:'),
  new Paragraph({ spacing: { after: 20 }, shading: { type: ShadingType.CLEAR, fill: 'F2F1ED' },
    children: [new TextRun({ text: '  java -cp out ServiceCentreApp     (the interactive menu)', font: 'Consolas', size: 20 })] }),
  new Paragraph({ spacing: { after: 20 }, shading: { type: ShadingType.CLEAR, fill: 'F2F1ED' },
    children: [new TextRun({ text: '  java -cp out DemoRunner           (every demonstration and trace)', font: 'Consolas', size: 20 })] }),
  new Paragraph({ spacing: { after: 20 }, shading: { type: ShadingType.CLEAR, fill: 'F2F1ED' },
    children: [new TextRun({ text: '  java -cp out PostfixEvaluator     (the postfix stack exercise)', font: 'Consolas', size: 20 })] }),
  new Paragraph({ spacing: { after: 160 }, shading: { type: ShadingType.CLEAR, fill: 'F2F1ED' },
    children: [new TextRun({ text: '  java -cp out SortingExperiment    (the Part C experiment)', font: 'Consolas', size: 20 })] }),
  P('Java 8 or any newer version works.'),

  H1('5. Who we are'),
  table([
    ['#', 'Full name', 'Student number', 'Role'],
    ['1', 'George Shimaneni', '225018497', 'Group leader and submitter'],
    ['2', 'Dipundhi Paul Peter', '225058146', 'Member'],
    ['3', 'Mangulukeni Kayoko', '227074404', 'Member'],
    ['4', 'Nelumbu Rachel', '225049511', 'Member'],
    ['5', 'Enerist T Shilumbu', '222093951', 'Member'],
  ], [700, 3400, 2300, 2626]),

  new Paragraph({ spacing: { before: 200, after: 140 },
    children: [new TextRun({ text: 'Project repository: ', size: 22 }),
      new ExternalHyperlink({ link: REPO,
        children: [new TextRun({ text: REPO, size: 22, color: TEAL, underline: {} })] })] }),
  P('Submitted by: 225018497 – George Shimaneni', { bold: true }),
  P('Submission file: DSA521S_Group11_Project2026.zip', { after: 240 }),
  P('Every member of the group can explain, trace and defend any part of this work.', { italics: true }),

    ],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync('/home/user/workspace/DSA521S_Project/DSA521S_Group11_Project_Explained.docx', buf);
  console.log('wrote DSA521S_Group11_Project_Explained.docx');
});
