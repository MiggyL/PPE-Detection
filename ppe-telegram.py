import os
# Import configurations from config.py
from config import IMAGE_DIR, IMAGE_ARCH_DIR

import asyncio
from telegram import Bot
import logging
import shutil  # Import shutil for moving files
import schedule
import threading
import time

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot token and chat_id
bot_token = "6985782331:AAEuLM3qS8TxezDWrOBKCXXQvdA5Af315nE"
chat_id = "-1002485388728"

# Initialize the bot
bot = Bot(token=bot_token)

# Create the archive directory if it doesn't exist
if not os.path.exists(IMAGE_ARCH_DIR):
    os.makedirs(IMAGE_ARCH_DIR)

# Semaphore for concurrency control
semaphore = asyncio.Semaphore(1)

async def send_image(image_path):
    async with semaphore:
        try:
            with open(image_path, 'rb') as image:
                await bot.send_photo(chat_id=chat_id, photo=image)
            logger.info(f"Image sent successfully: {image_path}")

            # Move the file to the archive directory after successful send
            shutil.move(image_path, os.path.join(IMAGE_ARCH_DIR, os.path.basename(image_path)))
            logger.info(f"Image moved to archive: {os.path.join(IMAGE_ARCH_DIR, os.path.basename(image_path))}")
            
        except Exception as e:
            logger.error(f"Failed to send image {image_path}: {e}")

def find_and_send_oldest_image(loop):
    # Find the oldest image
    files = [os.path.join(IMAGE_DIR, filename) for filename in os.listdir(IMAGE_DIR) if filename.endswith(".jpg")]
    oldest_image = min(files, key=os.path.getmtime) if files else None

    # If there's an oldest image, schedule it to be sent in the event loop
    if oldest_image:
        asyncio.run_coroutine_threadsafe(send_image(oldest_image), loop)

def start_scheduler(loop):
    # Every 10 seconds, send files in order starting from oldest until no files left
    schedule.every(10).seconds.do(lambda: find_and_send_oldest_image(loop))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    # Run the scheduler in a separate thread, passing the main event loop
    scheduler_thread = threading.Thread(target=start_scheduler, args=(loop,), daemon=True)
    scheduler_thread.start()

    # Run the asyncio event loop
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()