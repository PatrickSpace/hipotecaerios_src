class FixDocumentUseCase:
    def __init__(self, wordsInterface):
        self.wordsInterface = wordsInterface
        #self.inmobiliaria = inmobiliaria
        pass
    
    #def execute(self, name, date, minuta, clausula, bankDoc, signers, inmob, bank, tables, images):
    def execute(self, data, filePath, basePath, fileName):
        try:
            fixWords = self.wordsInterface.fix(data, filePath, basePath, fileName)
            return fixWords
        except Exception as exc:
            print(exc)

class FixFormatDocumentUseCase:
    def __init__(self, formatInterface):
        self.formatInterface = formatInterface
    
    def execute(self):
        try:
            fixFormat = self.formatInterface.fix()
            return fixFormat
        except Exception as exc:
            print(exc)

class FixAppendixUseCase:
    def __init__(self, formatInterface):
        self.formatInterface = formatInterface

    def execute(self):
        try:
            print("Fix appendix")
            fixAppendix = self.formatInterface.fixAppendix()
            return fixAppendix
        except Exception as exc:
            print(exc)

class FixClausulaUseCase:
    def __init__(self, formatInterface):
        self.formatInterface = formatInterface

    def execute(self):
        try:
            print("Fix appendix")
            fixClausula = self.formatInterface.fixClausulaAdicional()
            return fixClausula
        except Exception as exc:
            print(exc)

class FixContractUseCase:
    def __init__(self, formatInterface):
        self.formatInterface = formatInterface

    def execute(self):
        try:
            print("Fix contract")
            fixContract = self.formatInterface.fixContract()
            return fixContract
        except Exception as exc:
            print(exc)

class EditSignersUseCase:
    def __init__(self, editSignersInterface):
        self.editSignersInterface = editSignersInterface

    def execute(self, path, body):
        try:
            update = self.editSignersInterface.update(path, body)
            return update
        except Exception as exc:
            print(exc)

class CreateContractUseCase:
    def __init__(self, contractInterface):
        self.contractInterface = contractInterface

    def execute(self):
        try:
            create = self.contractInterface.create()
        except Exception as exc:
            print(exc)

class ExtractSigners:
    def __init__(self, extractSignersInterface):
        self.signersInterface = extractSignersInterface

    def execute(self):
        try:
            signers = self.signersInterface.get()
        except Exception as exc:
            print(exc)