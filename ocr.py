import pytesseract
from PIL import Image


class OCR():
    """OCR
    圖片驗證碼識別
    """    
    def __init__(self, tesseract_cmd='tesseract'):
        """__init__
        
        Keyword Arguments:
            tesseract_cmd {str} --  tesseract指令或路徑(default: {'tesseract'})
        """        
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def judge(self, pixl):
        THRESHOLD = 80
        if pixl>THRESHOLD:
            return 1
        else:
            return 0
    def depoint(self, img):
        """對傳入的二值化圖像進行降噪"""
        pixdata = img.load()
        w,h = img.size
        for y in range(1,h-1):
            for x in range(1,w-1):
                count = 0
                if self.judge(pixdata[x,y-1]):#上
                    count = count + 1
                if self.judge(pixdata[x,y+1]):#下
                    count = count + 1
                if self.judge(pixdata[x-1,y]):#左
                    count = count + 1
                if self.judge(pixdata[x+1,y]):#右
                    count = count + 1
                if self.judge(pixdata[x-1,y-1]):#左上
                    count = count + 1
                if self.judge(pixdata[x-1,y+1]):#左下
                    count = count + 1
                if self.judge(pixdata[x+1,y-1]):#右上
                    count = count + 1
                if self.judge(pixdata[x+1,y+1]):#右下
                    count = count + 1
                if count > 4:
                    pixdata[x,y] = 255
        return img
    def heibaihua(self, img):
        Img = img.convert('L')
        threshold = 200
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        photo = Img.point(table, '1')
        #photo.save("BuildImageCode2.jpg")
        return photo
    def noise_remove_pil(self, image_name, k):
        """
        8鄰域降噪
        Args:
            image_name: 圖片文件命名
            k: 判斷閾值
        Returns:
        """
        def calculate_noise_count(img_obj, w, h):
            """
            計算鄰域非白色的個數
            Args:
                img_obj: img obj
                w: width
                h: height
            Returns:
                count (int)
            """
            count = 0
            width, height = img_obj.size
            for _w_ in [w - 1, w, w + 1]:
                for _h_ in [h - 1, h, h + 1]:
                    if _w_ > width - 1:
                        continue
                    if _h_ > height - 1:
                        continue
                    if _w_ == w and _h_ == h:
                        continue
                    if img_obj.getpixel((_w_, _h_)) < 230:  
                        # 這裏因爲是灰度圖像，設置小於230爲非白色
                        count += 1
            return count
        img = Image.open(image_name)
        # 灰度
        gray_img = img.convert('L')
        w, h = gray_img.size
        for _w in range(w):
            for _h in range(h):
                if _w == 0 or _h == 0:
                    gray_img.putpixel((_w, _h), 255)
                    continue
                # 計算鄰域非白色的個數
                pixel = gray_img.getpixel((_w, _h))
                if pixel == 255:
                    continue
                if calculate_noise_count(gray_img, _w, _h) < k:
                    gray_img.putpixel((_w, _h), 255)
        return gray_img
    def convert(self, image, threshold=4):
        img = self.noise_remove_pil(image, threshold)
        img = self.heibaihua(img)
        img = self.depoint(img)
        text = pytesseract.image_to_string(img)
        return text

if __name__ == "__main__":
    TEST = OCR()
    text = TEST.convert('./codeImg.jpg')
    print(text)
