import face_recognition
import cv2
import pickle
import time
# import pygame

# Initialize pygame for music
# pygame.mixer.init()

RECENCY_THRESHOLD = 5 # number of seconds after which to allow repeat recognition of an individual 

def seen_too_recently(last_seen: dict[str, float], name: str) -> bool:
    return name in last_seen and time.time() - last_seen[name] < RECENCY_THRESHOLD


def main():
    # Load the face encodings and names from the saved file
    with open('known_faces.pkl', 'rb') as f:
        known_face_encodings, known_face_names = pickle.load(f)

    # Initialize video capture (camera)
    cap = cv2.VideoCapture(0)

    # NOTE: this setup is super important and webcam-dependent
    # Set the resolution (use one of the supported resolutions, e.g., 640x480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # Set the pixel format (MJPEG should work well with most webcams)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    # dictionary storing person name and last time they were seen
    last_seen: dict[str] = dict()


    while True:
        # Capture a frame from the video feed
        ret, frame = cap.read()

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            if True in matches:
                first_match_index = matches.index(True)
                friend_name = known_face_names[first_match_index]
                if not seen_too_recently(last_seen, friend_name):
                    last_seen[friend_name] = time.time()
                    cv2.putText(frame, f"Welcome, {friend_name}!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    music_file = f"{friend_name}_theme.mp3"

                # Play the associated theme music
                # pygame.mixer.music.load(music_file)
                # pygame.mixer.music.play()

                # Display the name of the recognized friend

        # Display the video frame
        cv2.imshow("Video", frame)

        # Exit condition
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()