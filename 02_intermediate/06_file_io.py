# =============================================================================
# 06_file_io.py — File I/O in Python
# python-ai-journey | 02_intermediate
# =============================================================================
#
# THEORY:
# -------
# File I/O (Input/Output) lets Python read from and write to files.
# Python treats files as STREAMS — sequences of bytes or characters.
#
# Key concepts:
#   1. open()         — opens a file, returns file object
#   2. File modes     — r, w, a, x, r+, rb, wb
#   3. read methods   — read(), readline(), readlines()
#   4. write methods  — write(), writelines()
#   5. with statement — automatic file closing (context manager)
#   6. File position  — tell(), seek()
#   7. Text vs Binary — text mode (str) vs binary mode (bytes)
#   8. CSV/JSON       — structured file formats
#   9. pathlib        — modern file path handling
#
# FILE MODES:
#   "r"  — read (default). FileNotFoundError if missing
#   "w"  — write. Creates or OVERWRITES existing file!
#   "a"  — append. Creates or adds to end of existing
#   "x"  — exclusive create. FileExistsError if exists
#   "r+" — read + write. File must exist
#   "b"  — binary mode (add to any: "rb", "wb")
#   "t"  — text mode (default, add to any: "rt")
#
# INTERNALS (CPython):
# ---------------------
# open() returns a file object (io.TextIOWrapper for text mode):
#   - Wraps OS-level file descriptor
#   - Maintains internal buffer (default 8KB)
#   - Reads/writes in chunks for performance
#   - __enter__/__exit__ for context manager support
#
# Text mode:
#   - Decodes bytes using encoding (default: platform-dependent, use utf-8!)
#   - Handles line endings (\n on Unix, \r\n on Windows) automatically
#
# Binary mode:
#   - Raw bytes — no encoding/decoding
#   - Use for images, PDFs, audio, video, pickled objects
#
# Buffering:
#   - Python buffers writes in memory before flushing to disk
#   - flush() or close() forces buffer to disk
#   - with statement calls close() → flushes automatically
#
# =============================================================================

import os
import json
import csv
import tempfile
from pathlib import Path


# Setup — use temp directory for all file operations
WORK_DIR = Path(tempfile.mkdtemp())
print(f"Working directory: {WORK_DIR}\n")


# =============================================================================
# PART 1: BASIC FILE OPERATIONS
# =============================================================================

print("=" * 60)
print("PART 1: BASIC FILE OPERATIONS")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 1: Writing Files
# -----------------------------------------------------------------------------

print("\n--- Writing Files ---")

# Write mode — creates or OVERWRITES
filepath = WORK_DIR / "sample.txt"

with open(filepath, "w", encoding="utf-8") as f:
    f.write("Hello, Python!\n")
    f.write("This is line 2\n")
    f.write("This is line 3\n")
    bytes_written = f.write("Final line\n")

print(f"File written: {filepath}")
print(f"Last write returned: {bytes_written} chars")

# writelines — write a list of strings (no auto newlines!)
lines = ["Line A\n", "Line B\n", "Line C\n"]
filepath2 = WORK_DIR / "lines.txt"

with open(filepath2, "w", encoding="utf-8") as f:
    f.writelines(lines)             # no newlines added automatically!

print(f"writelines file written: {filepath2}")

# Append mode — adds to END, never overwrites
with open(filepath, "a", encoding="utf-8") as f:
    f.write("Appended line 1\n")
    f.write("Appended line 2\n")

print(f"Appended to: {filepath}")


# -----------------------------------------------------------------------------
# SECTION 2: Reading Files
# -----------------------------------------------------------------------------

print("\n--- Reading Files ---")

# read() — entire file as one string
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

print(f"read() — entire file:\n{content}")

# readline() — one line at a time
with open(filepath, "r", encoding="utf-8") as f:
    line1 = f.readline()    # reads first line including \n
    line2 = f.readline()    # reads second line

print(f"readline() line1: {line1!r}")
print(f"readline() line2: {line2!r}")

