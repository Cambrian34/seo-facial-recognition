import os
import json
import numpy as np
from deepface import DeepFace

# Folders
image_folder = "downloaded_images/faces_detected"#"downloaded_images/faces_detected"
embeddings_file = "face_embeddings.json"
DUPLICATE_THRESHOLD = 0.99  # Adjust as needed

def extract_embedding(image_path, model_name="ArcFace"):
    """Extracts a face embedding from an image using DeepFace."""
    try:
        embedding = DeepFace.represent(image_path, model_name=model_name)[0]['embedding']
        return np.array(embedding)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def load_embeddings():
    """Loads stored face embeddings from a file."""
    if os.path.exists(embeddings_file):
        with open(embeddings_file, "r") as file:
            return json.load(file)
    return {}

def save_embeddings(embeddings):
    """Saves face embeddings to a file."""
    with open(embeddings_file, "w") as file:
        json.dump(embeddings, file)

def is_duplicate(new_embedding, existing_embeddings):
    """Checks if the new embedding is a duplicate of any existing embeddings."""
    for stored_embedding in existing_embeddings.values():
        stored_embedding = np.array(stored_embedding)
        similarity = np.dot(new_embedding, stored_embedding) / (
            np.linalg.norm(new_embedding) * np.linalg.norm(stored_embedding)
        )

        if similarity > DUPLICATE_THRESHOLD:
            return True  # Found a duplicate
    return False  # No duplicate found

def cache_all_images():
    """Extracts embeddings for all images and saves them, avoiding duplicates. Tracks completion rate."""
    embeddings = load_embeddings()  # Load existing cache
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    total_images = len(image_files)
    completed = len(embeddings)

    print(f"📸 Total images: {total_images} | ✅ Already cached: {completed}")

    for i, filename in enumerate(image_files):
        image_path = os.path.join(image_folder, filename)

        if filename in embeddings:
            continue  # Skip already cached images

        embedding = extract_embedding(image_path)
        if embedding is not None:
            if is_duplicate(embedding, embeddings):
                print(f" Duplicate detected: {filename} (skipped)")
            else:
                embeddings[filename] = embedding.tolist()
                completed += 1  # Update count
                print(f"[{completed}/{total_images}] Cached: {filename}")

        # Show progress percentage
        progress = (completed / total_images) * 100
        print(f" Completion: {progress:.2f}%")

    # Save updated embeddings
    save_embeddings(embeddings)
    print(f"All images cached in {embeddings_file}")

# Run caching process
cache_all_images()