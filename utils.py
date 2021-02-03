#!/usr/bin/env python3

import time
import csv
import os
from vars import *  # Contains customization variables

## Code

def parse_time_slot_entry(subject_arg: str) -> (str, int):
    """Parses subject_arg and checks if a link index was provided."""
    if "-" in subject_arg:
        if DEBUG:
            print("Multiple Links Present")
        subject_arg = subject_arg.split("-")
        link_index = int(subject_arg[1])-1
        subject_arg = str(subject_arg[0])
        return subject_arg, link_index
    return (subject_arg, None)


def open_link(subject: str, link_type: str, link_index: int = None):
    """Opens the link provided in the csv file using the appropriate heading.
    Change the BROWSER variable if the default browser doesn't work for
    you"""

    with open(LINK_FILE, 'r') as f:
        # check if all the headings are correctly named
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            if row[SUBJECT] == subject:
                if link_index is None:
                    if DEBUG:
                        print("open_link: Opening link with browser...")
                    os.system(BROWSER_COMMAND + " " + row[link_type]) #command to open the link
                else:
                    if DEBUG:
                        print("open_link: Opening link {} with browser...".format(str(link_index)))
                    os.system(BROWSER_COMMAND + " " + row[link_type].split()[link_index])


def set_link(subject: str, link_type: str, link: str):
    """Opens the link provided in the csv file using the appropriate heading.
    Change the BROWSER variable if the default browser doesn't work for
    you"""
    subject_index = SUBJECT_LIST.index(subject)
    link_type_index = LINK_TYPE_LIST.index(link_type)

    f = open(LINK_FILE, 'r')
    reader = csv.reader(f, delimiter=',')
    contents_list = list(reader)
    contents_list[subject_index+1][link_type_index+1] = link
    f.close()

    nf = open(LINK_FILE, 'w')
    writer = csv.writer(nf)
    writer.writerows(contents_list)
    nf.close()
    if DEBUG:
        print("Wrote item to new file!")


def get_link_type(link_type_arg: str) -> str:
    """Returns the appropriate csv header for the intended link type (from
    LINK_TYPE_LIST) by comparing the argument with all the items in
    LINK_TYPE_ARGS_LIST"""
    for i in range(len(LINK_TYPE_ARGS_LIST)):
        if link_type_arg in LINK_TYPE_ARGS_LIST[i]:
            return LINK_TYPE_LIST[i]
    print("Subject not available in LINK_TYPE_ARGS_LIST!")
    return None


def get_subject(subject_arg: str):
    """Returns the appropriate csv header for the intended link type (from
    SUBJECT_LIST) by comparing the argument with all the items in
    SUBJECT_ARGS_LIST"""
    for i in range(len(SUBJECT_ARGS_LIST)):
        if subject_arg in SUBJECT_ARGS_LIST[i]:
            return SUBJECT_LIST[i]
    print("Subject not available in SUBJECT_ARGS_LIST!")
    return None


def create_csv_file(file_name: str, file_type: str = "link"):
    """Creates LINK_FILE and TIME_FILE that magik fetches the data from."""
    if not os.path.exists(file_name):
        if file_type == "link":
            with open(file_name, "w") as f:
                f.write(SUBJECT+","+','.join(LINK_TYPE_LIST)+"\n")
                commas = ","*len(LINK_TYPE_LIST)
                for subject in SUBJECT_LIST:
                    f.writelines(subject+commas+"\n")
            # add more commands to add more stuff to the file, like the subject headings
            # could also add commands to insert link at a specific point ('set' command)
        elif file_type == "time":
            with open(file_name, "w") as f:
                f.write(DAY+","+','.join(TIME_LIST)+"\n")
                commas = ","*len(TIME_LIST)
                for day in DAY_LIST:
                    f.writelines(day+commas+"\n")

    else:
        print(file_name, "already exists. Skipping creating a new file.")


def read_time_file_entry(event_time: DateType) -> str:
    """Reads TIME_FILE and outputs the slot contents corresponding to the given
    event_time. Input is a list in the format ["%a","%R"]."""
    with open(TIME_FILE, 'r') as f:
        reader = list(csv.DictReader(f))
        for row in reader:
            if row[DAY] == event_time[0]:
                return row[event_time[1]]


def watch_mode():
    """Checks what the next event is in TIME_FILE, waits until it's time for the
    event and opens the link after waiting."""
    try:
        while True:
            next_event_time = get_event_time()
            if DEBUG:
                print("watch_mode: The next event is on", next_event_time)
            waiting_time, is_late = get_waiting_time(next_event_time)
            time_file_entry = read_time_file_entry(next_event_time)
            if DEBUG and time_file_entry == "":
                print("watch_mode: time_file_entry is blank!")
            subject, link_index = parse_time_slot_entry(time_file_entry)
            if is_late:
                open_link(subject, LINK_TYPE_LIST[0], link_index)
                if DEBUG:
                    print(f"watch_mode: event is_late. Opened link, will wait for {waiting_time} seconds now.")
                time.sleep(waiting_time)
            else:
                time.sleep(waiting_time)
                open_link(subject, LINK_TYPE_LIST[0], link_index)
                if DEBUG:
                    print("watch_mode: open_link() finished")
    except KeyboardInterrupt as e:
        print("Exiting watch mode {}".format(str(e)))


