import os
from pathlib import Path



def check_log(BASE_DIR):  
    # BASE_DIR = Path(__file__).resolve().parent
    LOG_DIR = Path(BASE_DIR, 'logs')
    LOG_FILE = LOG_DIR / 'django.log'

    if not LOG_DIR.exists():
        LOG_DIR.mkdir(parents=True, exist_ok=True)

    if not LOG_FILE.exists():
        LOG_FILE.touch(exist_ok=True)
        os.chmod(LOG_FILE, 0o774)  
        
def set_permissions_recursively(path, mode):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            os.chmod(os.path.join(root, dir), mode)
        for file in files:
            os.chmod(os.path.join(root, file), mode)
        
def check_media(BASE_DIR):
    MEDIA_DIR = Path(BASE_DIR, 'media')
    IMAGES_DIR = Path(MEDIA_DIR, 'images')
    FILES_DIR = Path(MEDIA_DIR, 'files')
    
    if not MEDIA_DIR.exists():
        MEDIA_DIR.mkdir(parents=True, exist_ok=True)
        
    if not IMAGES_DIR.exists():
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        
    if not FILES_DIR.exists():
        FILES_DIR.mkdir(parents=True, exist_ok=True)
        
    set_permissions_recursively(MEDIA_DIR, 0o774)
