from facepy import GraphAPI
import json
import requests
import os

def downloadFile(url, fileName):
    r = requests.get(url, stream = True)
    try:
        with open(fileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()
    except:
        fileName = fileName.strip('/')
        with open(fileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
                    f.flush()


groupId = "714685238558448"
accessToken = "CAACEdEose0cBAI6mbn6Vf6DjaJY8F41VoxZAx3zNJZBFKwXL3D3Jl280iVtoqVdqhFYvpSe0R1MQEYhSU3jfNdpHSuFjRDOyiKvBpNxLAQbcZCNPZBIHtsmVRnpCtMMJNjrVJGepQbhpMgDYfQH7uyMFz2ZAl6WXdWbo6gWnjuq0olt0nrcBg9SI45gBm0VATWLy7lbZAg5u3zWtMD1ZC6uTbIorONisvUZD"

graph = GraphAPI(accessToken)
pages = graph.get(groupId + "/files", page = True, retry = 5, limit = 2000)
counter = 2
try:
    os.mkdir('fbPythonGroup')
except:
    pass
os.chdir(os.getcwd() + '/fbPythonGroup')


for page in pages:
    for post in page['data']:
        if counter > 0:
            counter -= 1
            continue
        url = post['download_link']
        fileName = url[50:]
        print "fetching " + url
        downloadFile(url, fileName)

