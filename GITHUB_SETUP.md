# GitHub — what is already done, and what each member must still do

Repository: <https://github.com/georgeshimaneni23-beep/DSA521S-Group11-ServiceCentre>
Visibility: **public**, so the lecturer can open the link without an invitation.

## Already done

* The repository was created under George's account.
* All project files were pushed to the `main` branch.
* The history is **15 separate commits**, one per component, with meaningful messages such as
  `Implemented Queue for the waiting line: enqueue, dequeue, peek, isEmpty, displayQueue (Task A1)`
  and `Implemented Selection, Insertion, Merge and Quick Sort with comparison and movement counters (Part B)`.
  You can see them with `git log --oneline` or on the repository's commits page.

## Step 1 — Add the other four members as collaborators (George does this once)

1. Open the repository, then **Settings → Collaborators → Add people**.
2. Add the GitHub username (or the email tied to the GitHub account) of:
   * Dipundhi Paul Peter — 225058146
   * Mangulukeni Kayoko — 227074404
   * Nelumbu Rachel — 225049511
   * Enerist T Shilumbu — 222093951
3. Each member then accepts the invitation from the email GitHub sends them.

If anyone does not have a GitHub account yet, they must create one at <https://github.com/signup>
using their real name, so the marker can identify them.

## Step 2 — Every member makes at least one commit from their own account

The brief requires each member's contribution to be visible under their own identifiable account.
Each member runs this **on their own computer**, once:

```bash
git clone https://github.com/georgeshimaneni23-beep/DSA521S-Group11-ServiceCentre.git
cd DSA521S-Group11-ServiceCentre

# Use your OWN name and the email on your GitHub account, otherwise the commit
# will not be linked to you.
git config user.name  "Your Full Name"
git config user.email "your-github-email@example.com"
```

Then make a small, real contribution and commit it. Suggested split so that nobody's commit
is empty or meaningless:

| Member | Suggested contribution | Suggested commit message |
| --- | --- | --- |
| Dipundhi Paul Peter | Add comments explaining the enqueue/dequeue pointer changes in `src/StudentQueue.java` | `Documented the front and rear pointer changes in the queue operations` |
| Mangulukeni Kayoko | Add comments to the insert and delete methods in `src/ServiceRecordList.java` | `Documented the link changes in linked list insertion and deletion` |
| Nelumbu Rachel | Add comments to `src/Sorters.java` explaining where each comparison is counted | `Documented the comparison counters in the four sorting algorithms` |
| Enerist T Shilumbu | Add comments to `src/SortingExperiment.java` explaining the timing method | `Documented the nanoTime measurement method used in the Part C experiment` |

After editing, each member runs:

```bash
git add -A
git commit -m "Your message from the table above"
git pull --rebase
git push
```

Do this **before the deadline of 25 September 2026, 23:59**, and check the repository's
Contributors page afterwards — all five names should appear.

## Step 3 — Confirm the lecturer can see it

Open the repository link in a private/incognito window. If the code loads without a login prompt,
the lecturer can reach it. Include the link in the eLearning submission (it is already printed on
the report cover page and in `README.md`).

## Rebuilding the report if the repository URL ever changes

The URL is stored in one place:

```bash
echo "https://github.com/NEW-OWNER/NEW-REPO" > tools/repo_url.txt
python tools/build_report.py
```

That regenerates `DSA521S_Group11_Project_Report.pdf` with the new link on the cover page and in
the conclusion. Remember to update the link in `README.md` too, then rebuild the submission zip.
