# A project to recognize people and play theme music for them in real-time 

## Setup

1. Create a folder called photo_dump in the root directory of the repo with a subfolder for each person you want to recognize. Each subfolder should contain images of that person and no other files.
1. Create a folder called walk_up_music in the root directory of the repo. Add audio files for each person where the file name format is `{person_name}.{audio_file_type}`. Example: if you have the folder `face_recognition/photo_dump/VR` then one possible audio file path could be `face_recognition/walk_up_music/VR.mp3` 

## Usage (on WSL)
1. Open Powershell and Run as Administrator to use usbipd commands to attach the USB webcam to WSL
    - If the commands fail with an error message about vhci_hcd, then open WSL and run `sudo modprobe vhci_hcd`
1. Open WSL and navigate to face-recognition
1. Run `python extract_face_embeddings.py` if you have edited the photo_dump folder
1. Run `ls /dev/video*` to see what file the camera has been assigned. If there are multiple then run the `v4l2-ctl --list-devices` and `v4l2-ctl --device=/dev/video0 --list-formats` commands to figure out which one it actually is
1. Edit face_detection.py so that the line cv2.VideoCapture(N) matches the device file of the camera (/dev/videoN)
1. Run `python face_detection.py`

## Adding new people
1. Create a subfolder in the photo_dump folder with the person's name and populate it with pictures
1. Re-run extract_face_embeddings.py

## Installation notes:
- You need to have CMake installed in order to install face_recognition 
- This is the documentation for installing face_detection on Raspberry Pi (including required dependences): https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65
- I also had to install the required dependencies for opencv on Raspberry Pi: https://opencv.org/blog/raspberry-pi-with-opencv/