# readlines() — all lines as a list
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"\nreadlines(): {lines[:3]}...")   # first 3

# Iterate line by line — MOST MEMORY EFFICIENT for large files!
print("\nIterating line by line (memory efficient):")
with open(filepath, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        print(f"  Line {i}: {line.rstrip()}")
        if i >= 3:
            print("  ...")
            break


# -----------------------------------------------------------------------------
# SECTION 3: File Position — tell() and seek()
# -----------------------------------------------------------------------------

print("\n--- File Position ---")

with open(filepath, "r", encoding="utf-8") as f:
    print(f"Initial position: {f.tell()}")    # 0 — start of file

    first = f.read(5)                          # read 5 chars
    print(f"After read(5): position={f.tell()}, read='{first}'")

    f.seek(0)                                  # go back to start
    print(f"After seek(0): position={f.tell()}")

    first_again = f.read(5)
    print(f"Reading again: '{first_again}'")   # same as before

    f.seek(0, 2)                               # seek to END (whence=2)
    print(f"End of file position: {f.tell()}") # file size in bytes


# -----------------------------------------------------------------------------
# SECTION 4: File Modes Comparison
# -----------------------------------------------------------------------------

print("\n--- File Modes ---")

test_file = WORK_DIR / "modes_test.txt"

# "w" — write (overwrites!)
with open(test_file, "w") as f:
    f.write("Original content\n")
print(f"After 'w': {open(test_file).read().strip()}")

with open(test_file, "w") as f:
    f.write("Overwritten!\n")              # original gone!
print(f"After 2nd 'w': {open(test_file).read().strip()}")

# "a" — append (preserves!)
with open(test_file, "a") as f:
    f.write("Appended line\n")
print(f"After 'a': {open(test_file).read().strip()}")

# "x" — exclusive create (fails if exists)
try:
    with open(test_file, "x") as f:
        f.write("Won't work!")
except FileExistsError as e:
    print(f"\n'x' mode on existing file: FileExistsError!")

new_file = WORK_DIR / "brand_new.txt"
with open(new_file, "x") as f:
    f.write("Created exclusively!\n")
print(f"'x' on new file: success!")


# =============================================================================
# PART 2: BINARY FILES
# =============================================================================

print("\n" + "=" * 60)
print("PART 2: BINARY FILES")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 5: Binary Read/Write
# -----------------------------------------------------------------------------

print("\n--- Binary Mode ---")

binary_file = WORK_DIR / "data.bin"

# Write binary — raw bytes
data = bytes([72, 101, 108, 108, 111])   # ASCII for "Hello"
with open(binary_file, "wb") as f:
    f.write(data)
    f.write(b" World!")                   # b prefix = bytes literal

print(f"Wrote {len(data)} bytes")

# Read binary
with open(binary_file, "rb") as f:
    raw = f.read()

print(f"Read bytes: {raw}")
print(f"Decoded:    {raw.decode('utf-8')}")

# Text vs Binary difference
text_file = WORK_DIR / "text.txt"
with open(text_file, "w", encoding="utf-8") as f:
    f.write("Hello\nWorld")

# Read as text — \n is a newline character
with open(text_file, "r") as f:
    text = f.read()
print(f"\nText mode:   {repr(text)}")    # 'Hello\nWorld'

# Read as binary — \n is byte 0x0a
with open(text_file, "rb") as f:
    binary = f.read()
print(f"Binary mode: {binary}")          # b'Hello\nWorld'


# =============================================================================
# PART 3: STRUCTURED FILE FORMATS
# =============================================================================

print("\n" + "=" * 60)
print("PART 3: STRUCTURED FORMATS — CSV AND JSON")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 6: CSV Files
# -----------------------------------------------------------------------------

print("\n--- CSV Files ---")

csv_file = WORK_DIR / "students.csv"

# Write CSV
students = [
    {"name": "Ayush",  "score": 95, "grade": "A"},
    {"name": "Rahul",  "score": 72, "grade": "B"},
    {"name": "Priya",  "score": 88, "grade": "A"},
    {"name": "Kiran",  "score": 65, "grade": "C"},
]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "score", "grade"])
    writer.writeheader()
    writer.writerows(students)

