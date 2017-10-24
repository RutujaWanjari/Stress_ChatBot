import urllib
from urllib import parse, request
import json


def bot_response(message):
    try:
        text = urllib.parse.urlencode({'text': message})
        text = text.encode('UTF-8')
        url = urllib.request.Request('http://text-processing.com/api/sentiment/', text)
        url.add_header("Content-Type", "application/x-www-form-urlencoded")
        response = urllib.request.urlopen(url).read().decode('utf8', 'ignore')
        response = json.loads(response)
        return response['label']
    except Exception as e:
        return "Sorry, I didn't get that"
