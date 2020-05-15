[![GitHub release](https://img.shields.io/github/pipenv/locked/python-version/thanatosdi/E-Tracking)]()
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
  * tracker(txtProductNum, autoVerify=False, tesseract_path='tesseract')  
    * txtProductNum: [str] 貨態號碼 詳細請至[貨態號碼查詢教學](https://eservice.7-11.com.tw/e-tracking/TeachPage.html)查看  
    * autoVerify: [Boolean] 是否啟用 OCR 自動辨識驗證碼 (default: False)
    * tesseract_path: [str] 設定 tesseract 路徑 (default: tesseract)  
# Use
```python
# import ECTracker class
from .etracking import ECTracker
ECTRACKER = ECTracker()
# ECTRACKER.tracker('txtProductNum', autoVerify=True)
print(ECTRACKER.tracker('F45913208600', autoVerify=True))
# Return message (type is dictionary)
{   
    '取貨門市': '仁東', 
    '取貨門市地址': '高雄市岡山區大仁北路175號1樓', 
    '取貨截止日': '2020-04-15', 
    '付款資訊': '取貨付款', 
    '貨態資訊': [
        '2020/04/06 18:30 交貨便訂單已成立，尚未至門市寄貨', 
        '2020/04/06 19:35 門市已收件', 
        '2020/04/07 02:16 包裹已送往物流中心', 
        '2020/04/07 07:35 包裹已送達物流中心，進行理貨中', 
        '2020/04/07 14:09 包裹等待配送中', 
        '2020/04/08 04:25 包裹配達門市', 
        '2020/04/08 16:57 已完成包裹成功取件'
    ]
}
```
# Error
使用 OCR 自動判斷驗證碼錯誤時將拋出例外: `VerifyError`  
請自行進行例外處理(重新執行至正確或中斷)
