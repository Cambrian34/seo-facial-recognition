import os
import shutil
from deepface import DeepFace

# Folders
image_folder ="matched_faces2"# "downloaded_images/faces_detected"  # Where images are stored
matched_folder = "matched_faces"  # Where matched images will be stored
reference_image_path = "IMG_2623.JPG"  # Image to compare against

# Create matched_faces folder if it doesn't exist
os.makedirs(matched_folder, exist_ok=True)

def find_matching_faces():
    """Compare the reference image to downloaded images and move matches to a new folder."""
    for filename in os.listdir(image_folder):
        image_path = os.path.join(image_folder, filename)

        try:
            # Use a more accurate model (Facenet or ArcFace)
            result = DeepFace.verify(reference_image_path, image_path, model_name="ArcFace")

            if result["verified"]:
                print(f"✅ Match found: {filename}")
                
                # Move matched image to "matched_faces" folder
                shutil.move(image_path, os.path.join(matched_folder, filename))
                print(f"🔄 Moved {filename} → {matched_folder}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

# Run face matching
find_matching_faces()