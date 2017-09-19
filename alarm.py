from time import sleep, strftime
from sys import argv, platform
import random
import webbrowser
import re
import requests
from os import system, path

# Point to file containing Youtube video URLs
FILE_CONTAINING_URLS = "Videos.txt"

# Check if Operating System is Windows
WINDOWS_OS = platform.startswith("win")

# Number of times to retry with a new URL before failing
RETRY_COUNT = 10

if not path.isfile(FILE_CONTAINING_URLS):
    print("Error: Could not find file '%s'" % FILE_CONTAINING_URLS)
    print("Please make sure it is in the same directory as \"alarm.py\"")
    exit(1)


def fetch_song_data(url):
    """Fetch song data from url"""
    response = requests.get(url)
    return response.text


def video_is_available(url):
    """Checks to make sure the video is available (not just the web page)"""
    vid_unavail_regex = re.compile(r'(Sorry about that\.)')
    response = requests.get(url)
    match = vid_unavail_regex.search(response.text)

    if match is None:
        return True
    else:
        return False


def get_url():
    """Pulls a youtube URL from Videos.txt at random"""
    songs = []
    with open(FILE_CONTAINING_URLS) as f:
        for line in f:
            if not line.startswith("#") and is_web_url(line):
                songs.append(line)

    # pick a random song and store it in song variable
    song = random.choice(songs)

    url_attempts = []

    for x in range(RETRY_COUNT):
        response = requests.get(song)
        # check if URL is valid and also make sure video is available
        if response.ok and video_is_available(song):
            return song
        # store failed URL
        url_attempts.append(song)
        # choose new random song
        song = random.choice(songs)

    print("Could not access video URLs. Please check network connection")
    print("Tried the following URLs before failing:")
    print("\n".join(url_attempts))
    exit(1)


# Gets the song title using RE on the HTML tags
def parse_song_data(data):
    """Returns the song title from <title> HTML tags"""
    song_title_regex = re.compile(r'<title>([\S\s]+)</title>')

    match = song_title_regex.search(data)

    song_title = match.groups(0)[0]

    # Replaces the HTML code for apostrophe with the symbol
    return re.sub(r'&#39;', "\'", song_title)


def is_web_url(text):
    """Regex test to make sure URL is in valid format"""
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
            if WINDOWS_OS:
                clear_screen = "cls"
            else:
                clear_screen = "clear"

            # clear the terminal screen
            system(clear_screen)

            # print alarm time
            print("Alarm time: %s" % alarm_time)
            # pull random video URL from text file
            url = get_url()
            print("-" * 50)
            # print song title
            print(parse_song_data(fetch_song_data(url)))
            print("-" * 50)

            # open web browser window for youtube
            webbrowser.open(url)

            # update time every second
            sleep(1)
            current_time = strftime("%H:%M:%S")


if __name__ == "__main__":
    main()

