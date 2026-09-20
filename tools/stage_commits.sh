#!/usr/bin/env bash
# Builds the repository history as a series of meaningful commits instead of one
# bulk upload. Run from the project root:  bash tools/stage_commits.sh
set -e
cd "$(dirname "$0")/.."

git init -q 2>/dev/null || true
printf 'out/\n*.class\ntools/fonts/\n' > .gitignore

c() { git commit -q -m "$1"; echo "commit: $1"; }

# 1 - project skeleton
git add .gitignore README.md 2>/dev/null || true
git commit -q -m "Initial project setup: README and gitignore for DSA521S Group 11 mini-project" || true

# 2 - shared data holder
git add src/Student.java && c "Added Student class holding student number, name, service type and service time"

# 3 - Task A1
git add src/StudentQueue.java && c "Implemented Queue for the waiting line: enqueue, dequeue, peek, isEmpty, displayQueue (Task A1)"

# 4 - Task A2
git add src/ServiceRecordList.java && c "Implemented singly linked list for student service records with insert, delete, search and traversal (Task A2)"

# 5 - Task A3 stack
git add src/IntStack.java && c "Added array-based Stack with push, pop and peek for the postfix exercise (Task A3)"
git add src/PostfixEvaluator.java && c "Implemented postfix expression evaluation using the Stack, with step-by-step stack trace (Task A3)"

# 6 - helpers and Task A4
git add src/ArrayUtil.java && c "Added array helper methods for manual copying and printing (no built-in Arrays methods)"
git add src/DailyStatistics.java && c "Implemented Array-based daily statistics: total, average, highest, lowest and services over 10 minutes (Task A4)"

# 7 - Part B sorting
git add src/Sorters.java && c "Implemented Selection, Insertion, Merge and Quick Sort with comparison and movement counters (Part B)"

# 8 - Part C experiment
git add src/SortingExperiment.java && c "Added sorting experiment for input sizes 20, 50, 100 and 500 plus the almost-sorted test (Part C)"

# 9 - Part D integration
git add src/ServiceCentreApp.java && c "Integrated queue, linked list, array statistics and sorting into one menu-driven system (Part D)"

# 10 - demonstration runner
git add src/DemoRunner.java && c "Added DemoRunner that prints every required demonstration, diagram and trace"

# 11 - pseudocode
git add PSEUDOCODE.md && c "Added Part E pseudocode for queue, stack, linked list and the four sorting algorithms"

# 12 - captured output and evidence
git add demo_output.txt menu_session.txt screenshots tools 2>/dev/null || true
c "Added captured program output and console screenshots used as evidence"

# 13 - report
git add -A && c "Added project report PDF and final README with group details and run instructions"

echo
echo "History:"
git log --oneline