print(f"CSV written: {csv_file}")

# Read CSV
print("\nReading CSV:")
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']}: {row['score']} ({row['grade']})")

# Read as plain lists
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    print(f"\nAs lists:")
    for row in reader:
        print(f"  {row}")


# -----------------------------------------------------------------------------
# SECTION 7: JSON Files
# -----------------------------------------------------------------------------

print("\n--- JSON Files ---")

json_file = WORK_DIR / "config.json"

# Python dict → JSON file
config = {
    "app_name": "python-ai-journey",
    "version": "1.0.0",
    "settings": {
        "debug": True,
        "max_retries": 3,
        "timeout": 30.5,
        "allowed_hosts": ["localhost", "127.0.0.1"]
    },
    "features": ["auth", "logging", "caching"]
}

# json.dump — write to file
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=4)    # indent=4 for pretty printing

print(f"JSON written: {json_file}")

# Read JSON file → Python dict
with open(json_file, "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(f"\nLoaded app_name: {loaded['app_name']}")
print(f"Debug mode:      {loaded['settings']['debug']}")
print(f"Features:        {loaded['features']}")

# JSON string conversion (not file)
json_str  = json.dumps(config, indent=2)    # dict → JSON string
back_dict = json.loads(json_str)            # JSON string → dict
print(f"\njson.dumps type: {type(json_str)}")
print(f"json.loads type: {type(back_dict)}")

# JSON type mapping
print(f"\nJSON ↔ Python type mapping:")
mapping = {
    "JSON string":  json.loads('"hello"'),
    "JSON number":  json.loads('42'),
    "JSON float":   json.loads('3.14'),
    "JSON bool":    json.loads('true'),
    "JSON null":    json.loads('null'),
    "JSON array":   json.loads('[1,2,3]'),
    "JSON object":  json.loads('{"a":1}'),
}
for json_type, py_val in mapping.items():
    print(f"  {json_type:<15} → Python {type(py_val).__name__}: {py_val}")


# =============================================================================
# PART 4: PATHLIB — MODERN FILE PATH HANDLING
# =============================================================================

print("\n" + "=" * 60)
print("PART 4: PATHLIB")
print("=" * 60)


# -----------------------------------------------------------------------------
# SECTION 8: pathlib.Path
# -----------------------------------------------------------------------------

print("\n--- pathlib.Path ---")

# pathlib is the modern way to handle file paths
# Much better than os.path string manipulation!

p = Path(WORK_DIR)

# Path properties
print(f"Path:      {p}")
print(f"Name:      {p.name}")         # last component
print(f"Parent:    {p.parent}")       # parent directory
print(f"Exists:    {p.exists()}")     # does it exist?
print(f"Is dir:    {p.is_dir()}")
print(f"Is file:   {p.is_file()}")

# Working with files
sample = p / "sample.txt"             # / operator for joining paths!
print(f"\nFile path: {sample}")
print(f"Stem:      {sample.stem}")    # filename without extension
print(f"Suffix:    {sample.suffix}")  # extension
print(f"Exists:    {sample.exists()}")

# Read/write with pathlib
new_path = p / "pathlib_test.txt"
new_path.write_text("Written via pathlib!\nLine 2\n", encoding="utf-8")
content = new_path.read_text(encoding="utf-8")
print(f"\nPathlib write/read: {content.strip()}")

# List directory contents
print(f"\nFiles in work dir:")
for f in sorted(p.iterdir()):
    size = f.stat().st_size
    print(f"  {f.name:<25} {size:>6} bytes")

# Glob — find files by pattern
print(f"\n*.txt files:")
for f in sorted(p.glob("*.txt")):
    print(f"  {f.name}")

print(f"\n*.json files:")
for f in sorted(p.glob("*.json")):
    print(f"  {f.name}")

# Create directories
new_dir = p / "subdir" / "nested"
new_dir.mkdir(parents=True, exist_ok=True)
print(f"\nCreated nested dir: {new_dir}")
print(f"Is dir: {new_dir.is_dir()}")


# -----------------------------------------------------------------------------
# SECTION 9: Practical Patterns
# -----------------------------------------------------------------------------

print("\n--- Practical Patterns ---")

# PATTERN 1: Safe file reading with default
def read_file_safe(path, default=""):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return default

content = read_file_safe(WORK_DIR / "nonexistent.txt", "File not found!")
print(f"Safe read: {content}")

# PATTERN 2: Process large file line by line — memory efficient
def count_lines(filepath):
    """Count lines without loading entire file"""
    count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for _ in f:
            count += 1
    return count

line_count = count_lines(filepath)
print(f"\nLine count in sample.txt: {line_count}")

# PATTERN 3: Write JSON safely — write to temp then rename
def save_json_safely(data, filepath):
    """Write to temp file first, then rename — atomic operation"""
    filepath = Path(filepath)
    tmp = filepath.with_suffix(".tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        tmp.rename(filepath)           # atomic on most systems
        print(f"  Saved safely to {filepath.name}")
    except Exception as e:
        tmp.unlink(missing_ok=True)    # cleanup temp on failure
        raise

save_json_safely({"status": "ok"}, WORK_DIR / "safe_output.json")

# PATTERN 4: Read CSV into list of dicts
def load_csv(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

data = load_csv(csv_file)
print(f"\nLoaded {len(data)} students from CSV")
avg_score = sum(int(s["score"]) for s in data) / len(data)
print(f"Average score: {avg_score:.1f}")

# PATTERN 5: Append log entries
log_file = WORK_DIR / "app.log"

def log(message, level="INFO"):
    import datetime
    timestamp = datetime.datetime.now().isoformat()
    entry = f"[{timestamp}] [{level}] {message}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)

log("Application started")
log("Processing data")
log("Something went wrong!", "ERROR")
log("Application stopped")

print(f"\nLog file contents:")
with open(log_file, "r") as f:
    for line in f:
        print(f"  {line.rstrip()}")


# Cleanup
import shutil
shutil.rmtree(WORK_DIR)
print(f"\nCleaned up temp directory: {WORK_DIR}")


# =============================================================================
# SUMMARY
# =============================================================================
#
# | Concept         | Key Insight                                            |
# |-----------------|--------------------------------------------------------|
# | open()          — always use with 'with' for auto-close                  |
# | "r"             — read. FileNotFoundError if missing                     |
# | "w"             — write. OVERWRITES existing file!                       |
# | "a"             — append. Adds to end, never overwrites                  |
# | "x"             — exclusive create. FileExistsError if exists            |
# | "rb"/"wb"       — binary mode. Raw bytes, no encoding                   |
# | encoding="utf-8"— ALWAYS specify encoding for text files                 |
# | read()          — entire file as string (careful with large files!)      |
# | readline()      — one line at a time                                     |
# | for line in f   — most memory efficient — streams one line at a time     |
# | tell()/seek()   — file position pointer                                  |
# | json.dump/load  — write/read JSON files                                  |
# | csv.DictWriter  — write CSV with headers                                 |
# | csv.DictReader  — read CSV as list of dicts                              |
# | pathlib.Path    — modern path handling — use / operator                  |
# | p.read_text()   — read file content directly via Path                    |
# | p.glob("*.txt") — find files by pattern                                  |
#
# GOLDEN RULES:
# 1. ALWAYS use 'with' — guarantees file closes even on exception
# 2. ALWAYS specify encoding="utf-8" — avoid platform surprises
# 3. "w" OVERWRITES — use "a" to preserve existing content
# 4. Iterate file line by line for large files — never read() all at once
# 5. Use pathlib.Path over os.path — cleaner, more readable
# 6. Use json.dump/load for structured data — not manual string building
# 7. Write to temp file then rename for safe atomic writes
#
# =============================================================================
