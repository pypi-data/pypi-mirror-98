#!/usr/bin/env python3
import houndify
import sys



CLIENT_ID = sys.argv[1]
CLIENT_KEY = sys.argv[2]
QUERY = sys.argv[3]

requestInfo = {
  'Latitude': 37.388309, 
  'Longitude': -121.973968
}

client = houndify.TextHoundClient(CLIENT_ID, CLIENT_KEY, "test_user", requestInfo)

response = client.query(QUERY)
print(response)