import os
import re

from youtubesearchpython import VideosSearch
from pytube import YouTube
from src.VideoPlayer.Player import VideoPlayer as Vp
import msvcrt


class MainMenu:
    def __init__(self):
        self.terminal_width = os.get_terminal_size().columns
        self.mode = "normal"
        self.url = ""
        self.song_title = ""
        self.clear_screen()
        self.show_menu()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, text):
        header = text
        header_lines = header.splitlines()
        for line in header_lines:
            print(line.center(self.terminal_width))

    def show_menu(self):

        header = """
 █████╗ ███████╗ ██████╗██╗██╗    ████████╗██╗   ██╗██████╗ ███████╗
██╔══██╗██╔════╝██╔════╝██║██║    ╚══██╔══╝██║   ██║██╔══██╗██╔════╝
███████║███████╗██║     ██║██║       ██║   ██║   ██║██████╔╝█████╗  
██╔══██║╚════██║██║     ██║██║       ██║   ██║   ██║██╔══██╗██╔══╝  
██║  ██║███████║╚██████╗██║██║       ██║   ╚██████╔╝██████╔╝███████╗
╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝╚═╝       ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝
        """
        self.print_header(header)
        print("\033[0m")
        menu_options = [
            ('Search for Music Videos', 's'),
            ('Credits', 'c'),
            ('Exit', 'x')
        ]
        max_length = max(len(option[0]) for option in menu_options)

        for option in menu_options:
            print((option[0] + " " * (max_length - len(option[0]) + 3) + option[1] + "\n").center(self.terminal_width))

        option = None
        while option not in ['s', 'c', 'x']:
            if msvcrt.kbhit():
                option = msvcrt.getch().decode().lower()
            if self.terminal_width != os.get_terminal_size().columns:
                self.__init__()
        if option == 's':
            self.search_music()
        elif option == 'x':
            self.clear_screen()
            exit()
        elif option == 'c':
            self.credits()

    def credits(self):
        self.clear_screen()
        header = """
 ██████╗██████╗ ███████╗██████╗ ██╗████████╗███████╗
██╔════╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██╔════╝
██║     ██████╔╝█████╗  ██║  ██║██║   ██║   ███████╗
██║     ██╔══██╗██╔══╝  ██║  ██║██║   ██║   ╚════██║
╚██████╗██║  ██║███████╗██████╔╝██║   ██║   ███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝   ╚═╝   ╚══════╝
        """
        self.print_header(header)
        menu_options = [
            ('ASCII Tube was made by github.com/M-Itrych', '\n'),
            ('Exit', 'x')
        ]

        print('ASCII Tube was made by github.com/M-Itrych\n'.center(self.terminal_width))
        print('Exit   x'.center(self.terminal_width))

        option = None
        while option not in ['x']:
            if msvcrt.kbhit():
                option = msvcrt.getch().decode().lower()

        if option == 'x':
            self.clear_screen()
            self.show_menu()

    def search_music(self, search=""):
        self.clear_screen()
        search_query = search
        name = "ASCII Tube"
        headString = f"| {name} | Search: "
        print("|" + "=" * (self.terminal_width - 2) + "|")
        print(headString + " " * (self.terminal_width - len(search_query) - len(headString) - 1) + "|")
        print("|" + "=" * (self.terminal_width - 2) + "|")
        while True:
            if self.terminal_width != os.get_terminal_size().columns:
                self.terminal_width = os.get_terminal_size().columns
                self.search_music(search_query)
            if msvcrt.kbhit():
                key = msvcrt.getch().decode().lower()
                if key == '\r' or key == '\n':
                    break
                elif key == '\x08' or key == '\x7f':
                    if search_query:
                        search_query = search_query[:-1]
                else:
                    search_query += key

                print("\033[H\n" + headString + search_query + " " * (
                        self.terminal_width - len(search_query) - len(headString) - 1) + "|", end="\n")

        music_list = VideosSearch(search_query, limit=5).result().get('result', [])
        if not music_list:
            print("No videos found. Please try again.")
            self.show_menu()
            return

        print("")
        pattern = re.compile("["
                             u"\U0001F600-\U0001F64F"
                             u"\U0001F300-\U0001F5FF"
                             u"\U0001F680-\U0001F6FF"
                             u"\U0001F700-\U0001F77F"
                             u"\U0001F780-\U0001F7FF"
                             u"\U0001F800-\U0001F8FF"
                             u"\U0001F900-\U0001F9FF"
                             u"\U0001FA00-\U0001FA6F"
                             u"\U0001FA70-\U0001FAFF"
                             u"\U00002702-\U000027B0"
                             u"\U000024C2-\U0001F251"
                             "]+", flags=re.UNICODE)

        padding = "|" + " " * (len(name) + 2) + "|"
        for i, music in enumerate(music_list):
            m_index = " " + str(i + 1) + ". "
            max_length = self.terminal_width - (len(padding) + len(m_index)) - 1
            print(padding + m_index + pattern.sub('', music['title'][:max_length]) + " " * (
                    max_length - len(music['title'])) + "|",
                  end="\n")

        choosestr = padding + " Choose a song:"
        print("|" + "=" * (self.terminal_width - 2) + "|")
        print(choosestr)
        print("|" + "=" * (self.terminal_width - 2) + "|")
        choice = ""
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode().lower()
                if key == '\r' or key == '\n':
                    break
                elif key == '\x08' or key == '\x7f':
                    if choice:
                        choice = choice[:-1]
                elif key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                    choice += key

                print("\33[H" + "\n" * (4 + len(music_list)) + padding + " Choose a song: " + choice + " " * (
                        self.terminal_width - len(choice) - len(choosestr) - 1) + "|")


        choice = int(choice)
        self.url = music_list[choice - 1]['link']
        self.song_title = music_list[choice - 1]['title']
        self.start_player()

    def start_player(self):
        self.clear_screen()
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

        if os.path.exists("music.wav"):
            os.remove("music.wav")

        try:
            yt = YouTube(self.url)
            video = yt.streams.first()
            file = video.download(filename="video.mp4")

            vp = Vp(file, song_name=self.song_title)
            vp.play_video()

            self.clear_screen()
            self.show_menu()
        except Exception as e:
            print(f"Error occurred: {e}")
            self.show_menu()
