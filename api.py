import requests
isbn='080213825X'
response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn).json()
print(response)