# ASCII Tube

This Python script allows you to search for music videos on YouTube and play them in ASCII art form. 

## Demo
Check out this short video to see the program in action: [ASCII Tube Demo](https://youtu.be/HZ5kZ6KhAP4)

## Requirements

- Python 3.x
- `pytube`, `youtubesearchpython`, `moviepy`, `pygame`, and `opencv` libraries
- Terminal with support for ANSI escape codes

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your_username/ascii-video-player.git
   ```

2. Navigate to the project directory:

   ```sh
   cd ascii-video-player
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the script in your terminal:

   ```sh
   python main.py
   ```

2. Choose the option to search for music.
3. Enter the title of the song you want to search for.
4. Select the desired video from the search results.
5. Enjoy watching the video in ASCII art!

## Features

- Search for music videos by title.
- Play selected music videos in ASCII art form.

## File Structure

- `main.py`: Contains the main menu and the entry point of the program.
- `src/VideoPlayer/Player.py`: Defines the `VideoPlayer` class responsible for playing videos in ASCII art.
- `src/ImageProcessing/ImageConverter.py`: Defines the `ImageConverter` class responsible for converting frames to ASCII art.

## Contributing
Contributions are welcome! If you have any ideas, improvements, or bug fixes, feel free to open an issue or submit a pull request.

Enjoy exploring the world of music videos in ASCII art!
