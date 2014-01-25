from pinterest.models.model import Pinterest, User

CLIENT_SECRET = '56de81f97190ff657e0f828d54185cf527316fb3'
CLIENT_ID = '1435704'
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)
me = User('tcpanda')
pins = me.pins()
pin = pins[0]
pin.
print pin.comments()
boards = pin.related_boards()
followers = boards[0].followers()

