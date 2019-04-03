import requests
from IPython.display import HTML

subscription_key = "f8209f3535fc4ebea5ed1becfe41f28e"
search_term = "Microsoft"
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

descriptions = [article["description"] for article in search_results["value"]]

print(descriptions)
rows = "\n".join(["<tr><td>{0}</td></tr>".format(desc) for desc in descriptions])
HTML("<table>"+rows+"</table>")