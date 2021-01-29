#!/usr/bin/env python

import os
import sys
import time
from vars import *  # Contains customization variables
from utils import * # Contains helper functions


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(USAGE_TEXT)
    else:
        command = sys.argv[1]

        if command in ["init"]:
            create_csv_file(LINK_FILE, "link")
            create_csv_file(TIME_FILE, "time")

        elif command in ["open", "o"]:
            subject_arg, link_index = parse_time_slot_entry(sys.argv[2])

            subject = get_subject(subject_arg)
            if len(sys.argv) == 3:
                link_type = LINK_TYPE_LIST[0]
            else:
                link_type = get_link_type(sys.argv[3])

            if subject is None or link_type is None:
                print("ERROR: subject or link_type not found")
            else:
                if DEBUG:
                    print("Opening", subject, link_type)
                open_link(subject, link_type, link_index)

        elif command in ["set"]:
            subject = get_subject(sys.argv[2])
            link_type = get_link_type(sys.argv[3])
            link = sys.argv[4]
            
            if subject is None or link_type is None:
                print("ERROR: subject or link_type not found")
            else:
                set_link(subject, link_type, link)
                if DEBUG:
                    print("Finished setting link of", subject, link_type, "to", link)

        elif command in ["w","watch"]:
            try:
                while True:
                    open_next_link()
            except KeyboardInterrupt as e:
                print("Exiting watch mode {}".format(str(e)))


        elif command in ["help", "h"]:
            print(HELP_TEXT)

        else:
            print(USAGE_TEXT)
