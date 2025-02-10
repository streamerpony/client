import requests
from config import UPLOAD_PROCESSED_API
import os

UPLOAD_URL = UPLOAD_PROCESSED_API


def upload_processed_image(image_id, processed_file_path):
    """
    上传本地处理后的图像到服务器，并更新其状态
    :param image_id: 服务器分配的图像 ID
    :param processed_file_path: 本地处理后图像的文件路径
    :return: 是否上传成功
    """
    if not os.path.exists(processed_file_path):
        print(f"❌ 文件不存在: {processed_file_path}")
        return False

    with open(processed_file_path, "rb") as file:
        files = {"file": file}
        data = {"image_id": image_id}
        print(f"📤 正在上传处理后的图片: {processed_file_path}")

        try:
            response = requests.post(UPLOAD_URL, files=files, data=data)
            response_data = response.json()

            if response.status_code == 200 and response_data.get("status") == "success":
                print(f"✅ 上传成功: {response_data['file_path']}")
                return True  # 返回 True 表示上传成功
            else:
                print(f"❌ 上传失败: {response_data.get('message', '未知错误')}")
                return False  # 上传失败返回 False

        except requests.RequestException as e:
            print(f"❌ 网络错误: {e}")
            return False  # 网络请求异常时返回 False
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            return False  # 其他异常时返回 False
