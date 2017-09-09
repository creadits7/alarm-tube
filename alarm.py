from time import sleep, strftime
from sys import argv, platform
import random
import webbrowser
import re
import requests
from os import system

#Point to file containing Youtube video URLs
file_containing_urls = "Videos.txt"

#  pulls a youtube URL from Videos.txt at random
def get_url(filename):
    try:
        f = open(filename, 'r')
    #Exit program is file is not found
    except FileNotFoundError:
        raise("Error: Could not find file '" + filename + "'")
        
    songs = []
    # add songs in list to songs[]
    for line in f:
        if not line.startswith("#") and is_web_url(line):
            songs.append(line)
    # pick a random song and store it in song variable
    song = random.choice(songs)
    f.close()

    # verify connection to URL
    try:
        r = requests.get(song)

    except requests.exceptions.RequestException:
        print("Error: Could not connect to URL: ", song)
        exit(0)

    # return song URL
    return song


# Gets the song title using RE on the HTML tags
def get_song_name(url):
    r = requests.get(url)

    song_title_regex = re.compile(r'<title>([\S\s]+)</title>')

    mo = song_title_regex.search(r.text)

    song_title = mo.groups(0)[0]


    #Replaces the HTML code for apostrophe with the symbol
    return re.sub(r'&#39;', "\'", song_title)

def is_web_url(text):
    return re.match(r'(http://|https://|www.)(www\.)?([a-zA-Z0-9-_.]+)(\.[a-zA-Z0-9]{2,4})(\S+)', text)

def main():
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
            if platform.startswith("win"):
                clear_screen = "cls"
            else:
                clear_screen = "clear"

            system(clear_screen)
            print("Alarm time: %s" % alarm_time)
            # call get_url function to pull video from txt file
            url = get_url(file_containing_urls)
            print("-" * 50)
            print(get_song_name(url))
            print("-" * 50)
            webbrowser.register('firefox', None)
            # open web browser window for youtube
            webbrowser.open(url)
            sleep(1)
            current_time = strftime("%H:%M:%S")


if __name__ == "__main__":
    main()

