import os
import shutil
import json
import numpy as np
from deepface import DeepFace

# Folders
image_folder = "matched_faces2"#"downloaded_images/faces_detected"
matched_folder = "matched_faces3"
embeddings_file = "face_embeddings.json"
reference_image_path = "IMG_2623.JPG" 

# Create matched_faces folder if not exists
os.makedirs(matched_folder, exist_ok=True)

def load_embeddings():
    """Loads stored face embeddings from a file."""
    if os.path.exists(embeddings_file):
        with open(embeddings_file, "r") as file:
            return json.load(file)
    return {}

def extract_embedding(image_path, model_name="ArcFace"):
    """Extracts a face embedding from the reference image."""
    try:
        embedding = DeepFace.represent(image_path, model_name=model_name)[0]['embedding']
        return np.array(embedding)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def find_matching_faces():
    """Compares the reference image's embedding to stored embeddings and moves matches."""
    embeddings = load_embeddings()  # Load cached embeddings
    print(f"🔍 Loaded {len(embeddings)} embeddings")  # Debug: Show count

    # Compute embedding for reference image
    ref_embedding = extract_embedding(reference_image_path)
    if ref_embedding is None:
        print(" ERROR: Reference image embedding could not be extracted.")
        return

    for filename, target_embedding in embeddings.items():
        target_embedding = np.array(target_embedding)

        # Compute cosine similarity
        similarity = np.dot(ref_embedding, target_embedding) / (
            np.linalg.norm(ref_embedding) * np.linalg.norm(target_embedding)
        )

        print(f"🔍 Similarity with {filename}: {similarity:.4f}")  # Debug print

        if similarity > 0.6:  # Adjust threshold if needed
            print(f" Match found: {filename} (Similarity: {similarity:.4f})")
            image_path = os.path.join(image_folder, filename)

            # Move image
            shutil.move(image_path, os.path.join(matched_folder, filename))

            # Verify move success
            if os.path.exists(os.path.join(matched_folder, filename)):
                print(f"Successfully moved {filename}")
            else:
                print(f"Move failed for {filename}")

# Run face matching
find_matching_faces()