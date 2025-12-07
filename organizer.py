import os
import shutil
import yaml
from datetime import datetime

# Settings load karne ka function
def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def organize():
    config = load_config()
    # Agar config me path nahi hai to Desktop automatically lo
    desktop = config.get("desktop_path") or os.path.join(os.path.expanduser("~"), "Desktop")
    mappings = config.get("mappings", {})

    print(f"Cleaning folder: {desktop}")
    
    # Files check karna shuru
    for filename in os.listdir(desktop):
        file_path = os.path.join(desktop, filename)
        
        # Agar ye folder hai to skip karo
        if os.path.isdir(file_path):
            continue

        # File extension nikalo (e.g., .jpg, .pdf)
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        target_folder = "Others" # Default folder

        # Check karo file kis category ki hai
        for folder, extensions in mappings.items():
            if ext in extensions:
                target_folder = folder
                break
        
        # Target folder banao agar nahi hai
        target_dir = os.path.join(desktop, target_folder)
        os.makedirs(target_dir, exist_ok=True)

        # File move karo
        try:
            new_path = os.path.join(target_dir, filename)
            # Agar file pehle se waha hai to rename karo
            if os.path.exists(new_path):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_path = os.path.join(target_dir, f"{timestamp}_{filename}")
            
            shutil.move(file_path, new_path)
            print(f"Moved: {filename} -> {target_folder}")
        except Exception as e:
            print(f"Error moving {filename}: {e}")

if __name__ == "__main__":
    organize()