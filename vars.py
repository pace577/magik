#!/usr/bin/env python3

import os
import platform

#--- Customization variables ---#

BROWSER = "firefox" # used to execute shell command to open links
LINK_FILE = "links.csv"
TIME_FILE = "times.csv"

# CSV file headings for first row, first column. Used to create new csv file. If
# a CSV file already exists, these strings must match headings in those files.
SUBJECT = "subject" # For LINK_FILE
DAY = "Day" # For TIME_FILE

# Link types (LINK_FILE headings for columns containing links)
LINK_TYPE_LIST = ["live_lectures", "recorded_lectures", "assignments"] #must match the entry in csv file
LINK_TYPE_ARGS_LIST = [["lecture", "live", "l", "zoom"],
                       ["recorded", "r"],
                       ["assignment", "a"]] #can enter any of these in the command line

# Subject names (LINK_FILE first column rows)
SUBJECT_LIST = ["ps", "cv", "math"] #must match the entry in csv file
SUBJECT_ARGS_LIST = [["ps", "PS"], ["cv", "CV"], ["math", "MATH"]] #can enter any of these in the command line

# Time slots (For TIME_FILE)
TIME_LIST = ["09:00","10:00","11:00","12:00","14:00"]
DAY_LIST = ["Mon", "Tue", "Wed", "Thu", "Fri"]

# Magik opens the link EARLY seconds prior to the event time
EARLY = 300

#--- End of Customization Variables ---#
#--- Don't modify anything beyond this, unless you know what you're doing ---#


#--- Other ---#

DEBUG = True
DateType = list[str, str] #type alias

# Adding SUBJECT_LIST to SUBJECT_ARGS_LIST to avoid repetition
for i in range(len(SUBJECT_LIST)):
    SUBJECT_ARGS_LIST[i] = [SUBJECT_LIST[i]] + SUBJECT_ARGS_LIST[i]

# Adding LINK_TYPE_LIST to LINK_TYPE_ARGS_LIST to avoid repetition
for i in range(len(LINK_TYPE_LIST)):
    LINK_TYPE_ARGS_LIST[i] = [LINK_TYPE_LIST[i]] + LINK_TYPE_ARGS_LIST[i]

# Use start to run commands from windows console
if platform.system() == "Windows":
    BROWSER_COMMAND = "start "+BROWSER
else:
    BROWSER_COMMAND = BROWSER

# Put absolute path for LINK_FILE and TIME_FILE
LINK_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), LINK_FILE)
TIME_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), TIME_FILE)


#--- Help text ---#
USAGE_TEXT = """
Usage:
    ./magik.py [COMMAND] [SUBJECT] [LINK_TYPE] [LINK]

Commands: 
    h, help
        Displays help text
    init
        Creates the csv file according to variables specified in vars.py
    on, open-next
        Opens the link for the next event from current time as given in the first link column of TIME_FILE
    op, open-prev
        Opens the link for the previous event from current time as given in the first link column of TIME_FILE
    w, watch
        Infinite process that waits until the event time and opens links then.
    o, open
        Opens the subject link
    set
        Writes the given link to the csv file at a place corresponding to LINK_TYPE and SUBJECT
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
    init
        Creates the csv file according to variables specified in vars.py
    h, help
        Displays this help text
    on, open-next
        Opens the link for the next event from current time as given in the
        first link column of TIME_FILE
    op, open-prev
        Opens the link for the previous event from current time as given in the
        first link column of TIME_FILE
    w, watch
        Calculates the time for next event from times.csv, waits until that time
        and then opens the link. This continues until the process is killed.
    o, open
        Opens the subject link. If LINK_TYPE is not given, it falls back to
        default value LIVE.
    set
        Writes the given link to the csv file at a place corresponding to
        LINK_TYPE and SUBJECT

Examples:
    To open the link to the class you just missed
        ./magik.py open-prev
        ./magik.py op

    To open the link to the next class
        ./magik.py open-next
        ./magik.py on

    To open a link corresponding to subject(row heading) 'math' and link
    type(column heading) 'lecture'
        ./magik.py open math lecture
    
    You can also use shortcuts. (Assign shortcuts in vars.py)
        ./magik.py o m l

    To automatically open links, set your timetable in times.csv and run
        ./magik.py watch
"""
