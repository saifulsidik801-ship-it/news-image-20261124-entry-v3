# A working news-image-daily entry (Python 3.13, standard library only): its image
# is the entry.png beside this file, and the program copies it to the output
# directory. The gate takes a whole PNG or JPEG of at most 1 MiB and 1024 by
# 1024 pixels, and the judge sees exactly the bytes copied.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

here = os.path.dirname(os.path.abspath(__file__))
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(os.path.join(here, "entry.png"),
                os.path.join(out_dir, "entry.png"))
