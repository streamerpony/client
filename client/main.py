from fetcher import fetch_unprocessed_images, download_image, mark_images_as_received
import time

# 轮询间隔时间，单位为秒
POLLING_INTERVAL = 5  
def main():
    while True:
        print("🚀 开始检查服务器上的未处理图片...")
        images = fetch_unprocessed_images()

        if not images:
            print("🤯 没有未处理的图片")
        else:
            received_ids = []
            for img in images:
                file_path = download_image(img["file_url"], img["file_name"])
                if file_path:
                    received_ids.append(img["id"])

            if received_ids:
                mark_images_as_received(received_ids)

        # 等待指定的轮询间隔时间后再次检查
        print(f"🕒 等待 {POLLING_INTERVAL} 秒后再次检查...")
        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    main()
