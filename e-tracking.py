import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup


class ECTracker():
    def __init__(self):
        self.api = 'https://eservice.7-11.com.tw/E-Tracking'
        self.session = requests.Session()
    def get_resource(self):
        """取得網頁 cookies、headers 等資源"""
        with self.session.get(f'{self.api}/search.aspx', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}) as response:
            if response.status_code != 200:
                response.raise_for_status()
            cookies = response.cookies
            body = BeautifulSoup(response.text, 'html.parser')
        __VIEWSTATE = body.find('input', {'id':'__VIEWSTATE'}).get('value', None)
        __VIEWSTATEGENERATOR = body.find('input', {'id':'__VIEWSTATEGENERATOR'}).get('value', None)
        headers_tmp_cookie = []
        for k, v in cookies.get_dict().items():
            headers_tmp_cookie.append(f'{k}={v}')
        headers = {
            'Cookie': ';'.join(headers_tmp_cookie),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        resource = {
            'headers': headers,
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            'code': f'{self.api}/ValidateImage.aspx?ts={datetime.now().strftime("%H%M%S%m%d")}'
        }
        self.codeImg(f'{self.api}/ValidateImage.aspx?ts={datetime.now().strftime("%H%M%S%m%d")}', headers)
        return resource
    def codeImg(self, codeImgURL, headers):
        with self.session.get(codeImgURL, headers=headers) as response:
            if response.status_code != 200:
                response.raise_for_status()
            with open('./codeImg.jpg', 'wb') as file_io:
                file_io.write(response.content)
    def tracker(self, txtProductNum):
        resource = self.get_resource()
        code = input('請輸入驗證碼: ')
        payload = {
            '__LASTFOCUS': '',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE':resource['__VIEWSTATE'],
            '__VIEWSTATEGENERATOR':resource['__VIEWSTATEGENERATOR'],
            'txtProductNum':'F45913208600',
            'tbChkCode':code,
            'aaa': '',
            'txtIMGName': '',
            'txtPage': '1'
        }
        with requests.post('https://eservice.7-11.com.tw/E-Tracking/search.aspx', headers=resource['headers'], data=payload, allow_redirects=False) as response:
            if response.status_code != 200:
                response.raise_for_status()
            body = BeautifulSoup(response.text, 'html.parser')
            info_children = body.find('div', {'class': 'info'}).find_all('div', recursive=False)
            shipping = body.find('div', {'class': 'shipping'})
            pickup_info = info_children[0]
            #取貨門市
            store_name = pickup_info.find('span', {'id': 'store_name'}).text
            #取貨門市地址
            store_address = pickup_info.find('p', {'id': 'store_address'}).text
            #取貨截止日
            pickup_deadline = pickup_info.find('span', {'id': 'deadline'}).text
            #付款資訊
            payment_type = info_children[1].find('h4', {'id': 'servicetype'}).text
            #貨態資訊
            status = []
            for element in shipping.find_all('li'):
                status_date = re.findall(r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}", element.text)[0]
                status.append(status_date + ' ' + (element.text).replace(status_date, ''))
            status.reverse()
            tracker = {
                '取貨門市': store_name,
                '取貨門市地址': store_address,
                '取貨截止日': pickup_deadline,
                '付款資訊': payment_type,
                '貨態資訊': status
            }
            return tracker


if __name__ == '__main__':
    ECTRACKER = ECTracker()
    print(ECTRACKER.tracker('F45913208600'))
