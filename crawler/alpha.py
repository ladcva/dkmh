# Importing libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests

def get_dict_semester_website():

	url = 'https://sv.isvnu.vn/dashboard.html'
	headers = {
	'cookie': '_ga=GA1.2.1000091377.1671634543; ASP.NET_SessionId=t0fmbgxgkd3n3ayoutw10p22; __RequestVerificationToken=ixTDUomDQ7f1Kx6DRJzmpedAmS2KmZyjzv8BDV-WFoETIPyuE9nxcEqOTa1PtrNzIX1Kva6rc8WfsPAyNTb9iCZ-aG7X4Bdfu5ZD9ZJvDZ01; PAVWs3tE769MuloUJ81Y=lJVoIW0Nv6nBeFQ5y0RWnLqHyVkRK5V-zGEVZDYbXkY; ASC.AUTH=C755BEDF469030D764CA9EFA3B5F9067E8EB2CECE8C30C1C7365EB0DBBF2725859E0099D6D76321C88CF90ABD53266990D8479247E63757457040F631611FB6DFFF67130DE0A342F3997FE2B30F3ED386EA4680196F761BD1BEE622FD8448C3EA5189E7519ED4BEB7A315283F9430F97D8BF0803E242CC1F4F74C0E4F94F444D; _gid=GA1.2.674121839.1677083976; _gat_gtag_UA_184858033_10=1',
	}
	
	main_site = requests.get(url, headers=headers)
	soup = BeautifulSoup(main_site.content, 'html.parser')
	
	# Get all option tags
	tag_items = soup.select('option[value]')
	values = [item.get('value') for item in tag_items if item.get('value')]
	textValues = [item.text for item in tag_items if 'HK' in item.text]

	# Convert to dict
	# dict_res = {35: 'HK2 (2022-2023)', 34: 'HK1 (2022-2023)'}
	dict_res = dict(map(lambda k,v : (int(k), v), values,textValues))

	return dict_res

get_dict_semester_website()