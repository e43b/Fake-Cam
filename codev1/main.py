import imageio
import numpy as np
from PIL import Image
import pyvirtualcam
from pyvirtualcam import PixelFormat

def apply_filter(frame):
    # Exemplo de filtro que não altera a cor
    # Aqui você pode aplicar qualquer outro filtro que mantenha as cores
    return frame

def main():
    file_path = input("Insira o caminho para o vídeo ou imagem: ")
    is_video = False

    try:
        # Tenta abrir como vídeo
        video = imageio.get_reader(file_path, 'ffmpeg')
        is_video = True
    except Exception as e:
        print(f"Erro ao tentar abrir vídeo: {e}")
        # Se falhar, tenta abrir como imagem
        try:
            frame = Image.open(file_path)
            frame = frame.convert("RGB")  # Certifica-se de que a imagem está no formato RGB
        except Exception as e:
            print(f"Erro ao tentar abrir imagem: {e}")
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
                    # Converte o frame para numpy array
                    frame = np.array(frame)
                    # Converte de RGB para BGR (necessário para pyvirtualcam)
                    frame = frame[:, :, ::-1]
                    # Aplica o filtro ao frame
                    frame = apply_filter(frame)
                    cam.send(frame)
                    cam.sleep_until_next_frame()
            else:
                # Converte o frame para numpy array
                frame = np.array(frame)
                # Converte de RGB para BGR (necessário para pyvirtualcam)
                frame = frame[:, :, ::-1]
                # Aplica o filtro à imagem
                frame = apply_filter(frame)
                while True:
                    cam.send(frame)
                    cam.sleep_until_next_frame()

if __name__ == "__main__":
    main()
