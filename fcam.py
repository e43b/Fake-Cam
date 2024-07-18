import argparse
import imageio
import numpy as np
from PIL import Image, ImageOps
import pyvirtualcam
from pyvirtualcam import PixelFormat
import threading
import wave
import pyaudio
import time
import sys
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx.all import volumex

def apply_filter(frame):
    return frame

def play_audio(audio_file, volume):
    chunk = 1024
    wf = wave.open(audio_file, 'rb')
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                     channels=wf.getnchannels(),
                     rate=wf.getframerate(),
                     output=True)
    volume = volume / 100.0

    data = wf.readframes(chunk)
    while data and not stop_event.is_set():
        audio_data = np.frombuffer(data, dtype=np.int16)
        audio_data = (audio_data * volume).astype(np.int16)
        stream.write(audio_data.tobytes())
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    pa.terminate()

def play_video_audio(video_file, volume):
    clip = VideoFileClip(video_file)
    audio = clip.audio
    audio = volumex(audio, volume / 100.0)
    audio = audio.set_fps(44100)
    audio.preview()
    clip.close()

def resize_with_borders(image, target_width, target_height):
    original_width, original_height = image.size
    ratio = min(target_width / original_width, target_height / original_height)
    new_size = (int(original_width * ratio), int(original_height * ratio))
    resized_image = image.resize(new_size, Image.LANCZOS)
    delta_w = target_width - new_size[0]
    delta_h = target_height - new_size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
    return ImageOps.expand(resized_image, padding, fill="black")

def monitor_stop_command():
    while not stop_event.is_set():
        command = input()
        if command.strip().lower() == 'stop':
            stop_event.set()

def main():
    parser = argparse.ArgumentParser(description="Virtual camera with media playback")
    parser.add_argument('resolution', nargs='?', default=None, help="Resolution of the camera (e.g., 1280x720)")
    parser.add_argument('media_file', help="Path to the media file (video or image)")
    parser.add_argument('-a', '--audio', nargs='?', default=None, help="Path to the audio file to play alongside the media")
    parser.add_argument('-v', '--volume', type=int, default=30, help="Volume for the audio (0-100)")
    parser.add_argument('-av', '--video_audio', type=int, choices=[0, 1], default=1, help="Audio setting for the video (0 for off, 1 for on)")
    parser.add_argument('-vv', '--video_volume', type=int, default=100, help="Volume for the video audio (0-100)")
    parser.add_argument('-l', '--loop', action='store_true', help="Loop the media")

    args = parser.parse_args()

    global stop_event
    stop_event = threading.Event()
    
    stop_thread = threading.Thread(target=monitor_stop_command)
    stop_thread.start()

    is_video = False
    try:
        video = imageio.get_reader(args.media_file, 'ffmpeg')
        is_video = True
    except Exception as e:
        print(f"Erro ao tentar abrir vídeo: {e}")
        try:
            frame = Image.open(args.media_file)
            frame = frame.convert("RGB")
        except Exception as e:
            print(f"Erro ao tentar abrir imagem: {e}")
            print("Arquivo não pode ser aberto como vídeo ou imagem.")
            return

    if is_video:
        meta_data = video.get_meta_data()
        width = meta_data['size'][0] if not args.resolution else int(args.resolution.split('x')[0])
        height = meta_data['size'][1] if not args.resolution else int(args.resolution.split('x')[1])
    else:
        width = frame.width if not args.resolution else int(args.resolution.split('x')[0])
        height = frame.height if not args.resolution else int(args.resolution.split('x')[1])

    with pyvirtualcam.Camera(width, height, 30, fmt=PixelFormat.BGR) as cam:
        print(f'Usando câmera virtual: {cam.device}')

        if args.audio:
            audio_thread = threading.Thread(target=play_audio, args=(args.audio, args.volume))
            audio_thread.start()
        elif is_video and args.video_audio == 1:
            audio_thread = threading.Thread(target=play_video_audio, args=(args.media_file, args.video_volume))
            audio_thread.start()

        if is_video:
            meta_data = video.get_meta_data()
            fps = meta_data['fps']
            while not stop_event.is_set():
                for frame in video:
                    start_time = time.time()
                    frame = np.array(frame)
                    frame = Image.fromarray(frame)
                    frame = resize_with_borders(frame, width, height)
                    frame = np.array(frame)
                    frame = frame[:, :, ::-1]
                    frame = apply_filter(frame)
                    cam.send(frame)
                    time.sleep(max(1./fps - (time.time() - start_time), 0))
                    cam.sleep_until_next_frame()
                    if stop_event.is_set():
                        break
                if not args.loop:
                    break
                video.set_image_index(0)
        else:
            frame = resize_with_borders(frame, width, height)
            frame = np.array(frame)
            frame = frame[:, :, ::-1]
            frame = apply_filter(frame)
            while not stop_event.is_set():
                cam.send(frame)
                cam.sleep_until_next_frame()

    stop_event.set()
    stop_thread.join()

if __name__ == "__main__":
    main()
