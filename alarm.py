from time import sleep, strftime
from sys import argv
from random import randint
import webbrowser
import re
import requests
from os import system



def set_alarm():
    # If less or more than 3 arguments do not run script
    if len(argv) != 4:
        print("No arguments given or invalid format. Please enter a time. "
        "Format is HH MM SS (24hr). Example: alarm.py 19 30 00")
        print("Current time is ", strftime("%H:%M:%S"))
        exit()

        # else convert the arguments into a single string that we can use to compare later
    else:
        alarm_hour = argv[1]
        alarm_minute = argv[2]
        alarm_second = argv[3]
        alarm_time = "%s:%s:%s" % (alarm_hour, alarm_minute, alarm_second)
        print("Alarm set for %s." % (alarm_time))

        # Set current_time to the current system time in the same format as the user provided time
        current_time = strftime("%H:%M:%S")
        print("Current time is %s." % (current_time))

        # infinite loop for alarm to keep running
    while True:
        # while it isn't time for alarm to go off, wait 1 second and check time again
        while current_time != alarm_time:
            sleep(1)
            current_time = strftime("%H:%M:%S")
        else:
            # open web browser window for youtube
            # call get_url function to pull video from txt file
            system("clear")
            print("Alarm time: %s" % alarm_time)
            url = get_url()
            print("-" * 50)
            print(get_song_name(url))
            print("-" * 50)
            webbrowser.register('firefox', None)
            webbrowser.open(url)
            sleep(1)
            current_time = strftime("%H:%M:%S")


#  pulls a youtube URL from Videos.txt at random
def get_url():
    f = open("Videos.txt", 'r')
    songs = []
    # add songs in list to songs[]
    for line in f:
        if line[0] != "#" and "." in line:
            songs.append(line)
    # pick a random song and store it in song variable
    song = songs[randint(0, len(songs) - 1)]
    f.close()
    # return URL of random song
    return song

# Gets the song title from between the 'title' HTML tags and changes the &#39; to an apostrophe if it exists.
def get_song_name(url):
    r = requests.get(url)

    songTitleRegex = re.compile(r'(?<=<title>)([\S\s]+)(?=</title>)')

    mo = songTitleRegex.search(r.text)

    songtitle = ""

    for i in mo.groups(0):
        songtitle += i

    return re.sub(r'&#39;', "\'", songtitle)


if __name__ == "__main__":
    set_alarm()
