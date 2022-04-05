import json
import os

class Signers:
    def __init__(self):#, signerDict):
        #self.signerDict = signerDict
        #self.path = "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\bot-hip\\backend\\src\\libs\\comparecientes.json"
        pass

    def update(self, path, body):
        #pathf = path+"\\comparecientes.json"
        #print("data ", body)
        if os.path.exists(path):
            print("existe path")
            bodyOut = self.updateBody(path, body)
            return bodyOut
        else:
            print("no existe el archivo")
        """if os.path.exists(path):
            print("existe")
            os.remove(path)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(body, f, ensure_ascii=False, indent=4)
        print("self signer ", body)
        return body"""

    def updateBody(self, path, body):
        with open(path) as f:
            data = json.load(f)
        if list(body.keys()).count('dni') > 0:#'dni' in body.keys():
            for item in range(len(data['comparecientes'])):
                #print("data ", data['comparecientes'][item]['dni'], body['dni'])
                if data['comparecientes'][item]['dni'] == body['dni']:
                    data['comparecientes'][item] = body
        os.remove(path)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return data