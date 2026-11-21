"""Entry program for make.fun bounty news-image-20261121.

"Sum up 21 November's world news in one image": the front page was rendered
ahead of time by render.py into entry.png, which sits next to this file.
This program copies that image to the output directory the grader reads:
$MAKEFUN_OUTPUT_DIR/entry.png when the variable is set, else
/output/entry.png.

Python 3 standard library only. No network access. Deterministic: the
output bytes are exactly the bytes of the bundled entry.png.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
