import os
import shutil
import json
import numpy as np
from deepface import DeepFace

# Folders
image_folder = "downloaded_images/faces_detected"  # Source folder"matched_faces"#
matched_folder = "matched_faces3"  # Destination folder
embeddings_file = "face_embeddings.json"  # Embeddings cache
reference_image_path = "IMG_2623.JPG"  # Reference image

# Create matched_faces folder if it doesn't exist
os.makedirs(matched_folder, exist_ok=True)

def load_embeddings():
    """Loads stored face embeddings from a file, skipping missing images."""
    if os.path.exists(embeddings_file):
        with open(embeddings_file, "r") as file:
            embeddings = json.load(file)
        
        # Filter out entries whose images are missing
        valid_embeddings = {
            k: v for k, v in embeddings.items() if os.path.exists(os.path.join(image_folder, k))
        }

        if len(valid_embeddings) < len(embeddings):
            print(f"Skipped {len(embeddings) - len(valid_embeddings)} missing images from embeddings.")

        return valid_embeddings
    return {}

def extract_embedding(image_path, model_name="ArcFace"):
    """Extracts a face embedding from an image."""
    try:
        embedding = DeepFace.represent(image_path, model_name=model_name)[0]['embedding']
        return np.array(embedding)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def find_matching_faces():
    """Compares the reference image's embedding to stored embeddings and moves matches."""
    embeddings = load_embeddings()  # Load cleaned embeddings
    print(f"🔍 Loaded {len(embeddings)} valid embeddings")  # Debug

    # Compute embedding for reference image
    ref_embedding = extract_embedding(reference_image_path)
    if ref_embedding is None:
        print("ERROR: Reference image embedding could not be extracted.")
        return

    for filename, target_embedding in embeddings.items():
        target_embedding = np.array(target_embedding)

        # Compute cosine similarity
        similarity = np.dot(ref_embedding, target_embedding) / (
            np.linalg.norm(ref_embedding) * np.linalg.norm(target_embedding)
        )

        print(f"Similarity with {filename}: {similarity:.4f}")  # Debug print

        if similarity > 0.5:  # Threshold for matching
            print(f"Match found: {filename} (Similarity: {similarity:.4f})")
            image_path = os.path.join(image_folder, filename)

            # Check if file exists before moving
            if os.path.exists(image_path):
                shutil.move(image_path, os.path.join(matched_folder, filename))
                print(f"Successfully moved {filename}")
            else:
                print(f"Skipping {filename}: File not found in {image_folder}")

# Run face matching
find_matching_faces()