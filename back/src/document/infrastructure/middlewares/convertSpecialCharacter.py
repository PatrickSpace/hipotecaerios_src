def convertSpecialCharacter(data):
    """ data es un diccionario con la siguiente estructura
        { 
            comparecientes: [lista de diccionarios],
            banco: diccionario,
            inmobiliaria: diccionario
        } 
    """
    if "comparecientes" in data.keys():
        for item in range(len(data["comparecientes"])):
            for key in data["comparecientes"][item].keys():
                comp = data["comparecientes"][item][key]
                data["comparecientes"][item][key] = data["comparecientes"][item][key].replace("Ã‘", "Ñ") if isinstance(comp, str) else ""#data["comparecientes"][item][key].replace("Ã‘", "Ñ")
                data["comparecientes"][item][key] = data["comparecientes"][item][key].replace("Â°", "°") if isinstance(comp, str) else ""
    if "banco" in data.keys():
        for key in data["banco"].keys():
            bank = data["banco"][key]
            data["banco"][key] = data["banco"][key].replace("Ã‘", "Ñ") if isinstance(bank, str) else ""
            data["banco"][key] = data["banco"][key].replace("Â°", "°") if isinstance(bank, str) else ""
    if "inmobiliaria" in data.keys():
        for key in data["inmobiliaria"].keys():
            inmo = data["inmobiliaria"][key]
            data["inmobiliaria"][key] = data["inmobiliaria"][key].replace("Ã‘", "Ñ") if isinstance(inmo, str) else ""
            data["inmobiliaria"][key] = data["inmobiliaria"][key].replace("Â°", "°") if isinstance(inmo, str) else ""

    return data