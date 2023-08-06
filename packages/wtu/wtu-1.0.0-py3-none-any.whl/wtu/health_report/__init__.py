#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import httpx


class JKClient:
    def __init__(self, jwt: str):

        _headers = {
            'Host': 'jk.wtu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; OPPO R17 Pro Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MicroMessenger/7.0.17.1720(0x27001134) Process/appbrand0 WeChat/arm32 NetType/WIFI Language/zh_CN ABI/arm32',
            'charset': 'utf-8',
            'authorization': jwt,
                    'Accept-Encoding': 'gzip, deflate',
            'content-type': 'application/x-www-form-urlencoded',
            'Referer': 'https://servicewechat.com/wx186658badc0a17c7/8/page-frame.html',
        }
        self.client = httpx.Client(
            base_url='https://jk.wtu.edu.cn/health/mobile/',
            headers=_headers)

    def get_user_info(self, uid: str) -> dict:
        _data = {
            'yhm': uid,
            'yhlx': 'student',
            'get_card': 1
        }
        res = self.client.post('/get_user_info/', data=_data)

        return res.json()

    def get_user_qrcode(self, uid: str) -> bytes:
        data = self.get_user_info(uid)

        pic_path = 'https://jk.wtu.edu.cn' + data.get('path')
        response = httpx.get(pic_path)
        return response.content

    def getAvatar(self, uid: str) -> bytes:
        _data = {
            'yhm': uid,
            'yhlx': 'student',
        }
        res = self.client.post('/getAvatar/', data=_data)

        return res.content

    @staticmethod
    def _save_pic(bin_data: bytes, save_path: str):
        with open(save_path, 'wb') as f:
            f.write(bin_data)
            f.close()
    
    def get_last_health_report_data(self):
        """JWT authorization user ONLY"""
        res = self.client.post('/get_last_health_report_data/')

        return res.json()

    def get_card_report(self, uid: str):
        _data = {
            'yhm': uid,
        }
        res = self.client.post('/get_card_report/', data=_data)

        return res.json()

    def _solve_report_data(self, uid: str, isBack: bool):
        data = self.get_card_report(uid)["rows"][0]
        if isBack:
            _jkklx = '已返校'
        else:
            _jkklx = '未返校'

        _data = {
            'yhm': uid,
            'yhlx': 'student',
            'jkklx': _jkklx,
            'jkmdqzt': 'green',
            'longitude': data['longitude'],
            'latitude': data['latitude'],
            'address': data['address'],
            'data': data['structure'],
            'normal': 1

        }
        return _data

    def health_report(self, uid: str, isBack: bool=True):
        _data = self._solve_report_data(uid, isBack)

        res = self.client.post('/health_report/', data=_data)
        return res.json()
