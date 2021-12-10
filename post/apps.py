from django.apps import AppConfig


class PostConfig(AppConfig):
    name = 'post'


i = 0
while i < 100:
    i += 1
    import requests

    url = "http://35.203.69.86:5000/"

    payload = {}
    headers = {
        'Cookie': 'csrftoken=VmRVxffxNC203OFrbxAmy4GTpbg6KG5rCOSYMYTcl4lVTPSZcQpbSX8Aq6YNjb4e'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(i)
    print(response.text[50])
