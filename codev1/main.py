import imageio
import numpy as np
from PIL import Image, ImageOps
import pyvirtualcam
from pyvirtualcam import PixelFormat

def apply_filter(frame):
    # Converte o frame para escala de cinza
    gray_frame = ImageOps.grayscale(frame)
    # Converte o frame de volta para RGB
    return gray_frame.convert("RGB")

def main():
    file_path = input("Insira o caminho para o vídeo ou imagem: ")
    is_video = False
    try:
        # Tenta abrir como vídeo
        video = imageio.get_reader(file_path, 'ffmpeg')
        is_video = True
    except Exception as e:
        # Se falhar, tenta abrir como imagem
        try:
            frame = Image.open(file_path)
        except Exception as e:
            print("Arquivo não pode ser aberto como vídeo ou imagem.")
            return
    
    if is_video:
        meta_data = video.get_meta_data()
        width = meta_data['size'][0]
        height = meta_data['size'][1]
    else:
        width, height = frame.size

    with pyvirtualcam.Camera(width, height, 30, fmt=PixelFormat.BGR) as cam:
        print(f'Usando câmera virtual: {cam.device}')

        while True:
            if is_video:
                for frame in video:
                    # Converte o frame para PIL Image
                    frame = Image.fromarray(frame)
                    # Aplica o filtro ao frame
                    frame = apply_filter(frame)
                    # Converte o frame para numpy array
                    frame = np.array(frame)
                    cam.send(frame)
                    cam.sleep_until_next_frame()
            else:
                # Aplica o filtro à imagem
                frame = apply_filter(frame)
                # Converte o frame para numpy array
                frame = np.array(frame)
                while True:
                    cam.send(frame)
                    cam.sleep_until_next_frame()

if __name__ == "__main__":
    main()
