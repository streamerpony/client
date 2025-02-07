from fetcher import fetch_unprocessed_images, download_image, mark_images_as_received

def main():
    print("🚀 开始检查服务器上的未处理图片...")
    images = fetch_unprocessed_images()
    
    if not images:
        print("⚠️ 没有未处理的图片")
        return
    
    received_ids = []
    for img in images:
        file_path = download_image(img["file_url"], img["file_name"])
        if file_path:
            received_ids.append(img["id"])
    
    if received_ids:
        mark_images_as_received(received_ids)

if __name__ == "__main__":
    main()
