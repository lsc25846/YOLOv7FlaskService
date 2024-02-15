import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
import os
import json

class ImageSenderApp:
    def __init__(self, master):
        self.master = master
        master.title('Image Sender UI')

        # 顯示圖片的區域
        self.image_label = tk.Label(master, text="No Image")
        self.image_label.pack()

        # 顯示檔案名稱的標籤
        self.filename_label = tk.Label(master, text="Filename: None")
        self.filename_label.pack()

        # 顯示回應的標籤
        self.response_label = tk.Label(master, text="Response: None")
        self.response_label.pack()

        # 新增 URL 輸入框和相應的標籤
        self.url_label = tk.Label(master, text="Server URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master)
        self.url_entry.pack()
        self.url_entry.insert(0, "http://127.0.0.1:5000")  # 設置預設值

        # 開啟資料夾按鈕
        self.open_folder_button = tk.Button(master, text="Open Folder", command=self.open_folder)
        self.open_folder_button.pack()

        # 開始傳送按鈕
        self.send_button = tk.Button(master, text="Send Image", command=self.send_image)
        self.send_button.pack()

        # 新增發送全部圖片的按钮
        self.send_all_button = tk.Button(master, text="Send All Images", command=self.send_all_images)
        self.send_all_button.pack()

        # 圖片資料夾和當前圖片索引
        self.directory = './Images'
        self.images = []
        self.current_image_index = 0

    def load_images(self):
        self.images = [f for f in os.listdir(self.directory) if f.endswith(('.png', '.jpg'))]
        self.current_image_index = 0
        if self.images:
            self.display_image()

    def display_image(self):
        if self.images:
            image_path = os.path.join(self.directory, self.images[self.current_image_index])
            img = Image.open(image_path)
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=photo)
            self.image_label.image = photo  # keep a reference!
            self.filename_label.configure(text=f"Filename: {self.images[self.current_image_index]}")
        else:
            messagebox.showinfo("Info", "No images found or finished all images.")

    def send_image(self):
        if self.images and self.current_image_index < len(self.images):
            filename = self.images[self.current_image_index]
            file_path = os.path.join(self.directory, filename)
            with open(file_path, 'rb') as file:
                files = {'file': file}
                url = self.url_entry.get() + '/upload'
                try:
                    response = requests.post(url, files=files)
                    self._handle_response(response)  # 處理回應
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to send image: {e}")
                    
            if self.current_image_index < len(self.images):
                self.display_image()
                self.current_image_index += 1            
            else:
                messagebox.showinfo("Info", "Finished all images.")
        else:
            messagebox.showinfo("Info", "No images loaded.")

    # 發送整個資料夾中的圖片
    def send_all_images(self):
        url = self.url_entry.get() + '/upload_batch'  # 使用 Entry widget 中的 URL
        files = {}
        total_images = 0

        for filename in self.images:  # 使用已經載入的圖片列表
            file_path = os.path.join(self.directory, filename)
            files[f'image{total_images+1}'] = open(file_path, 'rb')
            total_images += 1

        data = {'total_images': total_images}

        try:
            response = requests.post(url, files=files, data=data)  
            self._handle_response(response) # 處理回應      
        except Exception as e:
            self.response_label.configure(text=f'Error: {e}')
            messagebox.showerror("Error", f"Failed to send all images: {e}")
        finally:
            # 確保打開的文件被關閉
            for file in files.values():
                file.close()

        # 重置索引
        self.current_image_index = 0
        self.display_image()

    def _handle_response(self, response):
        try:
            response_data = response.json()  # 直接使用 .json() 方法轉換 JSON 數據
            # 從 response_data 中提取 'message' 列表，並將列表中的每個元素用換行符連接成一個字符串
            messages = '\n'.join(response_data['message'])
            # 更新 response_label 的 text 屬性，以顯示所有消息，每條消息後面跟著一個換行符
            self.response_label.configure(text=f'Response: {messages}')
        except Exception as e:
            self.response_label.configure(text=f'Error: {e}')
            messagebox.showerror("Error", f"Failed to handle response: {e}")

    def open_folder(self):
        self.directory = filedialog.askdirectory(initialdir="./Images")
        self.load_images()

def main():
    root = tk.Tk()
    app = ImageSenderApp(root)
    root.geometry("600x500")
    root.mainloop()

if __name__ == "__main__":
    main()
