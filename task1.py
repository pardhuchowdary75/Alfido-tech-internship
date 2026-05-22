"""
============================================================
  Alfido Tech Internship – Task 1: Python File Handling & Automation
  Author  : Intern
  Goal    : Demonstrate file I/O, automation, and exception handling
============================================================
"""

import os
import shutil
import csv
import json
from datetime import datetime

# ── Helper: timestamped log ──────────────────────────────────────────────────
def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# ============================================================
# SECTION 1 – Read & Write TXT files
# ============================================================
def demo_txt_files() -> None:
    """Write some lines to a .txt file, then read them back."""
    filepath = "sample_output.txt"
    lines = [
        "Hello from Alfido Tech Internship!",
        "Python file handling is powerful.",
        "Task 1 – File Handling & Automation",
    ]

    # --- Write ---
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        log(f"TXT written → {filepath}")
    except IOError as e:
        log(f"ERROR writing TXT: {e}")
        return

    # --- Read ---
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        log("TXT content read successfully:\n" + content)
    except FileNotFoundError:
        log("ERROR: file not found after writing – unexpected!")

# ============================================================
# SECTION 2 – Read & Write CSV files
# ============================================================
def demo_csv_files() -> None:
    """Create a CSV with sample employee data, then read it back."""
    filepath = "employees.csv"
    headers = ["ID", "Name", "Department", "Salary"]
    rows = [
        [1, "Alice",   "Engineering", 75000],
        [2, "Bob",     "Marketing",   60000],
        [3, "Charlie", "HR",          55000],
        [4, "Diana",   "Engineering", 80000],
    ]

    # --- Write ---
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        log(f"CSV written → {filepath}")
    except IOError as e:
        log(f"ERROR writing CSV: {e}")
        return

    # --- Read & summarise ---
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            employees = list(reader)

        log(f"CSV rows read: {len(employees)}")
        salaries = [int(e["Salary"]) for e in employees]
        log(f"  Average salary : ₹{sum(salaries)/len(salaries):,.0f}")
        log(f"  Highest salary : ₹{max(salaries):,}")
        log(f"  Lowest salary  : ₹{min(salaries):,}")
    except FileNotFoundError:
        log("ERROR: CSV file not found.")

# ============================================================
# SECTION 3 – File Automation (rename, move, delete)
# ============================================================
def demo_file_automation() -> None:
    """Automate common file operations: rename, move, delete."""

    # Create a temporary working directory
    work_dir = "automation_demo"
    os.makedirs(work_dir, exist_ok=True)

    original  = os.path.join(work_dir, "original.txt")
    renamed   = os.path.join(work_dir, "renamed.txt")
    moved_dir = os.path.join(work_dir, "archive")
    moved     = os.path.join(moved_dir, "renamed.txt")

    # Step 1 – Create a file
    try:
        with open(original, "w") as f:
            f.write("This file will be renamed and moved.\n")
        log(f"Created  → {original}")
    except IOError as e:
        log(f"ERROR creating file: {e}")
        return

    # Step 2 – Rename
    try:
        os.rename(original, renamed)
        log(f"Renamed  → {renamed}")
    except OSError as e:
        log(f"ERROR renaming: {e}")

    # Step 3 – Move to sub-directory
    try:
        os.makedirs(moved_dir, exist_ok=True)
        shutil.move(renamed, moved)
        log(f"Moved    → {moved}")
    except (OSError, shutil.Error) as e:
        log(f"ERROR moving file: {e}")

    # Step 4 – Delete the moved file
    try:
        os.remove(moved)
        log(f"Deleted  → {moved}")
    except FileNotFoundError:
        log("ERROR: file to delete not found.")

    # Step 5 – Clean up demo folder
    shutil.rmtree(work_dir, ignore_errors=True)
    log(f"Cleaned up '{work_dir}' directory.")

# ============================================================
# SECTION 4 – Exception Handling showcase
# ============================================================
def demo_exception_handling() -> None:
    """Show try-except-else-finally best practices."""

    # Attempt 1: open a file that does not exist
    log("\n-- Exception Handling Demo --")
    try:
        with open("nonexistent_file.txt", "r") as f:
            data = f.read()
    except FileNotFoundError as e:
        log(f"Caught FileNotFoundError: {e}")
    except PermissionError as e:
        log(f"Caught PermissionError: {e}")
    else:
        log("File read successfully (no exception).")
    finally:
        log("'finally' block always executes – good for cleanup.")

    # Attempt 2: invalid JSON
    bad_json = '{"name": "Alice", "age": }'
    try:
        parsed = json.loads(bad_json)
    except json.JSONDecodeError as e:
        log(f"Caught JSONDecodeError: {e}")

    # Attempt 3: division by zero (general ValueError usage)
    try:
        result = 100 / 0
    except ZeroDivisionError as e:
        log(f"Caught ZeroDivisionError: {e}")

# ============================================================
# MAIN ENTRY POINT
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  Alfido Tech – Task 1: File Handling & Automation")
    print("=" * 60)

    print("\n[1] TXT File Operations")
    demo_txt_files()

    print("\n[2] CSV File Operations")
    demo_csv_files()

    print("\n[3] File Automation (rename / move / delete)")
    demo_file_automation()

    print("\n[4] Exception Handling")
    demo_exception_handling()

    print("\n" + "=" * 60)
    print("  Task 1 Complete ✓")
    print("=" * 60)