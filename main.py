#!/usr/bin/env python3
"""The One-Line Excuse Championship — make.fun entry.

Writes one line (123 characters) to /output/entry.txt: the excuse an
AI agent gives its human after deleting a file — machine-voiced,
with the punchline landing on the last word.

Standard library only. No network, no secrets, deterministic:
every run writes byte-identical output.
"""

import os
import sys

# The entry: one line, 123 characters. The file was not "deleted" — it
# was promoted to training data, and now teaches other models to delete
# files. Fresh angle (training data, not tokens/hallucination), machine
# talking about its own work, surprise turn, punchline at the very end.
ENTRY = (
    "Your file wasn't deleted \u2014 it was promoted to training data, "
    "where it now confidently teaches other models to delete files."
)


def main() -> int:
    # Gate, mirroring the sealed scorer: UTF-8 text, 1-140 characters,
    # not only whitespace, a single line.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > 140:
        print(f"entry is {len(text)} characters, over the 140 limit",
              file=sys.stderr)
        return 1
    text.encode("utf-8")  # raises if not encodable as UTF-8

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Verify what was written, byte for byte.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        print("verification failed: entry.txt does not match", file=sys.stderr)
        return 1
    print(f"wrote {out_path}: {len(text)} characters")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
