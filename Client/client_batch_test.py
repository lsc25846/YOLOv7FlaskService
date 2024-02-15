import requests
import os

url = 'http://127.0.0.1:5000/upload_batch'
directory_path = './Images'  # 图片所在的文件夹路径
files = {}
total_images = 0
# 遍历指定目录，为每个文件创建文件对象
for filename in os.listdir(directory_path):
    if filename.endswith('.png') or filename.endswith('.jpg'):  # 根据需要过滤文件类型
        file_path = os.path.join(directory_path, filename)
        files[f'image{total_images+1}'] = open(file_path, 'rb')
        total_images += 1

data = {'total_images': total_images}

response = requests.post(url, files=files, data=data)

# 确保打开的文件被关闭
for file in files.values():
    file.close()

print(response.text)
