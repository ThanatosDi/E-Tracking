# E-Tracking
 統一超商交貨便貨態查詢(包含 OCR 自動辨識驗證碼)
# Install
1. 下載本 source code  
2. 安裝必要套件
    ```python
    pip install -r requirements.txt
    ```
3. 安裝 tesseract (如需使用 OCR 自動辨識)  
   [Linux 安裝 tesseract](https://github.com/tesseract-ocr/tesseract/wiki)  
   [Windows 安裝 tesseract](https://github.com/UB-Mannheim/tesseract/wiki)  
# API Reference
* ECTracker: [class]
  * tracker(txtProductNum, autoVerify=False)  
    * txtProductNum: [str] 貨態號碼 詳細請至[貨態號碼查詢教學](https://eservice.7-11.com.tw/e-tracking/TeachPage.html)查看  
    * autoVerify: [Boolean] 是否啟用 OCR 自動辨識驗證碼 (default: False)  
# Use
```python
# import ECTracker class
from .etracking import ECTracker
ECTRACKER = ECTracker()
# ECTRACKER.tracker('貨態查詢碼', autoVerify=True)
print(ECTRACKER.tracker('F45913208600', autoVerify=True))
```