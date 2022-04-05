class Company:
    def __init__(self):
        pass

    def detect(self, document, typeEntity):
        companyName = None
        if typeEntity == 'banco':
            print("banco")
            lista = [
                'BANCO DE CREDITO DEL PERU',
                'SCOTIABANK PERU S.A.A.',
                'INTERBANK',
                'BANCO BBVA PERU'
            ]
            for banco in lista:
                isBanco = document.Content.Find.Execute(FindText=banco)
                if isBanco:
                    companyName = banco
        elif typeEntity == 'inmobiliaria':
            print("inmobiliaria")
            lista = [
                'PROMOTORA ALBAMAR S.A.C.',
                'INVERSIONES INMOBILIARIAS ALCANFORES S.A.C.',
                'BUENAS INVERSIONES S.A.C',
                'CP BUILDING SAC',
                'PROYECTOS EDIFICA',
                'ESPINOSA ARQUITECTOS S.A.C.',
                'ESPINOZA ARQUITECTOS S.A.C.',
                'INVERSIONES INMOBILIARIAS DEL INDICO S.A.',
                'LIDER INGENIERIA Y CONSTRUCCION S.A.',
                'JOSMI GRUPO INVERSOR S.A.C.',
                'MIRANDA CONSTRUCTORES S.A.',
                'PAZ CENTENARIO S.A.',
                'QUATRO BETA S.A.C.',
                'QUATRO EPSILON S.A.C.',
                'INVERSIONES ROCAZUL S.A.C',
                'VIENNA CONSTRUCTORES'
            ]
            for inmobiliaria in lista:
                isInmobiliaria = document.Content.Find.Execute(FindText=inmobiliaria)
                if isInmobiliaria:
                    companyName = inmobiliaria
        
        return companyName