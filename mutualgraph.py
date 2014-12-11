import networkx as nx # pip install networkx
import requests # pip install requests
import facebook
import json

ACCESS_TOKEN = 'CAACEdEose0cBAOMV1BjNbNKpOtyjSDm3PZChaFG4sbwLZABBMQUDQ8oODqMgxfhbZBiZBJOZBfxgJZCZAZA3IMXFkObdZBPFiZB6ZCkbI4gRoJvSDKfH8Xu5gvjZB3534Mtnq5GpDYcv0FkjnT8sx4CPAAu2K3KeX4hBW4o8hRc3Gu5QZC8gmkcMmFvOiaQLysm4c4XWZBZBRCSzc0c7liBRBJiqFwdxfsrqWIJcwcZD'
g = facebook.GraphAPI(ACCESS_TOKEN)

friends = [ (friend['id'], friend['name'],)
                for friend in g.get_connections('me', 'friends')['data'] ]

url = 'https://graph.facebook.com/me/mutualfriends/%s?access_token=%s'

mutual_friends = {} 

# This loop spawns a separate request for each iteration, so
# it may take a while. Optimization with a thread pool or similar
# technique would be possible.
for friend_id, friend_name in friends:
    print friend_id
    r = requests.get(url % (friend_id, ACCESS_TOKEN,) )
    print r
    response_data = json.loads(r.content)['data']
    mutual_friends[friend_name] = [ data['name'] 
                                    for data in response_data ]
    
nxg = nx.Graph()

[ nxg.add_edge('me', mf) for mf in mutual_friends ]

[ nxg.add_edge(f1, f2) 
  for f1 in mutual_friends 
      for f2 in mutual_friends[f1] ]

# Explore what's possible to do with the graph by 
# typing nxg.<tab> or executing a new cell with 
# the following value in it to see some pydoc on nxg
print nxg
