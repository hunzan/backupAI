import os
from datetime import datetime

BACKUP_FOLDER = "backups"

def ensure_folder(category):
    folder_path = os.path.join(BACKUP_FOLDER, category)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def save_chat(content, category):
    folder = ensure_folder(category)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"{timestamp}_{category}.txt"
    filepath = os.path.join(folder, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath
