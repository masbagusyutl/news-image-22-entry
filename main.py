#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261122.

Copies the build-time-rendered front page (entry.png, drawn by
render.py from 50 verified stories of Sunday 22 November 2026)
to $MAKEFUN_OUTPUT_DIR/entry.png. Standard library only, fully
deterministic: the same bytes are written on every run.
"""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

# sha256 of entry.png as rendered by render.py in this session.
EXPECTED_SHA256 = "e6d4b4094613e94fc2b6f56b883b158288963aabb922eee378b38a283ee68cc1"
EXPECTED_BYTES = 238013

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != PNG_MAGIC:
        raise SystemExit("entry.png is not a PNG")
    if len(data) != EXPECTED_BYTES:
        raise SystemExit("entry.png size changed: %d bytes" % len(data))
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("entry.png sha256 mismatch")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (dst, len(data)))


if __name__ == "__main__":
    main()
