import requests
### Snag a contest
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
### Register for a contest
'''
Method: GET
Path: /api/register
Query Parameters:
	id
	name
'''
### Retrieve a problem
'''
Method: GET
Path: /api/get
Query Parameters:
	id
	pid
	role
	code
'''
#If successful, the response contains a field `data`.
### Submit a problem/solution
'''
Method: POST
Path: /api/submit
Query Parameters:
	id
	pid
	role
	code
Request Data:
	data
'''

def createGame(host,date1, date2, date3, numpackages, numversions, numcompatibles):
	payload = {'date1': str(date1), 'date2': str(date2),'date3': str(date3), 'numpackages': str(numpackages),'numversions': str(numversions), 'numcompatibles': str(numcompatibles)}
	r = requests.get("http://" + host + "/api/create", params=payload)
	return r

def registerAGame(host,id1,name):
	payload = {'id': str(id1), 'name': str(name)}
	r = requests.get("http://" + host + "/api/register", params=payload)
	return r

def retrieveAProblem(host,id1,pid,role,code):
	payload = {'id': str(id1), 'pid': str(pid),'role': str(role), 'code': str(code)}
	r = requests.get("http://" + host + "/api/get", params=payload)
	return r

def submitProblemOrSolution(host,id1,pid,role,code,data):
	payload = {'id': str(id1), 'pid': str(pid),'role': str(role), 'code': str(code), 'data' : data}
	r = requests.post("http://" + host + "/api/submit", params=payload)
	return r
