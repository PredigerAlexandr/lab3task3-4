import requests

res = requests.get('http://127.0.0.1:8080/api/post_by_category/Business')
print(res.json())