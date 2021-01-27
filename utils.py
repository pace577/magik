
import time
import csv
import os
from vars import *  # Contains customization variables

## Code

def check_multiple_links(subject_arg):
    """Parses subject_arg and checks if a link index was provided"""
    if "-" in subject_arg:
        if DEBUG:
            print("Multiple Links Present")
        subject_arg = subject_arg.split("-")
        link_index = int(subject_arg[1])-1
        subject_arg = str(subject_arg[0])
        return subject_arg, link_index
    return subject_arg, None

def open_link(subject, link_type, link_index=None):
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
                    os.system(BROWSER + " " + row[link_type]) #command to open the link
                else:
                    if DEBUG:
                        print("open_link: Opening link {} with browser...".format(str(link_index)))
                    os.system(BROWSER + " " + row[link_type].split()[link_index])


def set_link(subject, link_type, link):
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


def create_csv_file(file_name, file_type="link"):
    """Creates the CSV file that magik fetches the data from"""
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


# def get_latest_time():
#     current_time = time.strftime(TIME_FORMAT_ALT).split()
#     with open(TIME_FILE, 'r') as f:
#         reader = list(csv.reader(f, delimiter=','))
#         times = [item for row in reader[1:] for item in row[1:]]
#         latest_time = times[0]
#         # for row in reader:

#         return times

def open_next_link():
    """Checks what the next event in line is, waits until it's time for the
    event and opens the link after waiting."""
    with open(TIME_FILE, 'r') as f:
        reader = list(csv.DictReader(f))
        next_event_time = get_next_event_time()
        if DEBUG:
            print("open_next_link: The next event is on", next_event_time)
        for row in reader:
            if row[DAY] == next_event_time[0]:
                time.sleep(get_waiting_time(next_event_time))
                subject, link_index = check_multiple_links(row[next_event_time[1]])
                open_link(subject, LINK_TYPE_LIST[0], link_index)
                if DEBUG:
                    print("open_next_link: open_link() finished")


def get_next_event_time():
    """Returns the time for next event, in the list with date format ["%a","%R"]"""
    current_day = time.strftime("%a")
    current_hour = int(time.strftime("%H"))
    current_minute = int(time.strftime("%M"))

    if current_day in DAY_LIST:
        for time_entry in TIME_LIST:
            hour, minute = map(int, time_entry.split(":"))
            if hour > current_hour:
                if DEBUG:
                    print("get_next_event_time: The event is today!")
                return [current_day, time_entry]
            if hour == current_hour and minute > current_minute:
                if DEBUG:
                    print("get_next_event_time: The event is within an hour!")
                return [current_day, time_entry]
        # else
        day_index = DAY_LIST.index(current_day)
        if day_index == len(DAY_LIST)-1:
            return [DAY_LIST[0], TIME_LIST[0]]
        else:
            if DEBUG:
                print("get_next_event_time: The event is tomorrow!")
            return [DAY_LIST[day_index+1], TIME_LIST[0]]
    else:
        return [DAY_LIST[0], TIME_LIST[0]]


def get_waiting_time(event_time):
    """Returns waiting time in seconds. Input (event_time) is a list or tuple of
    time format ["%a","%R"]"""
    waiting_seconds = 0
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
    if DEBUG:
        print("get_waiting_time: Must wait a total of {} seconds".format(waiting_seconds))

    return waiting_seconds
