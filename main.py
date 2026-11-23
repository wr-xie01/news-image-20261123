#!/usr/bin/env python3
"""Entry point for the 23 November 2026 news-image bounty.

Copies the front page this repository holds (entry.png) to the output
directory make.fun grades ($MAKEFUN_OUTPUT_DIR, or /output). No network,
no randomness: every run writes the same bytes.
"""

import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def check_image(path):
    """Refuse to run unless the image is a 1024x1024 PNG under 1 MiB."""
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, not 1024x1024")
    return size


def main():
    size = check_image(SOURCE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    digest = hashlib.sha256(open(dest, "rb").read()).hexdigest()
    print(f"wrote {dest} ({size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
