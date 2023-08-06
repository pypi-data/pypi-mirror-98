import pyaudio
import threading


class Listener:
    """
    Continuously listen audio as chunks in a different thread.
    """

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    def __init__(self):
        # used for recording audio for wake up word detection
        self.wake_up_frames = []
        # used for recording audio for speech-to-text
        self.stt_frames = []
        self.listening_thread = None
        self.setup_audio_stream()
        self.mode = "wakeword"

    def setup_audio_stream(self):
        p = pyaudio.PyAudio()

        self.stream = p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)

    def start_listening(self):
        listening_thread = threading.Thread(target=self.continuously_listen, args=())
        listening_thread.start()

    def continuously_listen(self):
        while True:
            data = self.stream.read(self.CHUNK)
            if self.mode == "wakeword":
                self.wake_up_frames.append(data)
            elif self.mode == "stt":
                self.stt_frames.append(data)