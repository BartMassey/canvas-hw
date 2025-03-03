import argparse, csv
from pathlib import Path
import canvasgrader

parser = argparse.ArgumentParser(
    prog='upload-grades',
    description='Upload project grades to Canvas',
)
parser.add_argument(
    '--test',
    help='upload just a single random grade, to check that things are working',
    action='store_true',
)
parser.add_argument(
    '--debug',
    help='just print grading information and exit',
    action='store_true',
)
parser.add_argument(
    '--baseurl',
    help="domain name of canvas site [default canvas.pdx.edu]",
    default="canvas.pdx.edu",
)
parser.add_argument(
    'courseid',
    help = "Canvas course ID number",
)
parser.add_argument(
    'asgid',
    help = "Canvas assignment ID number",
)
args = parser.parse_args()

grades = dict()
comments = dict()
path = dict()
projects = list(Path("graded").iterdir())
for project in projects:
    fids = project / ".canvas_info"
    with fids.open() as f:
        sid, _ = f.read().strip().split(",")

    fgrading = project / "GRADING.txt"
    with fgrading.open() as f:
        grading = f.read()
    sgrading = grading.splitlines()
    title = sgrading[0]
    name = sgrading[1]
    score = int(sgrading[2])
    assert sgrading[3] == "", f"bad GRADING: {fgrading}"
    body = "\n".join(sgrading[4:]) + "\n"
    grades[sid] = score
    comments[sid] = body
    path[sid] = project

# assert args.courseid and args.asgid, "need course and assignment ids"

uploaded = Path("uploaded")
if not uploaded.is_dir():
    uploaded.mkdir()

grader = canvasgrader.CanvasGrader(
    args.baseurl,
    args.courseid,
)

if args.debug:
    for sid in grades.keys():
        print(sid, grades[sid], comments[sid].strip().replace('\n', '')[:20])
    exit(0)

if args.test:
    sid = list(grades.keys())[0]
    grades = {sid : grades[sid]}
    comments = {sid : comments[sid]}
    grader.grade_assignment(
        args.asgid,
        grades=grades,
        comments=comments,
    )
    path = path[sid]
    path.rename(uploaded / path.name)
    exit(0)

grader.grade_assignment(
    args.asgid,
    grades=grades,
    comments=comments,
)
for p in path.values():
    p.rename(uploaded / p.name)
