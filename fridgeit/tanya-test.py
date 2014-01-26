from pinterest.models.model import Pinterest, User
import pinterest.search as search

CLIENT_ID = "1435790"
CLIENT_SECRET = "8c8eab09fe710377c9e879872855109c9f349195"
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

pins = search.pins("chocolate")

#returns 10 pins
for x in range (0, 25):
  print pins[x].description