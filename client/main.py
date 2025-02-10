from fetcher import fetch_unprocessed_images, download_image, mark_images_as_received
from uploader import upload_processed_image
from processor import process_image
import time

# 轮询间隔时间，单位为秒
POLLING_INTERVAL = 5

def main():
    while True:
        print("🚀 开始检查服务器上的未处理图片...")
        # 获取服务器上的未处理图片列表
        images = fetch_unprocessed_images()

        if not images:
            print("⚠️ 没有未处理的图片")
        else:
            received_ids = []
            downloaded_files = {}

            # 下载所有未处理的图片
            for img in images:
                file_path = download_image(img["file_url"], img["file_name"])
                if file_path:
                    received_ids.append(img["id"])
                    downloaded_files[img["id"]] = file_path

            # 一次性将下载的图片标记为已接收
            if received_ids:
                print("✅ 开始将下载的图片标记为已接收")
                mark_images_as_received(received_ids)

            # 逐个处理已下载并标记为已接收的图片
            for img_id, file_path in downloaded_files.items():
                print(f"✅ 开始处理图片 ID {img_id}：{downloaded_files[img_id]}")
                # 处理图片
                processed_file_path = process_image(file_path)

                if processed_file_path:
                    print(f"🖼️ 上传已处理图片 ID {img_id}：{processed_file_path}")
                    # 上传已处理的图片并获取上传结果
                    upload_success = upload_processed_image(img_id, processed_file_path)

                    if upload_success:
                        # 上传成功后，标记该图片为已处理
                        print(f"✅ 图片 ID {img_id} 上传成功，已标记为已处理")

        # 等待指定的轮询间隔时间后再次检查
        print(f"🕒 等待 {POLLING_INTERVAL} 秒后再次检查...")
        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    main()