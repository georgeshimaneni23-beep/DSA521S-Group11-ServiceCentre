"""Renders captured console output into terminal-style PNG 'screenshots'
used as evidence in the project report."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/user/workspace/DSA521S_Project"
SHOTS = os.path.join(BASE, "screenshots")
os.makedirs(SHOTS, exist_ok=True)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
]
fp = next(p for p in FONT_PATHS if os.path.exists(p))
FONT = ImageFont.truetype(fp, 15)
FONT_B = ImageFont.truetype(fp, 15)

BG = (24, 23, 21)
FG = (222, 221, 219)
ACCENT = (79, 152, 163)
BAR = (46, 45, 43)
PAD = 16
LH = 20


def render(lines, out_name, title):
    lines = [l.rstrip("\n").replace("\t", "    ") for l in lines]
    width_chars = max([len(l) for l in lines] + [len(title) + 10, 60])
    char_w = FONT.getlength("M")
    w = int(PAD * 2 + char_w * width_chars) + 8
    h = PAD * 2 + LH * len(lines) + 34
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    # title bar
    d.rectangle([0, 0, w, 28], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([12 + i * 18, 9, 22 + i * 18, 19], fill=c)
    d.text((76, 6), title, font=FONT, fill=(170, 169, 166))
    y = 28 + PAD
    for l in lines:
        colour = FG
        s = l.strip()
        if s.startswith("===") or s.startswith("---") or s.startswith("Select option"):
            colour = ACCENT
        elif s.startswith("CAMPUS") or s.startswith("TASK") or s.startswith("PART"):
            colour = (232, 175, 52)
        d.text((PAD, y), l, font=FONT, fill=colour)
        y += LH
    img.save(os.path.join(SHOTS, out_name))
    print("wrote", out_name, img.size)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


demo = read(os.path.join(BASE, "demo_output.txt"))
menu = read(os.path.join(BASE, "menu_session.txt"))


def slice_between(lines, start_sub, end_sub, start_from=0, include_end=False):
    s = next(i for i in range(start_from, len(lines)) if start_sub in lines[i])
    e = next(i for i in range(s + 1, len(lines)) if end_sub in lines[i])
    return lines[s:e + (1 if include_end else 0)]


MENU_BLOCK = 16  # lines of the menu banner

# 1. Menu + option 3 (queue display)
i = menu.index("========================================")
shot1 = [("Select option: 3" if l.strip()=="Select option:" else l) for l in menu[i:i + 27]]
render(shot1, "01_menu_option3_queue.png",
       "Option 3 - Display waiting students (Queue traversal)")

# 2. Option 2 serve + option 8 statistics
s = next(i for i, l in enumerate(menu) if l.startswith("Next in line"))
serve = menu[s:s + 4]
t = next(i for i, l in enumerate(menu) if "DAILY STATISTICS" in l)
render(["Select option: 2", ""] + serve + ["", "Select option: 8", ""] + menu[t:t + 8],
       "02_option2_serve_option8_stats.png",
       "Options 2 and 8 - Queue dequeue and Array statistics")

# 3. Options 4 and 5 - linked list insert + display
s = next(i for i, l in enumerate(menu) if "Insert where?" in l)
blk = ["Select option: 4"] + menu[s - 1:s + 3]
t = next(i for i, l in enumerate(menu) if "STUDENT SERVICE RECORDS" in l)
render(blk + ["", "Select option: 5", ""] + menu[t:t + 9],
       "03_option4_5_linkedlist.png",
       "Options 4 and 5 - Linked list insertion and traversal")

# 4. Options 6 and 7 - search and delete
s = next(i for i, l in enumerate(menu) if l.startswith("Enter the student number to search"))
t = next(i for i, l in enumerate(menu) if l.startswith("Enter the student number to remove"))
render(["Select option: 6"] + menu[s:s + 3] + ["", "Select option: 7"] + menu[t:t + 4],
       "04_option6_7_search_delete.png",
       "Options 6 and 7 - Linked list search and deletion")

# 5. Option 9 - sorting service times
s = next(i for i, l in enumerate(menu) if l.startswith("Service times taken"))
render(["Select option: 9"] + menu[s:s + 5], "05_option9_sort.png",
       "Option 9 - Sorting the service times")

# 6. Postfix stack trace (Task A3)
s = next(i for i, l in enumerate(demo) if "TASK A3" in l) - 1
e = next(i for i, l in enumerate(demo) if l.startswith("Further checks")) + 5
render(demo[s:e], "06_taskA3_postfix_stack.png", "Task A3 - Postfix evaluation using a Stack")

# 7. Task A1 queue demo
s = next(i for i, l in enumerate(demo) if "TASK A1" in l) - 1
e = next(i for i, l in enumerate(demo) if l.startswith("WHY A QUEUE")) - 1
render(demo[s:e], "07_taskA1_queue_demo.png", "Task A1 - Six arrivals and three students served")

# 8. Task A2 linked list demo
s = next(i for i, l in enumerate(demo) if "TASK A2" in l) - 1
e = next(i for i, l in enumerate(demo) if l.startswith("4) displayStudents"))
render(demo[s:e], "08_taskA2_linkedlist_demo.png", "Task A2 - Linked list before and after link changes")

# 9. Part C experiment table
s = next(i for i, l in enumerate(demo) if "PART C" in l) - 1
e = next(i for i, l in enumerate(demo) if l.startswith("=== END"))
render(demo[s:e], "09_partC_experiment.png", "Part C - Sorting experiment results")

# 10. Part B traces
s = next(i for i, l in enumerate(demo) if "TASK B1" in l) - 1
e = next(i for i, l in enumerate(demo) if "TASK B3" in l) - 1
render(demo[s:e], "10_partB_selection_insertion.png", "Tasks B1 and B2 - Selection and Insertion Sort traces")

s = next(i for i, l in enumerate(demo) if "TASK B3" in l) - 1
e = next(i for i, l in enumerate(demo) if "PART C" in l) - 1
render(demo[s:e], "11_partB_merge_quick.png", "Tasks B3 and B4 - Merge Sort and Quick Sort traces")
