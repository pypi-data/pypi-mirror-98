from aiotcloud.aicam import *
from aicam.aitool import detect_marker,detect_trace

cam = AiCam(AiCam.WEB_MJPEG)
cam.connect("http://admin:admin@10.55.19.148:8081/video")

while True:
    picture = cam.get_picture()
    cam.show(picture)
