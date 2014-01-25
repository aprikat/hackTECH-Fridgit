from pinterest.client import raw_client

APP_SECRET = "08b5300683311856a4397ad33dbc117af5e89edb"
APP_ID = "1435798"

my_client = raw_client(APP_ID, APP_SECRET)

# get a board's pins
response = my_client.boards('evrhets/shoes').pins.get()
print response