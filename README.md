# canvas-hw: tools for offline homework grading in Canvas LMS
Bart Massey 2023

These are tools for working with Canvas grades.

* `unpack-hw.py`: Unpack downloaded Canvas submissions for
  local grading. Each submission should be a ZIP file or PDF.
  
  With the `--rust` flag enabled, Cargo projects in
  submissions are cleaned up to a more consistent format.

* `upload-grades.py`: Extract the local grades and upload
  them to Canvas.

* `update-grades.py`: Extract the local grades and update a
  local CSV gradebook. Not used in a long time — may not work.

Thus is SpeedGrader avoided.

## Instructions

### One-Time Setup

* https://canvas.pdx.edu/profile/settings to generate Canvas
  API token
* Store Canvas API token in ~/.canvasgrader
* Clone `canvasgrader` fork
  http://github.com/BartMassey-upstream/canvasgrader (for
  now) and run `pip install .`


### Get the Student Roster

Before unpacking submissions, obtain the roster from Canvas:

1. Sign in to Canvas and open your course. The number in
   `/courses/<course-id>` in the URL is the course ID.
2. Open `https://canvas.pdx.edu/courses/<course-id>/students`,
   replacing `<course-id>` with that number.
3. Copy the JSON shown there into a file named `students.json`
   in your local grading directory. Save the JSON itself,
   rather than the page's HTML.

The file must contain a JSON list of student objects with
`id` and `short_name` fields, for example:

```json
[
  {"id": 12345, "short_name": "Example Student"}
]
```

The unpacker reads this file; it does not create it. It matches
the Canvas student IDs in submission filenames to roster IDs.
Run the commands below from the directory containing this
file. Use the paths to the scripts if they are elsewhere.

### Download and Unpack

Download the assignment's submission ZIP from Canvas. Then run:

```sh
python3 unpack-hw.py --hw "Homework 1" submissions.zip
```

Replace the assignment name and ZIP filename as needed. The
unpacker creates `staged/` and an empty `graded/` directory.

### Grading

* For each directory in `staged/`:

  * Edit `GRADING.txt`. Replace the `-` on line 3 with an
    integer score. Keep line 4 blank; add feedback below it.
  * Keep the hidden `.canvas_info` file inside each student's
    directory, alongside `GRADING.txt`. It records the Canvas
    student and assignment IDs. Use `ls -la` to see it.
  * Move directory from `staged/` to `graded/`

### Upload

* Find course ID in course URL
* Find assignment ID in assignment URL
* Run `python3 upload-grades.py <courseid> <asgid>`

Note that the `--test` argument can be used to upload just
one grade. This is useful to avoid spamming the list if
something is configured wrong / you are unsure. Notice also
that projects will be moved to `uploaded/` after their
grades are uploaded: in particular the `--test` project
(which is effectively a random one).

## Acknowledgments

Thanks to the authors of the Python `canvasgrader` package
for making this all possible.

## License

This work is licensed under the "MIT License". Please see the file
`LICENSE.txt` in this distribution for license terms.
