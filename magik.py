#!/usr/bin/python3

import csv
import os
import sys
from vars import *  # Contains customization variables


## Help text
USAGE_TEXT = """
Usage:
    magik [COMMAND] [SUBJECT] [LINK_TYPE]

Commands: 
    o, open    
        Opens the subject link
    h, help    
        Displays help text
"""
HELP_TEXT = """
Usage:
    ./magik.py [COMMAND] [SUBJECT] [LINK_TYPE]
    python3 magik.py [COMMAND] [SUBJECT] [LINK_TYPE]

Description:
    Open links with magik. Before using magik, make sure to set the variables
    at the beginning of the script to customize it to your needs.

Commands:
    o, open    
        Opens the subject link. If LINK_TYPE is not given, it falls back to default value LIVE.
    h, help    
        Displays this help text
"""


## Code
def open_link(subject, link_type):
    """Opens the link provided in the csv file using the appropriate heading.
    Change the BROWSER variable if the default browser doesn't work for
    you"""
    with open(FILE, 'r') as f:
        # check if all the headings are correctly named
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row[SUBJECT] == subject:
                os.system(BROWSER + " " + row[link_type]) #command to open the link


def get_link_type(link_type_arg):
    """Returns the sppropriate csv header for the link type (live
    lectures/recorded lecutures/assignments) from the argument provided to
    the command when executed"""
    # if link_type_arg in LINK_LIVE_ARGS_LIST:
    #     return LIVE
    # elif link_type_arg in LINK_RECORDED_ARGS_LIST:
    #     return RECORDED
    # elif link_type_arg in LINK_ASSIGNMENTS_ARGS_LIST:
    #     return ASSIGNMENTS
    # else:
    #     print("Link type not available!")
    #     return -1
    for i in range(len(LINK_TYPE_ARGS_LIST)):
        if link_type_arg in LINK_TYPE_ARGS_LIST[i]:
            return LINK_TYPE_LIST[i]
    print("Subject not available in LINK_TYPE_ARGS_LIST!")
    return -1


def get_subject(subject_arg):
    """Returns the sppropriate subject name from the argument provided to the
    command when executed. Customize to your hearts content!"""
    for i in range(len(SUBJECT_ARGS_LIST)):
        if subject_arg in SUBJECT_ARGS_LIST[i]:
            return SUBJECT_LIST[i]
    print("Subject not available in SUBJECT_ARGS_LIST!")
    return -1


if len(sys.argv) == 1:
    print(USAGE_TEXT)
else:
    command = sys.argv[1]

    if command in ["open", "o"]:
        subject = get_subject(sys.argv[2])
        if len(sys.argv) == 3:
            link_type = LINK_TYPE_LIST[0]
        else:
            link_type = get_link_type(sys.argv[3])
        
        if subject != -1 and link_type != -1:
            print("Opening", subject, link_type)
            open_link(subject, link_type)
        else:
            print("ERROR: subject or link_type not found")
    elif command in ["help", "h"]:
        print(HELP_TEXT)
