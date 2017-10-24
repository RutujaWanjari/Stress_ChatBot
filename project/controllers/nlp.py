import urllib
from urllib import parse, request


try:
    text = urllib.parse.urlencode({'text': 'I am good'})
    text = text.encode('UTF-8')
    url = urllib.request.Request('http://text-processing.com/api/sentiment/', text)
    url.add_header("Content-Type", "application/x-www-form-urlencoded")
    responseData = urllib.request.urlopen(url).read().decode('utf8', 'ignore')
    print(responseData)
except Exception as e:
    print(str(e))
