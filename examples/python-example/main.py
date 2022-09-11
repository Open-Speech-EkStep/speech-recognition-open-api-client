import socketio
from urllib.parse import urlencode
import pyaudio

class BhashiniStreamingClient:
    def __init__(self, socket_url: str, language_code: str, streaming_rate: int = 640, sampling_rate: int = 16000, bytes_per_sample: int = 2, post_processors: list = []) -> None:
        self.language_code = language_code
        self.streaming_rate = streaming_rate
        self.sampling_rate = sampling_rate
        self.bytes_per_sample = bytes_per_sample

        self.sio_client = self._get_client(
            on_ready=self.start_transcribing_from_mic
        )
        query_string = urlencode({
            "language": language_code,
            "samplingRate": sampling_rate,
            "postProcessors": post_processors,
        })
        self.sio_client.connect(
            url=socket_url + "?" + query_string,
            transports=["websocket", "polling"],
        )

        # states
        self.audio_stream = None
        self.is_running = False

    def _get_client(self, on_ready=None) -> socketio.Client:
        sio = socketio.Client(reconnection_attempts=5)

        @sio.event
        def connect():
            print("Socket connected with ID:", sio.get_sid())
            sio.emit("connect_mic_stream")

        @sio.on('connect-success')
        def ready_to_stream(response="", language=""):
            # print("Server ready to receive data from client")
            if on_ready:
                on_ready()
        
        @sio.on('response')
        def handle_response(response, language):
            print(response)
        
        @sio.on('terminate')
        def terminate(response="", language=""):
            sio.disconnect()

        @sio.event
        def connect_error(data):
            print("The connection failed!")

        @sio.event
        def disconnect():
            print("Stream disconnected!")

        return sio
    
    def stop(self) -> None:
        self.is_running = False
        print("Stopping...")
        if self.audio_stream:
            self.audio_stream.stop_stream()
        self.transmit_end_of_stream()

        # Wait till stream is disconnected
        self.sio_client.wait()
        # self.sio_client.disconnect()

    def _create_audio_stream(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(self.bytes_per_sample),
            channels=1,
            rate=self.sampling_rate,
            input=True,
            output=False,
            frames_per_buffer=self.streaming_rate,
            stream_callback=self.recorder_callback,
        )
        return stream
    
    def start_transcribing_from_mic(self):
        self.is_running = True
        self.audio_stream = self._create_audio_stream()
        print("START SPEAKING NOW!!!")
        # self.audio_stream.start_stream()
        # while self.is_running:
        #     data = self.stream.read(self.streaming_rate)
        #     self.sio_client.emit("mic_data", data, self.language_code, self.is_running, self.is_running)
    
    def recorder_callback(self, in_data, frame_count, time_info, status_flags):
        self.sio_client.emit("mic_data", (in_data, self.language_code, self.is_running, False))
        return (None, pyaudio.paContinue)
    
    def transmit_end_of_stream(self):
        # Convey endOfSpeech
        self.sio_client.emit("mic_data", (None, self.language_code, self.is_running, False))
        # Convey endOfStream
        self.sio_client.emit("mic_data", (None, self.language_code, self.is_running, True))


if __name__ == "__main__":
    streamer = BhashiniStreamingClient(
        socket_url="http://216.48.183.5:9009",
        language_code="hi",
        streaming_rate=160,
        post_processors=['numbers-only'],
    )

    input("(Press Enter to Stop) ")
    streamer.stop()
