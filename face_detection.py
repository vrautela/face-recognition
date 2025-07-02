import face_recognition
import cv2
import pickle
import pygame
import threading
import time

# Initialize pygame for music
pygame.mixer.init()

# number of seconds after which to allow repeat recognition of an individual 
RECENCY_THRESHOLD = 30 


def seen_too_recently(last_seen: dict[str, float], name: str) -> bool:
    """Was the given person seen too recently to acknowledge them again?"""
    return name in last_seen and time.time() - last_seen[name] < RECENCY_THRESHOLD


def audio_file_path(name: str) -> str:
    """A helper function to return the path of a person's audio file"""
    return f'walk_up_music/{name}.mp3'


def play_music(name: str):
    """Play a person's music"""
    pygame.mixer.music.load(audio_file_path(name))
    pygame.mixer.music.play()

    # Wait until the music has finished playing
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    print(f"Finished playing music for {name}")


def main():
    with open('known_faces.pkl', 'rb') as f:
        known_face_encodings, known_face_names = pickle.load(f)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera properly. Exiting now...")
        exit()

    # NOTE: this setup is super important and webcam-dependent
    # Set the resolution (use one of the supported resolutions, e.g., 640x480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # Set the pixel format (MJPEG should work well with most webcams)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    # dictionary storing person name and last time they were seen
    last_seen: dict[str] = dict()
    # queue to keep track of whose walk up music to play
    music_queue: list[str] = []

    while True:
        ret, frame = cap.read()

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                friend_name = known_face_names[first_match_index]
                if not seen_too_recently(last_seen, friend_name):
                    last_seen[friend_name] = time.time()
                    cv2.putText(frame, f"Welcome, {friend_name}!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    if friend_name not in music_queue:
                        music_queue.append(friend_name)

        if music_queue and not pygame.mixer.music.get_busy():
            current_person = music_queue.pop(0)
            print(f"Playing music for {current_person}")
            music_thread = threading.Thread(target=play_music, args=(current_person,))
            music_thread.start()

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()