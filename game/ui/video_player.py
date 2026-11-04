import pygame
from moviepy import VideoFileClip


class VideoPlayer:
    def __init__(self, archivo_video, tamaño):
        self.clip = VideoFileClip(archivo_video)
        self.frames = self.clip.iter_frames(fps=30)
        self.finished = False
        self.tamaño = tamaño
        self.audio_iniciado = False

        # Guardar el último frame mostrado
        self.last_frame = None

    def draw(self, window):
        # Si el vídeo se ha acabado  seguimos mostrando el último frame parado
        if self.finished:
            if self.last_frame:
                window.blit(self.last_frame, (0, 0))
            return

        # Iniciar el audio
        if not self.audio_iniciado:

            pygame.mixer.music.load(
                "game/ui/assets/videos/intro.mp3"
            )
            pygame.mixer.music.play()
            self.audio_iniciado = True
        try:
            frame = next(self.frames)
            frame_surface = pygame.surfarray.make_surface(
                frame.swapaxes(0, 1)
            )

            frame_surface = pygame.transform.scale(
                frame_surface,
                self.tamaño
            )

            # Guardar el último frame
            self.last_frame = frame_surface.copy()
            window.blit(frame_surface, (0, 0))
            
        except StopIteration:
            pygame.mixer.music.stop()
            self.finished = True