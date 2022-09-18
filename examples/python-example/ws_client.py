from websocket import create_connection, WebSocket
import json
from urllib.parse import urlencode
import signal
import pyaudio

class BhashiniStreamingClient_WebSocket:
    '''
    Communication with EngineIO-server using websocket-client instead of SocketIO

    TODO: Implement using `WebSocketApp` for async communication
    '''
    def __init__(self, socket_url: str, language_code: str, streaming_rate: int = 640, sampling_rate: int = 16000, bytes_per_sample: int = 2, post_processors: list = [], auto_start: bool = False) -> None:
        # Parameters
        self.language_code = language_code
        self.streaming_rate = streaming_rate
        self.sampling_rate = sampling_rate
        self.bytes_per_sample = bytes_per_sample

        # states
        self.audio_stream = None
        self.is_active = False

        query_string = urlencode({
            "language": language_code,
            "samplingRate": sampling_rate,
            "postProcessors": post_processors,
            "EIO": 4,
            "transport": "websocket",
        })

        full_url = socket_url + "/socket.io/" + "?" + query_string
        self.socket_client = self._get_client(full_url)

        if auto_start:
            self.start_transcribing_from_mic()
        
    
    def _get_client(self, socket_url: str) -> WebSocket:
        socket_client = create_connection(socket_url, skip_utf8_validation=True)
        connection_response = socket_client.recv()
        if connection_response[0] != "0":
            raise Exception("EngineIO Connection unsuccessful: " + connection_response)
        connection_response = json.loads(connection_response[1:])

        socket_client.send('40')
        handshake_response = socket_client.recv()
        if handshake_response[:2] != "40":
            raise Exception("EngineIO Handshake unsuccessful: " + handshake_response)
        handshake_response = json.loads(handshake_response[2:])
        socket_client.sid = handshake_response["sid"]

        socket_client.send('42["connect_mic_stream"]')
        stream_state_response = socket_client.recv()
        if stream_state_response[:2] != "42" or 'connect-success' not in stream_state_response:
            raise Exception("EngineIO was unable to create a stream: " + stream_state_response)

        return socket_client
    
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
    
    def recorder_callback(self, in_data, frame_count, time_info, status_flags) -> tuple:
        if self.is_active:
            # self.socket_client.emit("mic_data", (in_data, self.language_code, self.is_active, False))
            self.socket_client.send('451-["mic_data",{"_placeholder":true,"num":0},"%s",true,false]' % self.language_code)
            self.socket_client.send_binary(in_data)
        return (None, pyaudio.paContinue)
    
    def start_transcribing_from_mic(self) -> None:
        self.is_active = True
        self.audio_stream = self._create_audio_stream()
        print("START SPEAKING NOW!!!")
        # self.audio_stream.start_stream()

        while True:
            message = self.socket_client.recv()

            if message == '2': # ping
                self.socket_client.send('3') # pong
            
            elif message[:2] == '42':
                message_array = json.loads(message[2:])
                if message_array[0] == 'terminate':
                    self.socket_client.close()
                    break
                elif message_array[0] == 'response':
                    self.handle_output(message_array[1])
                else:
                    raise Exception("Unknown message event: " + message_array[0])
            else:
                raise Exception("Unexpected message: " + message)
    
    def handle_output(self, output) -> None:
        print(output)

    def stop(self, sig=None, frame=None) -> None:
        print("Stopping...")
        if self.audio_stream:
            self.audio_stream.stop_stream()
        self.is_active = False
        self._transmit_end_of_stream()
    
    def _transmit_end_of_stream(self) -> None:
        # Convey that speaking has stopped
        self.socket_client.send('42["mic_data",null,"%s",false,false]' % self.language_code)

        # Convey that we can close the stream safely
        self.socket_client.send('42["mic_data",null,"%s",false,true]' % self.language_code)

    def force_disconnect(self, sig=None, frame=None) -> None:
        self.socket_client.disconnect()

if __name__ == "__main__":
    streamer = BhashiniStreamingClient_WebSocket(
        socket_url="<SOCKET_SERVER_ENDPOINT>",
        language_code="<LANG_CODE>",
        streaming_rate=160,
        sampling_rate=8000,
        post_processors=[]
    )

    signal.signal(signal.SIGINT, streamer.stop)
    print("(Press Ctrl+C to stop)")

    streamer.start_transcribing_from_mic()
    # try:
    #     streamer.start_transcribing_from_mic()
    # except KeyboardInterrupt:
    #     streamer.stop()
