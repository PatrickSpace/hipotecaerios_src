import json
import os


print(os.path.dirname(os.path.abspath(__file__)))
myDir = os.path.dirname(os.path.abspath(__file__))
print(os.path.join(myDir, 'replace.json'))

def rules():
    myDir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(myDir, 'replace.json'),"r", encoding="utf-8") as f:
        data = json.load(f)
    return data