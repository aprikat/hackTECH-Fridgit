import requests

page = requests.get("http://www.pinterest.com/pin/346566133796878258/")
print page.text
