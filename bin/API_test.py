import json
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# This library will be used to fetch the API.
import urllib.request

try:
    if True:
        raise()
    else: "abc"

except:
    "abc"

apikey = "19690b2a340baf75aa2b4820b75391ca"
url = f"https://gnews.io/api/v4/search?q='UBS AND Blockchain'&token={apikey}&from=2022-01-21T00:00:00Z&to2022-02-21T00:00:00Z&lang=en&country=us&max=10"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))
    articles = data["articles"]

    print(len(articles))

    for i in range(len(articles)):
        # articles[i].title
        print(f"Title: {articles[i]['title']}")
        # articles[i].description
        print(f"Description: {articles[i]['description']}")
        # You can replace {property} below with any of the article properties returned by the API.
        # articles[i].{property}
        # print(f"{articles[i]['{property}']}")

        # Delete this line to display all the articles returned by the request. Currently only the first article is displayed.