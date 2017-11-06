import requests
'''
Method: GET
Path: /api/create
Query Parameters:
	date1
	date2
	date3
	numpackages
	numversions
	numcompatibles
'''
payload = {'date1': '10/10/2019 10:00 AM', 'date2': '10/10/2020 10:00 AM','date3': '10/10/2021 10:00 AM', 'numpackages': '20','numversions': '40', 'numcompatibles': '10000',}
r = requests.get("http://localhost:34567/api/create", params=payload)
print(r.text)
