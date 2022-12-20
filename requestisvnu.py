import requests
import shutil
from bs4 import BeautifulSoup

'''
# check ma hoc phan, thay vao URL
lhp = str(input("Dien ma mon hoc: "))

url = f"https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy=35&MaMonHoc={lhp}&DSHocPhanDuocHoc={lhp}&IsLHPKhongTrungLich=true&LoaiDKHP=1"
'''

url = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy=35&MaMonHoc=PES1003&DSHocPhanDuocHoc=PES1003&IsLHPKhongTrungLich=true&LoaiDKHP=1"

payload={}
headers = {
  'authority': 'sv.isvnu.vn',
  'accept': 'text/html, */*; q=0.01',
  'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'cookie': 'ASP.NET_SessionId=eegxrqrbdm5xxp2cxrnql3hh; __RequestVerificationToken=72wUCejJDOAf2mifGTwY-ui2wdHPQ-D8q1egJi0BRoGloRQLlM4SwS-JEfkDAuo39egNoDsvkgU1w5qa-hjoKjnCKm9vuLxSPDI_-lUNssE1; SinhVien_LangName=; _ga=GA1.2.343368229.1671026498; ASC.AUTH=34552BB4081FAC768BE5324FDA464E5EB259E619364F4EBA217AE33D00D1326B6960FD0E5780AE22A99F327D358B272212E212DCB364BCCD089CE31AB0B46F7F5319713E122E7BE5EDD81C169507EA03C77EAE9D1884D4ECEBC07FCEF7AD2256C350BF58BCCC148C48DB8EB5CDE38CA306D6C5EE6A63927270488275FE515377',
  'origin': 'https://sv.isvnu.vn',
  'Referer': 'https://sv.isvnu.vn/dang-ky-hoc-phan.html',
  'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': 'Windows',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.46',
  'x-requested-with': 'XMLHttpRequest'
}

response = requests.request("POST", url, headers=headers, data=payload)

'''
with open('sample.json', 'wb') as out_file:
  shutil.copyfileobj(response.raw, out_file)
'''

soup = BeautifulSoup(response.text, 'html.parser')

tag = soup.findAll('tr')[1]
attribute = tag['data-guidlhp']

print(attribute)


# 2 
attribute2 = tag.findAll('div')[1].find('span', text='Mã lớp  học phần').next_sibling



print(attribute2)


#print(response.text)
