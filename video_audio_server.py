import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
gi.require_version('GLib', '2.0')
from gi.repository import Gst, GstRtspServer, GLib

VIDEO_DEVICE = '/dev/video0'  # Change to your video device
AUDIO_DEVICE = 'default'       # Change to your audio device
SERVER_IP = '10.5.2.31'     # Change to your IP address
PORT = 8554                   # RTSP server port

class VideoStreamServer(GstRtspServer.RTSPMediaFactory):
    def __init__(self):
        super(VideoStreamServer, self).__init__()
        self.set_shared(True)

    def do_create_element(self, url):
        pipeline_str = (
            f"v4l2src device={VIDEO_DEVICE} ! videoconvert ! video/x-raw,format=I420 ! "
            f"x264enc tune=zerolatency bitrate=500 speed-preset=ultrafast ! rtph264pay name=pay0 pt=96 "
            f"alsasrc device={AUDIO_DEVICE} ! audioconvert ! audioresample ! opusenc ! rtpopuspay name=pay1 pt=97"
        )
        return Gst.parse_launch(pipeline_str)

class Server:
    def __init__(self):
        Gst.init(None)
        self.server = GstRtspServer.RTSPServer()
        self.server.props.service = str(PORT)
        self.server.set_address(SERVER_IP)

        factory = VideoStreamServer()
        self.server.get_mount_points().add_factory("/video_stream", factory)
        self.server.attach(None)

    def run(self):
        print(f"RTSP server is running at rtsp://{SERVER_IP}:{PORT}/video_stream")
        loop = GLib.MainLoop()
        loop.run()

if __name__ == "__main__":
    server = Server()
    server.run()