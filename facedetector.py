import cv2
import os
import shutil
from mtcnn import MTCNN

# Initialize MTCNN face detector
detector = MTCNN()

# Input folder
image_folder = "downloaded_images"

# Output folders
faces_folder = "downloaded_images/faces_detected"
no_faces_folder = "downloaded_images/no_faces_detected"

# Ensure output directories exist
os.makedirs(faces_folder, exist_ok=True)
os.makedirs(no_faces_folder, exist_ok=True)

def detect_faces(image_path):
    """Detects if an image contains a face using MTCNN."""
    try:
        img = cv2.imread(image_path)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faces = detector.detect_faces(rgb_img)

        return len(faces) > 0  # True if a face is detected
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

def sort_images():
    """Sorts images into 'faces_detected' and 'no_faces_detected' folders."""
    for filename in os.listdir(image_folder):
        image_path = os.path.join(image_folder, filename)

        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            continue  # Skip non-image files

        if detect_faces(image_path):
            shutil.move(image_path, os.path.join(faces_folder, filename))
            print(f"Face detected: {filename} → Moved to '{faces_folder}'")
        else:
            shutil.move(image_path, os.path.join(no_faces_folder, filename))
            print(f"No face detected: {filename} → Moved to '{no_faces_folder}'")

# Run sorting
sort_images()