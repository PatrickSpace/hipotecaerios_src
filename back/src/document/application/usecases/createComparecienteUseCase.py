class CreateCompareciente:
    def __init__(self, comparecientesInterface):
        self.comparecientesInterface = comparecientesInterface

    def execute(self, body, myPath):
        try:
            #userPath = myPath + '\\' + kardex
            print("usecase")
            self.comparecientesInterface.crearCompareciente(body, myPath)
            outPut = {
                "message": "Compareciente agregado"
            }
        except Exception as exc:
            print(exc)
            outPut = {
                "message": "error"
            }
        finally:
            return outPut