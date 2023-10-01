"""
(c)araigumaG. 2022

This file is licensed under the terms of zlib/libpng license

"""


from urllib import request
import json

voices = []
host = "http://localhost:50021"
enabled = True

try:
    req = request.Request(host + "/speakers",method="GET")
    data = json.loads(request.urlopen(req).read())
    for speaker in data:
        for style in speaker["styles"]:
            voices.append((str(style["id"]),speaker["name"] + " - " + style["name"],""))
except:
    voices = [("3", "ずんだもん" + " - " + "ノーマル","")]