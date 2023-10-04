"""
(c)araigumaG. 2022

This file is licensed under the terms of zlib/libpng license

"""


from urllib import request, parse
import subprocess
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

def engine_voicevox(_text, _voice, _rate, _path):
    # query = subprocess.run(["curl", "-X", "POST", f"http://localhost:50021/audio_query?text={urllib.parse.quote(_text)}&speaker={_voice}"], text=True, capture_output=True)
    req_query = request.Request(f"{host}/audio_query?text={parse.quote(_text)}&speaker={_voice}",method="POST")
    data = json.loads(request.urlopen(req_query).read())
    data["speedScale"] = _rate / 140

    req_voice = request.Request(f"{host}/synthesis?speaker={_voice}",\
        data=json.dumps(data).encode(),\
        headers = {'Content-Type': 'application/json'}
    )
    voice = request.urlopen(req_voice).read()
    fd = open(_path,"wb")
    fd.write(voice)
    # subprocess.run(["curl", "-X", "POST", f"{host}/synthesis?speaker={_voice}",\
    #     "-H", "Content-Type: application/json",\
    #     "-o", _path,\
    # ], input=query, text=True)