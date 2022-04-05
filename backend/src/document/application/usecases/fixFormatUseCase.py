from backend.src.document.infrastructure.middlewares.printExceptionInfo import *

class FixFormatDocumentUseCase:
    def __init__(self, formatInterface, threadInterface):
        self.formatInterface = formatInterface
        self.threadInterface = threadInterface
    
    def execute(self, typeEntity):
        try:
            if typeEntity == "banco":
                fixFormat = self.formatInterface.fixContract()
                self.threadInterface.closeThreading()
                return fixFormat
            else:
                fixFormat = self.formatInterface.fix()
                self.threadInterface.closeThreading()
                return fixFormat
        except Exception as exc:
            printExceptionInfo(exc)
        finally:
            print("finally format")