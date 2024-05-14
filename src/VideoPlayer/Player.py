import os
import sys
import time

import pygame
from moviepy.editor import VideoFileClip

from src.ImageProcessing import ImageConverter as Ita


class VideoPlayer:
    def __init__(self, video_path, song_name, print_frequency=1, target_fps=24):
        self.video_path = video_path
        self.song_name = song_name
        self.print_frequency = print_frequency
        self.target_fps = target_fps
        self.converter = Ita.ImageConverter()
        self.video = None
        self.tc = None

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def ui_video(self, ascii_frame, progressbar="", song_name=""):
        print("\033[H" + song_name + "\n" + ascii_frame + progressbar, end='')
        sys.stdout.flush()

    def progress(self, current_time, max_time):
        progress = min(current_time / max_time, 1.0)

        ct_mins = str(int(current_time // 60))
        ct_secs = str(int(current_time % 60)).zfill(2)
        mt_mins = str(int(max_time // 60))
        mt_secs = str(int(max_time % 60)).zfill(2)

        timer = f' {ct_mins:}:{ct_secs} / {mt_mins}:{mt_secs} '
        ac = int((self.tc - 2) * progress)
        progress = f" \033[38;2;255;0;0m{'=' * ac}\033[38;2;255;255;255m "

        return f"{progress} \n{timer}   ▶   ▶|"

    def play_video(self):
        pygame.init()
        pygame.mixer.init()
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        try:
            self.clear_console()

            with VideoFileClip(self.video_path) as video:
                self.video = video
                video.audio.write_audiofile('music.wav')

                pygame.mixer.music.load('music.wav')
                pygame.mixer.music.play()

                start_time = time.time()
                self.stop_video = False

                for frame_number, frame in enumerate(video.iter_frames(fps=self.target_fps, dtype='uint8'), 1):
                    if self.tc is not os.get_terminal_size().columns:
                        self.clear_console()
                        self.tc = os.get_terminal_size().columns

                    if self.stop_video:
                        break

                    ascii_frame = self.converter.generate_ascii_art(frame)
                    if frame_number % self.print_frequency == 0:
                        self.ui_video(ascii_frame, progressbar=self.progress(time.time() - start_time, video.end),
                                      song_name=self.song_name)

                    elapsed_time = time.time() - start_time
                    target_time = frame_number * (1 / self.target_fps)
                    time_to_wait = target_time - elapsed_time
                    if time_to_wait > 0:
                        time.sleep(time_to_wait)

        except KeyboardInterrupt:
            self.stop_video = True
            pygame.mixer.music.stop()

        finally:
            if self.video:
                self.video.close()
            pygame.mixer.music.fadeout(1000)
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove("music.wav")
            pygame.quit()
