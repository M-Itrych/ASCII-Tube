import sys
import threading

import cv2
import pygame
import time
from moviepy.editor import VideoFileClip
from src.ImageProcessing import ImageConverter as Ita
import os


class VideoPlayer:
    def __init__(self, video_path, print_frequency=2, target_fps=24):
        self.video_path = video_path
        self.print_frequency = print_frequency
        self.target_fps = target_fps
        self.converter = Ita.ImageConverter()
        self.video = None

    def clear_console(self):
        print("\033[H\033[J", end="")


    def print_ascii_frame(self, ascii_frame):
        self.clear_console()
        sys.stdout.write(ascii_frame)
        sys.stdout.flush()

    def play_video(self):
        pygame.init()
        pygame.mixer.init()

        try:
            with VideoFileClip(self.video_path) as video:
                self.video = video
                video.audio.write_audiofile('music.wav')

                pygame.mixer.music.load('music.wav')
                pygame.mixer.music.play()

                start_time = time.time()
                self.stop_video = False
                last_frame = None

                def display_frames():
                    nonlocal last_frame
                    for frame_number, frame in enumerate(video.iter_frames(fps=self.target_fps, dtype='uint8'), 1):
                        if self.stop_video:
                            break

                        # Compare current frame with the last frame
                        if frame_number > 1 and (frame == last_frame).all():
                            continue

                        ascii_frame = self.converter.generate_ascii_art(frame)
                        if frame_number % self.print_frequency == 0:
                            self.print_ascii_frame(ascii_frame)

                        last_frame = frame  # Update last frame

                        elapsed_time = time.time() - start_time
                        target_time = frame_number * (1 / self.target_fps)
                        time_to_wait = target_time - elapsed_time
                        if time_to_wait > 0:
                            time.sleep(time_to_wait)

                display_thread = threading.Thread(target=display_frames)
                display_thread.start()

                while display_thread.is_alive():
                    key = cv2.waitKey(1)
                    if key & 0xFF == ord('q'):
                        self.stop_video = True
                        break

                display_thread.join()

        finally:
            if self.video:
                self.video.close()
            cv2.destroyAllWindows()
            pygame.mixer.music.stop()
