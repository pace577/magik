#!/usr/bin/python3

## Customization variables

BROWSER = "firefox" # used to execute shell command to open links
FILE = "test.csv"

# csv file headings. change these or change the csv file headings to make things work
SUBJECT = "subject"
LIVE = "live_lectures"
RECORDED = "recorded_lectures"
ASSIGNMENTS = "assignments"

# Subjects names
SUBJECT_LIST = ["ps", "cv"] #must match the entry in csv file
SUBJECT_ARGS_LIST = [["ps", "PS"], ["cv", "CV"]] #can enter any of these in the command line 

# Link types
LINK_LIVE_ARGS_LIST = ["live_lectures", "lecture", "live", "l", "zoom"]
LINK_RECORDED_ARGS_LIST = ["recorded_lectures", "recorded", "r"]
LINK_ASSIGNMENTS_ARGS_LIST = ["assignments", "assignment", "a"] 