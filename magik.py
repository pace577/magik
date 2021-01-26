#!/usr/bin/python3

import csv
import os
import sys
from vars import *  # Contains customization variables

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
        Opens the subject link. If LINK_TYPE is not given, it falls back to default value LIVE.
    h, help    
        Displays this help text
    init
        Creates the csv file according to variables specified in vars.py
    set
        Writes the given link to the csv file at a place corresponding to LINK_TYPE and SUBJECT

Examples:
    To open a link corresponding to subject(row heading) 'math' and link type(column heading) 'lecture'
        ./magik.py open math lecture
    
    You can also use shortcuts. (Assign shortcuts in vars.py)
        ./magik.py o m l
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
                if DEBUG:
                    print("Opening link with browser...")
                os.system(BROWSER + " " + row[link_type]) #command to open the link


def set_link(subject, link_type, link):
    """Opens the link provided in the csv file using the appropriate heading.
    Change the BROWSER variable if the default browser doesn't work for
    you"""
    subject_index = SUBJECT_LIST.index(subject)
    link_type_index = LINK_TYPE_LIST.index(link_type)

    f = open(FILE, 'r')
    reader = csv.reader(f, delimiter=',')
    contents_list = list(reader)
    contents_list[subject_index+1][link_type_index+1] = link
    f.close()

    nf = open(FILE, 'w')
    writer = csv.writer(nf)
    writer.writerows(contents_list)
    nf.close()
    if DEBUG:
        print("Wrote item to new file!")



def get_link_type(link_type_arg):
    """Returns the appropriate csv header for the intended link type (from
    LINK_TYPE_LIST) by comparing the argument with all the items in
    LINK_TYPE_ARGS_LIST"""
    for i in range(len(LINK_TYPE_ARGS_LIST)):
        if link_type_arg in LINK_TYPE_ARGS_LIST[i]:
            return LINK_TYPE_LIST[i]
    print("Subject not available in LINK_TYPE_ARGS_LIST!")
    return -1


def get_subject(subject_arg):
    """Returns the appropriate csv header for the intended link type (from
    SUBJECT_LIST) by comparing the argument with all the items in
    SUBJECT_ARGS_LIST"""
    for i in range(len(SUBJECT_ARGS_LIST)):
        if subject_arg in SUBJECT_ARGS_LIST[i]:
            return SUBJECT_LIST[i]
    print("Subject not available in SUBJECT_ARGS_LIST!")
    return -1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(USAGE_TEXT)
    else:
        command = sys.argv[1]

        if command in ["init"]:
            if not os.path.exists(FILE):
                with open(FILE, "w") as f:
                    f.write(SUBJECT+","+','.join(LINK_TYPE_LIST)+"\n")
                    commas = ","*len(LINK_TYPE_LIST)
                    for subject in SUBJECT_LIST:
                        f.writelines(subject+commas+"\n")
                    # add more commands to add more stuff to the file, like the subject headings
                    # could also add commands to insert link at a specific point ('set' command)
            else:
                print(FILE, "already exists. Skipping creating a new file.")

        elif command in ["open", "o"]:
            subject = get_subject(sys.argv[2])
            if len(sys.argv) == 3:
                link_type = LINK_TYPE_LIST[0]
            else:
                link_type = get_link_type(sys.argv[3])
            
            if subject != -1 and link_type != -1:
                if DEBUG:
                    print("Opening", subject, link_type)
                open_link(subject, link_type)
            else:
                print("ERROR: subject or link_type not found")

        elif command in ["set"]:
            subject = get_subject(sys.argv[2])
            link_type = get_link_type(sys.argv[3])
            link = sys.argv[4]
            
            if subject != -1 and link_type != -1:
                set_link(subject, link_type, link)
                if DEBUG:
                    print("Finished setting link of", subject, link_type, "to", link)
            else:
                print("ERROR: subject or link_type not found")

        elif command in ["help", "h"]:
            print(HELP_TEXT)
