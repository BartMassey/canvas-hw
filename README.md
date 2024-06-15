# canvas-hw: tools for offline homework grading in Canvas LMS
Bart Massey 2023

These are tools for working with Canvas grades.

* `unpack-hw.py`: Download an assignment from Canvas that is
  presumed to be one ZIP file per submission, unpack that
  locally for local grading.
  
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


### Download

* Go to `https://canvas.pdx.edu/courses/<course-id>/students` and
  copy-paste the JSON found there into `students.json`
  (gross, will fix later)

* Download a zipball of the HW from Canvas.

* Run `unpack-hw.py --hw <assignment name> <zipball>`

### Grading

* For each directory in `staged/`:

  * Edit `GRADING.txt`. Make sure to replace the `-` with a
    score.
  * Move directory from `staged/` to `graded/`

### Upload

* Find course ID in course URL
* Find assignment ID in assignment URL
* Run `upload-grades.py <courseid> <asgid>`

Note that the `--test` argument can be used to upload just
one grade. This is useful to avoid spamming the list if
something is configured wrong / you are unsure.

## Acknowledgments

Thanks to the authors of the Python `canvasgrader` package
for making this all possible.

## License

This work is licensed under the "MIT License". Please see the file
`LICENSE.txt` in this distribution for license terms.
