# Fake-Cam

Fake Cam is a Python-based project that allows you to create a virtual camera that plays videos or displays images as a camera feed. Additionally, you can play audio alongside the media and control various settings such as resolution, volume, and looping.

## Features

- Play video files or display images through a virtual camera.
- Optionally play an audio file alongside the video/image.
- Control the resolution of the virtual camera.
- Adjust the volume for audio files and video audio.
- Loop the media playback.
- Stop the script by typing `stop` in the console.

## How to Use

1. **Make sure you have Python installed on your system.**
2. **Clone this repository:**

    ```sh
    git clone https://github.com/e43b/Fake-Cam/
    ```

3. **Navigate to the project directory:**

    ```sh
    cd Fake-Cam
    ```

## Requirements

- Python 3.x
- `argparse`
- `imageio`
- `numpy`
- `Pillow`
- `pyvirtualcam`
- `pyaudio`
- `moviepy`
- `pygame`

You can install the required packages using pip:

```sh
pip install -r requirements.txt
```

## Usage

### Command Line Arguments

- `resolution`: The resolution of the virtual camera (e.g., 1280x720).
- `media_file`: The path to the media file (video or image).
- `-a`, `--audio`: (Optional) The path to the audio file to play alongside the media.
- `-v`, `--volume`: (Optional) The volume for the audio file (0-100). Default is 30.
- `-av`, `--video_audio`: (Optional) The audio setting for the video (0 for off, 1 for on). Default is 1.
- `-vv`, `--video_volume`: (Optional) The volume for the video audio (0-100). Default is 100.
- `-l`, `--loop`: (Optional) Loop the media playback.

### Example Commands

#### Playing a Video File

```sh
python fcam.py 1280x720 video.mp4
```

#### Playing a Video File with Audio

```sh
python fcam.py 1280x720 video.mp4 -a audio.mp3
```

#### Playing a Video File with Audio and Custom Volume

```sh
python fcam.py 1280x720 video.mp4 -a audio.mp3 -v 50
```

#### Playing a Video File with Audio, Custom Volume, and Looping

```sh
python fcam.py 1280x720 video.mp4 -a audio.mp3 -v 50 -l
```

#### Displaying an Image

```sh
python fcam.py 1280x720 image.jpg
```

#### Stopping the Script

While the script is running, you can type `stop` in the console to stop the execution.

## Web Interface

You can use the provided site to generate the command easily:

[Fake Cam Command Generator](https://e43b.github.io/Fake-Cam/)

## Demonstrations

Here are some images and videos demonstrating the usage and features of Fake Cam:

### Images

![Demo Image 1](path/to/demo-image1.png)
![Demo Image 2](path/to/demo-image2.png)

### Videos

[![Demo Video 1](path/to/demo-video1-thumbnail.png)](path/to/demo-video1.mp4)
[![Demo Video 2](path/to/demo-video2-thumbnail.png)](path/to/demo-video2.mp4)

## Additional Notes

- Ensure that your system has the necessary permissions to create and use a virtual camera.
- This script has been tested on Windows. Functionality on other operating systems may vary.
- When using the loop option, the media will restart automatically once it finishes.
- Use the `stop` command in the console to terminate the script gracefully.

## Links

- [Project Repository](https://github.com/e43b/Fake-Cam)
- [Discord Server](https://discord.gg/CsBMMXBz7t)
- [Donations](https://oxapay.com/donate/40874860)

## Credits

&copy; Created by [E43b](https://github.com/e43b)
