from threading import Thread
import cv2
import numpy as np
from ultralytics import YOLO
import subprocess

class Inferencer(Thread):
    def __init__(self):
        super().__init__()
        # Load the YOLO model
        self.model = YOLO('/home/helix/Desktop/helix_yolo.py')  # Path to your optimized ONNX model
        self.camera = cv2.VideoCapture('/dev/video0')
        # Set up RTP stream using FFmpeg
        self.ffmpeg_cmd = [
            'ffmpeg',
            '-f', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', '640x480',  # Adjust resolution as needed
            '-i', '-',
            '-f', 'rtp',
            '-sdp_file', 'stream.sdp',
            'rtp://10.136.89.17:1234'
        ]
        self.ffmpeg_process = subprocess.Popen(
            self.ffmpeg_cmd,
            stdin=subprocess.PIPE
        )
        self.is_on = True

    def run(self):
        while self.is_on:
            ret, frame = self.camera.read()
            if not ret:
                continue
                
            # Run inference
            results = self.model(frame)
            
            # Draw detections on frame
            annotated_frame = results[0].plot()
            
            # Send frame to RTP stream
            self.ffmpeg_process.stdin.write(annotated_frame.tobytes())

    def on(self):
        self.start()

    def off(self):
        self.is_on = False
        self.camera.release()
        self.ffmpeg_process.stdin.close()
        self.ffmpeg_process.terminate()

class InferenceContainer:
    def __init__(self):
        self.inferencer = None

    def on(self):
        if not self.inferencer or not self.inferencer.is_alive():
            self.inferencer = Inferencer()
            self.inferencer.on()

    def off(self):
        if self.inferencer and self.inferencer.is_alive():
            self.inferencer.off()
            self.inferencer = None

if __name__ == "__main__":
    container = InferenceContainer()
    container.on()
    
    try:
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        container.off()
