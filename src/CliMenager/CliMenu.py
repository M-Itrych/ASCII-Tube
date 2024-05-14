import os
from youtubesearchpython import VideosSearch
from pytube import YouTube
from src.VideoPlayer.Player import VideoPlayer as Vp

class MainMenu:
    def __init__(self):
        self.mode = "normal"
        self.url = ""
        self.clear_screen()
        self.print_header()
        self.show_menu()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        header = """ASCII Video Player by M-Itrych"""
        print(header)

    def show_menu(self):
        print('\n--- Main Menu ---')
        print('1. Search for Music Videos')
        print('2. Exit')
        option = input('Enter your choice: ')
        if option == '1':
            self.search_music()
        elif option == '2':
            exit()
        else:
            print("Invalid choice. Please enter 1 or 2.")
            self.show_menu()

    def search_music(self):
        self.clear_screen()
        query = input('Enter the title of a song: ')

        music_list = VideosSearch(query, limit=5).result().get('result', [])
        if not music_list:
            print("No videos found. Please try again.")
            self.show_menu()
            return

        print('\n--- Search Results ---')
        for i, music in enumerate(music_list):
            print(f'{i + 1}. {music["title"]}')

        option = input('Enter the number of the song you want to choose: ')
        try:
            option = int(option)
            if 1 <= option <= len(music_list):
                self.url = music_list[option - 1]['link']
                self.start_player()
            else:
                print("Invalid choice. Please enter a number within the range.")
                self.search_music()
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            self.search_music()

    def start_player(self):
        self.clear_screen()
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

        try:
            yt = YouTube(self.url)
            video = yt.streams.first()
            file = video.download(filename="video.mp4")

            vp = Vp(file)
            vp.play_video()

            self.clear_screen()
            self.show_menu()
        except Exception as e:
            print(f"Error occurred: {e}")
            self.show_menu()

if __name__ == "__main__":
    MainMenu()
