#!/usr/bin/python3

## Customization variables

BROWSER = "firefox" # used to execute shell command to open links
LINK_FILE = "links.csv"
TIME_FILE = "times.csv"
# TIME_FORMAT = "%a %R"

# csv file headings. change these or change the csv file headings to make things work
SUBJECT = "subject" #first column heading
DAY = "Day"

# Link types (CSV file headings for columns containing links)
LINK_TYPE_LIST = ["live_lectures", "recorded_lectures", "assignments"]
LINK_TYPE_ARGS_LIST = [["live_lectures", "lecture", "live", "l", "zoom"],
                       ["recorded_lectures", "recorded", "r"],
                       ["assignments", "assignment", "a"]]

# Subject names (CSV file first column rows)
SUBJECT_LIST = ["ps", "cv", "math"] #must match the entry in csv file
SUBJECT_ARGS_LIST = [["ps", "PS"], ["cv", "CV"], ["math", "MATH"]] #can enter any of these in the command line

# Time slots
TIME_LIST = ["09:00","10:00","11:00","12:00","14:00","17:10","17:11","17:12"]
DAY_LIST = ["Mon", "Tue", "Wed", "Thu", "Fri"]


## Other

DEBUG = False

## Help text
USAGE_TEXT = """
Usage:
    ./magik.py [COMMAND] [SUBJECT] [LINK_TYPE] [LINK]

Commands: 
    o, open    
        Opens the subject link
    h, help    
        Displays help text
    init
        Creates the csv file according to variables specified in vars.py
    set
        Writes the given link to the csv file at a place corresponding to LINK_TYPE and SUBJECT
    w, watch
        Infinite process that waits until the event time and opens links then.
"""
HELP_TEXT = """
Usage:
    ./magik.py [COMMAND] [SUBJECT] [LINK_TYPE] [LINK]
    python3 magik.py [COMMAND] [SUBJECT] [LINK_TYPE] [LINK]
    magik [COMMAND] [SUBJECT] [LINK_TYPE] [LINK]

Description:
    Open links with magik. Before using magik, make sure to set the variables
    at the beginning of the script to customize it to your needs.

Commands:
    o, open    
        Opens the subject link. If LINK_TYPE is not given, it falls back to
        default value LIVE.
    h, help    
        Displays this help text
    init
        Creates the csv file according to variables specified in vars.py
    set
        Writes the given link to the csv file at a place corresponding to
        LINK_TYPE and SUBJECT
    w, watch
        Calculates the time for next event from times.csv, waits until that time
        and then opens the link. This continues until the process is killed.

Examples:
    To open a link corresponding to subject(row heading) 'math' and link
    type(column heading) 'lecture'
        ./magik.py open math lecture
    
    You can also use shortcuts. (Assign shortcuts in vars.py)
        ./magik.py o m l

    To automatically open links, set your timetable in times.csv and run
        ./magik.py watch
"""
