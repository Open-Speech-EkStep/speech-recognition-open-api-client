import socketio
from urllib.parse import urlencode
import signal
import pyaudio

class BhashiniStreamingClient:
    def __init__(self, socket_url: str, language_code: str, streaming_rate: int = 640, sampling_rate: int = 16000, bytes_per_sample: int = 2, post_processors: list = [], auto_start: bool = True) -> None:
        self.language_code = language_code
        self.streaming_rate = streaming_rate
        self.sampling_rate = sampling_rate
        self.bytes_per_sample = bytes_per_sample

        self.socket_client = self._get_client(
            on_ready=self.start_transcribing_from_mic if auto_start else None
        )
        query_string = urlencode({
            "language": language_code,
            "samplingRate": sampling_rate,
            "postProcessors": post_processors,
        })
        self.socket_client.connect(
            url=socket_url + "?" + query_string,
            transports=["websocket", "polling"],
        )

        # states
        self.audio_stream = None
        self.is_active = False

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
        self.is_active = False
        print("Stopping...")
        if self.audio_stream:
            self.audio_stream.stop_stream()
        self._transmit_end_of_stream()

        # Wait till stream is disconnected
        self.socket_client.wait()

    def force_disconnect(self, sig=None, frame=None) -> None:
        self.socket_client.disconnect()

    def _create_audio_stream(self) -> pyaudio.Stream:
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
    
    def start_transcribing_from_mic(self) -> None:
        self.is_active = True
        self.audio_stream = self._create_audio_stream()
        print("START SPEAKING NOW!!!")
        # self.audio_stream.start_stream()
        # while self.is_active:
        #     data = self.stream.read(self.streaming_rate)
        #     self.socket_client.emit("mic_data", (data, self.language_code, self.is_active, False))
    
    def recorder_callback(self, in_data, frame_count, time_info, status_flags) -> tuple:
        self.socket_client.emit("mic_data", (in_data, self.language_code, self.is_active, False))
        return (None, pyaudio.paContinue)
    
    def _transmit_end_of_stream(self) -> None:
        # Convey that speaking has stopped
        self.socket_client.emit("mic_data", (None, self.language_code, self.is_active, False))
        # Convey that we can close the stream safely
        self.socket_client.emit("mic_data", (None, self.language_code, self.is_active, True))


if __name__ == "__main__":
    streamer = BhashiniStreamingClient(
        socket_url="<SOCKET_SERVER_ENDPOINT>",
        language_code="<LANG_CODE>",
        streaming_rate=160,
        sampling_rate=8000,
        post_processors=[],
        auto_start=True,
    )
    signal.signal(signal.SIGINT, streamer.force_disconnect)

    input("(Press Enter to Stop) ")
    streamer.stop()
