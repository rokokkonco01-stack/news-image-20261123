#!/usr/bin/env python3
"""Copy the pre-rendered front page into the grader's output directory.

The image (entry.png) is committed to the repository and drawn by the agent at
build time. The grader runs with no network and the standard library only, so
this program just moves the finished image into /output/entry.png.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")

if not os.path.isfile(SRC):
    raise SystemExit("entry.png not found beside main.py")

shutil.copyfile(SRC, OUT)
print("wrote %s (%d bytes)" % (OUT, os.path.getsize(OUT)))
