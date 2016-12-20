
import urllib
from lxml.html import fromstring

import json
import requests

response = requests.get('http://games.espn.com/college-bowl-mania/2016/en/group?groupID=93049')
doc = fromstring(response.content)


spread = doc.xpath("//td[contains(@class,'entry')]//text()")

print(spread)

