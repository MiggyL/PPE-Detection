# config.py

import os

# Directory containing the videos
PPE_CCTV_HOME = os.environ.get('PPE_CCTV_HOME')
IMAGE_SRC = os.path.join(PPE_CCTV_HOME, 'images_src')
IMAGE_DIR = os.path.join(PPE_CCTV_HOME, 'images')
IMAGE_ARCH_DIR = os.path.join(PPE_CCTV_HOME, 'image_archives')
VIDEO_DIR = os.path.join(PPE_CCTV_HOME, 'videos')
VIDEO_ARCH_DIR = os.path.join(PPE_CCTV_HOME, 'video_archives')
DATA = os.path.join(PPE_CCTV_HOME, 'all_data')