def open_event_link(reverse_time: bool = False):
    """Checks what the next event is in TIME_FILE, waits until it's time for the
    event and opens the link after waiting."""
    if reverse_time:
        global DAY_LIST, TIME_LIST
        DAY_LIST = DAY_LIST[::-1]
        TIME_LIST = TIME_LIST[::-1]
    next_event_time = get_event_time(reverse_time)
    if DEBUG:
        if reverse_time:
            print("open_event_link: reverse_time is True. Will open previous event")
        else:
            print("open_event_link: reverse_time is False. Will open next event")
        print("open_event_link: The next event is on", next_event_time)
    time_file_entry = read_time_file_entry(next_event_time)
    if DEBUG and time_file_entry == "":
        print("open_event_link: time_file_entry is blank!")

    subject, link_index = parse_time_slot_entry(time_file_entry)
    if DEBUG:
        print("open_event_link: Opening link...")
    open_link(subject, LINK_TYPE_LIST[0], link_index)


def compare_times(entry_time: int, given_time: int, reverse_time: bool = False) -> bool:
    """Used in get_event_time_from_given_time() to make it work with reverse_time=False.
    It compares given times. Returns True if:
    - reverse_time is True and entry_time>given_time
    - reverse_time is False and entry_time<given_time"""
    if reverse_time:
        return entry_time < given_time
    else:
        return entry_time > given_time


def get_event_time_from_given_time(given_time: DateType, reverse_time: bool = False) -> DateType:
    """Returns next event time from given time. Reads only TIME_LIST, does not
    read TIME_FILE .Given time input format is ["%a","%R"]"""
    given_day = given_time[0]
    given_hour, given_minute = map(int, given_time[1].split(":"))

    if given_day in DAY_LIST:
        for time_entry in TIME_LIST:
            entry_hour, entry_minute = map(int, time_entry.split(":"))
            if compare_times(entry_hour, given_hour, reverse_time):
                if DEBUG:
                    print(f"get_event_time_from_given_time: {given_time} The event might be today {time_entry}!")
                return [given_day, time_entry]
            elif entry_hour == given_hour and compare_times(entry_minute, given_minute, reverse_time):
                if DEBUG:
                    print(f"get_event_time_from_given_time: {given_time} The event might within an hour!")
                return [given_day, time_entry]
            elif entry_hour == given_hour and entry_minute == given_minute:
                time_index = TIME_LIST.index(time_entry)
                if time_index < len(TIME_LIST)-1:
                    # if DEBUG:
                    #     print("get_event_time_from_given_time: The event might've just passed! Next event might be tomorrow.")
                    # day_index = DAY_LIST.index(given_day)+1
                # else:
                    if DEBUG:
                        print(f"get_event_time_from_given_time: {given_time} A probable event just passed! There might be another event today.")
                    return [given_day, TIME_LIST[time_index+1]]
        # else
        day_index = DAY_LIST.index(given_day)
        if day_index >= len(DAY_LIST)-1:
            if DEBUG:
                print(f"get_event_time_from_given_time: {given_time} We probably reached the weekend!")
            return [DAY_LIST[0], TIME_LIST[0]]
        else:
            if DEBUG:
                print(f"get_event_time_from_given_time: {given_time} The event might be tomorrow!")
            return [DAY_LIST[day_index+1], TIME_LIST[0]]
    else:
        return [DAY_LIST[0], TIME_LIST[0]]


def get_event_time(reverse_time: bool = False) -> DateType:
    """Returns the time for next event, in the list with date format ["%a","%R"]"""
    current_time = time.strftime("%a %R").split()
    next_event_time = get_event_time_from_given_time(current_time, reverse_time)
    next_event_time_entry = read_time_file_entry(next_event_time)
    while next_event_time_entry == "":
        next_event_time = get_event_time_from_given_time(next_event_time, reverse_time)
        next_event_time_entry = read_time_file_entry(next_event_time)
    return next_event_time



def get_waiting_time(event_time: DateType) -> (int, bool):
    """Returns waiting time in seconds, and a boolean value is_late. is_late is
    True if the next event is less than EARLY seconds from now. Input
    (event_time) is DateType, which is a list of time format ["%a","%R"]"""
    waiting_seconds = 0
    is_late = False
    current_time = time.strftime("%a %R").split()
    week_numbers = {"Mon":1, "Tue":2, "Wed":3, "Thu":4, "Fri":5}

    # hours and minutes
    event_hours_minutes = event_time[1].split(':')
    current_hours_minutes = current_time[1].split(':')
    waiting_hours_minutes = [ int(event_hours_minutes[i]) - int(current_hours_minutes[i]) for i in range(2) ]
    if DEBUG:
        print("get_waiting_time: Must wait for {} hours and {} minutes (didn't count days yet)".format(
        waiting_hours_minutes[0], waiting_hours_minutes[1]))
    waiting_seconds += waiting_hours_minutes[0]*3600 + waiting_hours_minutes[1]*60

    # days
    waiting_days = int(week_numbers[event_time[0]] - week_numbers[current_time[0]])
    if waiting_days == 0 and waiting_seconds < 0:
        waiting_days = 1
    elif waiting_days < 0:
        waiting_days += 7
    waiting_seconds += waiting_days*24*3600

    # open the link EARLY seconds before wait time
    if waiting_seconds - EARLY <= 0:
        #waiting_seconds = 1
        is_late = True
        if DEBUG:
            print("get_waiting_time: No more time. Starting now!")
    else:
        waiting_seconds -= EARLY

    if DEBUG:
        print("get_waiting_time: Must wait a total of {} seconds".format(waiting_seconds))

    return (waiting_seconds, is_late)
