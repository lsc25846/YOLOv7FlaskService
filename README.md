# YOLOv7FlaskService
## 程式主畫面
![image]()

## 功能
此專案實現一基於Flask框架的影像檢測Server，透過yolov7進行影像辨識，再將結果回傳給Client端

## 安裝流程
### 1.安裝此專案requirements
```
pip install -r requirements.txt
```

### 2.安裝[yolov7](https://github.com/WongKinYiu/yolov7?tab=readme-ov-file)
此處僅提供安裝方式，請依照原作提供的安裝方式進行安裝
```
cd yolov7
pip install -r requirements.txt
```
此專案會使用到已經訓練過的權重檔，請至原作中進行下載

## 使用方式
### 1.請到Server資料夾中修改[server.py](https://github.com/lsc25846/YOLOv7FlaskService/blob/main/Server/server.py)
```
weights = './path/to/your/weight'  # 替換為你的權重檔路徑
```

### 2.執行[server.py](https://github.com/lsc25846/YOLOv7FlaskService/blob/main/Server/server.py)
如果運行成功，則會在[http://127.0.0.1:5000](http://127.0.0.1:5000)網址中可以看到畫面

### 3.請到Client資料夾中執行[client.py](https://github.com/lsc25846/YOLOv7FlaskService/blob/main/Client/client.py)
![image]()
請填入Server URL(預設為http://127.0.0.1:5000)  
![image]()
按下Open Folder開啟圖片的資料夾  
![image]()
Send Image按鈕可以傳送一張圖片到Server端進行辨識  
![image]()
Send All Images按鈕則可以一次傳送整個資料夾中的影像進行辨識  

## Reference
[yolov7](https://github.com/WongKinYiu/yolov7?tab=readme-ov-file)
