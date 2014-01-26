from pinterest.models.model import Pinterest, User, Pin, Board, Comment, Query, Domain, Category, Feed

CLIENT_ID = "1435800"
CLIENT_SECRET = "fd9f02008e57bcb30c37e8908264eb71cd64df20"
Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

import pinterest.search as search
results = search.pins(query="fudge", rich_type="recipe", rich_query="avocado, black beans, and bell peppers", boost="indyrank")


for x in range(0,3):
	print results[x].description
	print results[x].image_medium_url
	print results[x].link
	print results[x].comments.get[0]
