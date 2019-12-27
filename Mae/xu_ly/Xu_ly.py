from datetime import datetime

import re

#---Loại bỏ tag HTML
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)


def tao_chuoi_ngay(ngay_sinh):
    chuoi_ngay_sinh = ngay_sinh.split("/")
    ngay = int(chuoi_ngay_sinh[0])
    thang = int(chuoi_ngay_sinh[1])
    nam = int(chuoi_ngay_sinh[2])
    ket_qua = datetime(nam,thang,ngay)
    return ket_qua

