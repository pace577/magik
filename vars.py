#!/usr/bin/python3

## Customization variables

BROWSER = "firefox" # used to execute shell command to open links
FILE = "links.csv"

# csv file headings. change these or change the csv file headings to make things work
SUBJECT = "subject" #first column heading

# Link types (CSV file headings for columns containing links)
LINK_TYPE_LIST = ["live_lectures", "recorded_lectures", "assignments"]
LINK_TYPE_ARGS_LIST = [["live_lectures", "lecture", "live", "l", "zoom"],
                       ["recorded_lectures", "recorded", "r"],
                       ["assignments", "assignment", "a"]]

# Subject names (CSV file first column rows)
SUBJECT_LIST = ["ps", "cv", "math"] #must match the entry in csv file
SUBJECT_ARGS_LIST = [["ps", "PS"], ["cv", "CV"], ["math", "MATH"]] #can enter any of these in the command line
