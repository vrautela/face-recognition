import face_recognition
import os
import pickle

# Define the path to the directory containing the images
friends_folder = 'photo_dump/'

# Create a dictionary to store encodings and corresponding names
known_face_encodings = []
known_face_names = []

# Loop through each friend's folder and load images for encoding
for friend_name in os.listdir(friends_folder):
    friend_folder_path = os.path.join(friends_folder, friend_name)
    
    if os.path.isdir(friend_folder_path):
        for image_file in os.listdir(friend_folder_path):
            image_path = os.path.join(friend_folder_path, image_file)
            image = face_recognition.load_image_file(image_path)
            
            # Encode the face and append the encoding and name to the database
            encodings = face_recognition.face_encodings(image)
            if encodings:  # Check if any face is detected
                for encoding in encodings:
                    known_face_encodings.append(encoding)
                    known_face_names.append(friend_name)

# Save the encodings and names to a file (using pickle for serialization)
with open('known_faces.pkl', 'wb') as f:
    pickle.dump((known_face_encodings, known_face_names), f)