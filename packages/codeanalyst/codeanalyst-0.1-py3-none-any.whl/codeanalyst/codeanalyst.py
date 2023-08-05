import requests
import json
from . import api

url = api

def codetest(cid, secret, code, lang, langv):
  jsun = {
    "clientId": cid,
    "clientSecret": secret,
    "script": code,
    "language": lang,
    "versionIndex": langv}
  req = requests.post(url, json = jsun)
  result = json.loads(req.text)
  return CodeAnalystResult(result)


class CodeAnalystResult:
  def __init__(self, result):
    self.result = result
