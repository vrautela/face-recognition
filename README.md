# A project to recognize people and play theme music for them in real-time 

## Usage
1. Open Powershell and Run as Administrator to use usbipd commands to attach the USB webcam to WSL
    - If the commands fail with an error message about vhci_hcd, then open WSL and run `sudo modprobe vhci_hcd`
2. Open WSL and navigate to face-recognition
3. Run `ls /dev/video*` to see what file the camera has been assigned. If there are multiple then run the `v4l2-ctl --list-devices` and `v4l2-ctl --device=/dev/video0 --list-formats` commands to figure out which one it actually is
4. Edit face_detection.py so that the line cv2.VideoCapture(N) matches the device file of the camera (/dev/videoN)
5. Run face_detection.py

## Adding new people
1. Create a subfolder in the photo_dump folder with the person's name and populate it with pictures
2. Re-run extract_face_embeddings.py

## Installation notes:
- You need to have CMake installed in order to install face_recognition 
- This is the documentation for installing face_detection on Raspberry Pi (including required dependences): https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65
- I also had to install the required dependencies for opencv on Raspberry Pi: https://opencv.org/blog/raspberry-pi-with-opencv/

