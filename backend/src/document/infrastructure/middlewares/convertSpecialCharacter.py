def convertSpecialCharacter(data):
    """ data es un diccionario con la siguiente estructura
        { 
            comparecientes: [lista de diccionarios],
            banco: diccionario,
            inmobiliaria: diccionario
        } 
    """
    for item in range(len(data["comparecientes"])):
        for key in data["comparecientes"][item].keys():
            data["comparecientes"][item][key] = data["comparecientes"][item][key].replace("Ã‘", "Ñ")
            data["comparecientes"][item][key] = data["comparecientes"][item][key].replace("Â°", "°")
    for key in data["banco"].keys():
        data["banco"][key] = data["banco"][key].replace("Ã‘", "Ñ")
        data["banco"][key] = data["banco"][key].replace("Â°", "°")
    for key in data["inmobiliaria"].keys():
        data["inmobiliaria"][key] = data["inmobiliaria"][key].replace("Ã‘", "Ñ")
        data["inmobiliaria"][key] = data["inmobiliaria"][key].replace("Â°", "°")

    return data