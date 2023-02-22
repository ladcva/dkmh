import requests
from bs4 import BeautifulSoup

'''
# check ma hoc phan, thay vao URL
lhp = str(input("Dien ma mon hoc: "))

url = f"https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy=35&MaMonHoc={lhp}&DSHocPhanDuocHoc={lhp}&IsLHPKhongTrungLich=true&LoaiDKHP=1" 
'''

# Để crawl all môn thì IsLHPKhongTrungLich = false
url = "https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy=27&MaMonHoc=INS2011&DSHocPhanDuocHoc=INS2011&IsLHPKhongTrungLich=false&LoaiDKHP=1"

payload={}
headers = {
  'cookie': '_ga=GA1.2.1000091377.1671634543; ASP.NET_SessionId=t0fmbgxgkd3n3ayoutw10p22; __RequestVerificationToken=ixTDUomDQ7f1Kx6DRJzmpedAmS2KmZyjzv8BDV-WFoETIPyuE9nxcEqOTa1PtrNzIX1Kva6rc8WfsPAyNTb9iCZ-aG7X4Bdfu5ZD9ZJvDZ01; PAVWs3tE769MuloUJ81Y=lJVoIW0Nv6nBeFQ5y0RWnLqHyVkRK5V-zGEVZDYbXkY; ASC.AUTH=C755BEDF469030D764CA9EFA3B5F9067E8EB2CECE8C30C1C7365EB0DBBF2725859E0099D6D76321C88CF90ABD53266990D8479247E63757457040F631611FB6DFFF67130DE0A342F3997FE2B30F3ED386EA4680196F761BD1BEE622FD8448C3EA5189E7519ED4BEB7A315283F9430F97D8BF0803E242CC1F4F74C0E4F94F444D; _gid=GA1.2.674121839.1677083976; _gat_gtag_UA_184858033_10=1',
}

def subject_request():
  # create a response variable
  response = requests.request("POST", url, headers=headers, data=payload)

  # create a Soup variable using BS4
  soup = BeautifulSoup(response.text, 'html.parser')

  # Find GUID for mon hoc
  for i in range(1,16):
    try:
      tag = soup.find_all('tr')[i]
      attribute = tag['data-guidlhp']

      # Find ma hoc phan cho mon hoc
      attribute2 = tag.find_all('div')[1].find('span', text='Mã lớp  học phần').next_sibling
      print("GUID: {}".format(attribute),"\n","Ma hoc phan{}".format(attribute2))

    except IndexError:
      break


subject_request()
# crawl -> send den module khac xu li -> receiver
# database