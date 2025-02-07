import requests
import os
from config import GET_IMAGES_API, MARK_RECEIVED_API

LOCAL_SAVE_PATH = "./downloaded_images"  # 本地保存目录
os.makedirs(LOCAL_SAVE_PATH, exist_ok=True)

def fetch_unprocessed_images():
    """请求服务器获取未处理的图片列表"""
    try:
        response = requests.get(GET_IMAGES_API)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success":
                return data["images"]
        print(f"获取图片列表失败: {response.text}")
    except requests.RequestException as e:
        print(f"请求失败: {e}")
    return []

def download_image(image_url, file_name):
    """下载图片"""
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(LOCAL_SAVE_PATH, file_name)
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"✅ 图片下载成功: {file_name}")
            return file_path
        print(f"❌ 下载失败: {image_url}")
    except requests.RequestException as e:
        print(f"❌ 下载请求失败: {e}")
    return None

def mark_images_as_received(image_ids):
    """向服务器发送请求，标记已接收的图片"""
    try:
        response = requests.post(MARK_RECEIVED_API, data={'image_id': image_ids})
        if response.status_code == 200:
            print("✅ 已标记图片为已接收")
        else:
            print(f"❌ 服务器标记失败: {response.text}")
    except requests.RequestException as e:
        print(f"❌ 服务器请求失败: {e}")
