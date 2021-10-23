import requests

try:
	response = requests.get("https://api.open-notify.org/astros.json")
	print(response)
except Exception as error:
    print(error)
    print(type(error))
    print([o for o in dir(error) if not o.startswith('__')])

