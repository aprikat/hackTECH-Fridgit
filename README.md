Pinterest
=========

A Pythonic client for the Pinterest API

## Overview

The Pinterest client is actaully two clients in one, a builder styled client that returns dicts and a model-based client. We like variety at Pinterest, so you should pick the one that works for you.

### Low level client

The low level client is designed for those people who like to work as close to the metal as possible. It requires little configuration and does very little for you other than to take care of the boring details of authentication and response handling. To start off, you need a client. Create one like this:

	from pinterest.client import raw_client

	APP_SECRET = "my_app_key"
	APP_ID = "my_app_id"

	my_client = raw_client(APP_ID, APP_SECRET)

That's it, you're ready to make requests!

#### Making Requests

To make a request, you just call the appropriate methods on the client. Consider the following requests

	# Find a user's details
	response = my_client.users.icecreamcohen.get()

	# Find a user's pins
	response, bookmark = my_client.users.icecreamcohen.pins.get()

	# Find the second page of a user's pins
	response, bookmark = my_client.users.icecreamcohen.pins.get(bookmark=bookmark)

	# Get a board's details
	board_id = "240098292573185609"
	response = my_client.boards(board_id).get()

	# Get a user's board (assume evrhet has a board called my stuff).
	response = my_client.boards.evrhets('shoes').get()

	# get a board's pins
	response = my_client.boards('evrhets/shoes').pins.get()

You'll note that the method chain exactly duplicates the URL path of the request. However, there can be some urls that are invalid python method calls. Consider the username 'abcd-def'. Obviously we can't just tack that in as a method call, but we can do this;

	response = my_client.users('abcd-def').get()

Which will get you the response you desire. If you need to send query string parameters to an api request, simply use kwargs like this:

	response, next_bookmark = my_client.users.evrhet.pins.get(page_size=10)


###High Level Client
The high level client library is designed to have a model based approach. It takes care of authentication, response handling, json parsing, and pagination. While api calls in the low level client map directly to the path of the API endpoint being hit, the interaction is more abstracted in the high level library.

Before making requests, you first need to configure the client that will be used. You can configure your client like this:

	from pinterest.models.model import Pinterest

	CLIENT_ID = "your app's client id"
	CLIENT_SECRET = "your app's secret"
	Pinterest.configure_client(CLIENT_ID, CLIENT_SECRET)

####Making Requests
In the high level client, you make requests by calling methods on a model object or accessing attributes of a model. The only exception is the search module in which the functions are in the global name space.

The following models exist in the high level client:

	User
	Pin
	Board
	Comment
	Query
	Domain
	Category
	Feed

#####Models and requests
	# Create a User object for user vedharaju
	me = User("vedharaju")

	# Returns the users id
	me.id

	# Returns the users first_name
	me.first_name
Similarly, other fields can be accessed as attributes on the User model.

The other users endpoints can be accessed as function calls on the User model

	# Returns the user's pins as Pin objects
	me.pins()

	# Returns the user's boards as User objects
	me.boards()

	# Returns the user's followers as User objects
	me.followers()

	# Returns the user's followees as User objects
	me.followees()
Each of these functions returns model objects. For example, me.pins() would return a list of Pin objects on which further calls can be made.

	pins = me.pins()
	pin = pins[0]

	# Returns the pin's id
	pin.id

	# Returns a list of the pins comments as Comment objects
	pin.comments()

To get all the categories on Pinterest

	# Returns a list of Category objects
	Categories.all

The high level client abstracts away the idea of pagination and bookmarks. In the low level client you would have had to make another API call and pass the bookmark as a parameter to get the next page of a response. However, in the high level client you can just access elements by indexing, and the work of fetching more elements is done for you.

#####Search module
First, you have to import the search module

	import pinterest.search as search

Make sure the high level client has already been configured.

	# Search boards
	search.boards("cats")

	# Search a users pins
	search.user_pins("puppies")

	# Get typeahead suggestions as a list of Query objects
	search.typeahead_suggestions("anima", tags = "board")


####Passing Parameters
Like in the low level client, parameters can be passed as kwargs.

	# Pass parameters when creating an object
	me = User("vedharaju", fields = "user.first_name, user.last_name")

	# Pass parameters when calling an objects functions
	pins = me.pins(add_fields="pin.dominant_color")

	# Pass parameters when searching
	results = search.pins("purse", tags = "board,facebook_pinner", num_people = "2", num_boards="2")

### Handling Errors

The client considers any nonzero status code to be an error and will raise an exception when one is encountered. The raised exception will have code, message and detail fields which should help in determining what do do. Some errors like BookmarkNotFound should signal your client to stop requesting a url, others, like ServerError (error 12) indicate that Pinterest itself had trouble serving your request.

