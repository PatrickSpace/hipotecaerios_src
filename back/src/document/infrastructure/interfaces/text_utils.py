import re
from num2words import num2words
from future.utils import iteritems

def substitute_underscore(string_):
    if re.search(r'(?<=((\s)|(\d)|([^_])))(_{2,11})(?=(\.|\,|[^_]))', string_):
        result = re.sub(r'^(_{2,11})(?=(\.|\,|[^_]))', '.== == ', re.sub(r'(?<=((\s)|(\d)|([^_])))(_{2,11})(?=(\.|\,|[^_]))', '.== == ', string_))
    elif re.search(r'^(_{11,})(?=(\.|\,|[^_]))', string_):
        result = re.sub(r'^(_{11,})(?=(\.|\,|[^_]))', '.== == .== == ', string_)
    elif re.search(r'(_{11,})', string_):
        result = re.sub(r'(_{11,})', '.== == .== == ', string_)
    else:
        result = string_

    return result

def removechars(cellvalue):
    text = re.sub(r"[\r\n\t\x07\x0b]", "", cellvalue)
    return text

def adjust_items(item):
    if re.search(r'^[a-zA-ZñÑ]\.$', item) or re.search(r'^\d+\.$', item):
        item = '(' + item.replace('.','') + ')'

    elif re.search(r'^[a-zA-ZñÑ]\)$', item): #or re.search(r'^\d+\)$', item):
        item = '(' + item
    
    if '' in item:
        item = item.replace('', '•')

    item = item.upper()
    return item

def is_int(string_):
    return string_.isdigit() or (string_.startswith('-') and string_[1:].isdigit())

def num_to_string(quantity, moneda=''):
    if moneda != '':
        moneda2 = ' ' + moneda
    else: 
        moneda2 = moneda
    if quantity[-1] == ',':
        quantity.replace(',','')
    if '%' in quantity:
        quantity = quantity.replace(',','')
        quantity1 = quantity.replace("%","")
        if '.' in quantity and quantity.index('.') != -1:
            cents = quantity1.split('.')[-1]
            integer = quantity1.split('.')[0]
            number1 = num2words(float(quantity1), to='cardinal', lang='es').upper()
            if int(integer) != 0:  
                words1 = num2words(int(integer),to='cardinal', lang='es').replace("uno mil", "un mil").upper()
            else: 
                words1 = ''
            words2 = num2words(int(cents), to='cardinal', lang='es').replace("uno mil", "un mil").upper()
            
            if cents[0] == '0':
                words_aux = list()
                for digit in cents:
                    
                    if digit == '0': 
                        words_aux.append(num2words(int(digit), to='cardinal', lang='es').replace('uno mil', 'un mil').upper())
                    
                    else: 
                        break

                if words2 != 'CERO':
                    words2 = ' '.join(words_aux) + ' '+ words2 
                else:
                    words2 = ''
                    words2 = ' '.join(words_aux) + words2 

            if integer[0] == '0':
                words_aux = list()
                for digit in integer:
                    
                    if digit == '0': 
                        words_aux.append(num2words(int(digit), to='cardinal', lang='es').replace('uno mil', 'un mil').upper())
                    
                    else: 
                        break
                
                
                words1 = ' '.join(words_aux) + ' '+ words1        
            #print(words_aux)
            #print(words2)
            
            #if cents == '00':
                #complete_quantity= " ({} PUNTO CERO CERO POR CIENTO) ".format(words1)
            #elif int(cents) in range(1,10):
                #complete_quantity = " ({} POR CIENTO) ".format(number1)  
            if quantity1.split('.')[0] == '':
                complete_quantity= " (PUNTO {} POR CIENTO) ".format(words2)
            else:
                complete_quantity= " ({} PUNTO {} POR CIENTO) ".format(words1,words2)

        else:
            integer = quantity1.split('.')[0]
            words1 = num2words(int(integer),to='cardinal', lang='es').replace("uno mil", "un mil").upper()
            complete_quantity = " ({} POR CIENTO) ".format(words1)

    elif 'M2' in quantity:
        quantity = quantity.replace(',','')
        quantity = quantity.replace(' ','')
        quantity1 = quantity.replace("M2","")
        if '.' in quantity and quantity.index('.') != -1:
            cents = quantity1.split('.')[-1]
            integer = quantity1.split('.')[0]
            number1 = num2words(float(quantity1), to='cardinal', lang='es').upper()
            if int(integer) != 0:  
                words1 = num2words(int(integer),to='cardinal', lang='es').replace("uno mil", "un mil").upper()
            else: 
                words1 = ''
            words2 = num2words(int(cents), to='cardinal', lang='es').replace("uno mil", "un mil").upper()
            
            if cents[0] == '0':
                words_aux = list()
                for digit in cents:
                    
                    if digit == '0': 
                        words_aux.append(num2words(int(digit), to='cardinal', lang='es').replace('uno mil', 'un mil').upper())
                    
                    else: 
                        break

                if words2 != 'CERO':
                    words2 = ' '.join(words_aux) + ' '+ words2 
                else:
                    words2 = ''
                    words2 = ' '.join(words_aux) + words2 

            if integer[0] == '0':
                words_aux = list()
                for digit in integer:
                    
                    if digit == '0': 
                        words_aux.append(num2words(int(digit), to='cardinal', lang='es').replace('uno mil', 'un mil').upper())
                    
                    else: 
                        break
                
                
                words1 = ' '.join(words_aux) + ' '+ words1        

            if quantity1.split('.')[0] == '':
                complete_quantity= " (PUNTO {} METROS CUADRADOS) ".format(words2)
            else:
                complete_quantity= " ({} PUNTO {} METROS CUADRADOS) ".format(words1,words2)

        else:
            integer = quantity1.split('.')[0]
            words1 = num2words(int(integer),to='cardinal', lang='es').replace("uno mil", "un mil").upper()
            complete_quantity = " ({} METROS CUADRADOS) ".format(words1)

    else:
        quantity = quantity.replace(',','')

        if is_int(quantity):
            #print(int(quantity))
            words = num2words(int(quantity), to='cardinal', lang='es') 

            
            if quantity[0] == '0':
                words_aux = list()
                for digit in quantity:
                    
                    if digit == '0': 
                        words_aux.append(num2words(int(digit), to='cardinal', lang='es').replace('uno mil', 'un mil').upper())
                    
                    else: 
                        break
                
                
                words = ' '.join(words_aux) + ' '+ words   
            
            complete_quantity = " ({}{})".format( words.upper(), moneda2)
            complete_quantity = re.sub(r'^\s+\(CERO\s+', ' (', complete_quantity) #Elimina el cero a la izquierda
        
        else:
            words = num2words(int(float(quantity)), to='cardinal', lang='es').replace("uno mil", "un mil").upper()
            point = quantity.index('.')
            cents = quantity[point+1:] 
            complete_quantity= " ({} Y {}/100{})".format(words, cents, moneda2)
    
    
    return complete_quantity

def date_to_string(text):
    
    meses = {'1':'enero', '01':'enero', '2':'febrero', '02':'febrero', '3': 'marzo', '03': 'marzo', 
    '4': 'abril', '04': 'abril', '5': 'mayo', '05': 'mayo', '6':'junio', '06':'junio', '7':'julio',
     '07':'julio', '8':'agosto', '08':'agosto', '9':'septiembre', '09':'septiembre', '10':'octubre',
      '11': 'noviembre', '12': 'diciembre'}
    fechas= re.findall(r'\d+/\d+/\d+|\d+-\d+-\d+', text)
    for fecha in fechas:
        if re.search(r'/', fecha):
            fecha2 = fecha.split('/')
        else:
            fecha2 = fecha.split('-')
        if int(fecha2[1]) in range(1,13) and len(fecha2[0])==2:
            dia = str(num2words(int(fecha2[0]),  to='cardinal', lang='es').upper())
            if dia == 'UNO':
                dia = 'PRIMERO'
            mes = str(meses[fecha2[1]].upper())
            año = str(num2words(int(fecha2[2]),  to='cardinal', lang='es').upper()) 
            fecha_escrita = fecha + ' ('+dia + ' DE ' + mes +' DEL ' + año +')'
            text = text.replace(fecha, fecha_escrita)
        elif int(fecha2[1]) in range(1,13) and len(fecha2[0])==4:
            dia = str(num2words(int(fecha2[2]),  to='cardinal', lang='es').upper())
            if dia == 'UNO':
                dia = 'PRIMERO'
            mes = str(meses[fecha2[1]].upper())
            año = str(num2words(int(fecha2[0]),  to='cardinal', lang='es').upper()) 
            fecha_escrita = fecha + ' ('+dia + ' DE ' + mes +' DEL ' + año +')'
            text = text.replace(fecha, fecha_escrita)
        else:
             pass
    
    text = extend_year_with_point(text)
    
    return text

def date_to_string_with_point(text):
    
    meses = {'1':'enero', '01':'enero', '2':'febrero', '02':'febrero', '3': 'marzo', '03': 'marzo', 
    '4': 'abril', '04': 'abril', '5': 'mayo', '05': 'mayo', '6':'junio', '06':'junio', '7':'julio',
     '07':'julio', '8':'agosto', '08':'agosto', '9':'septiembre', '09':'septiembre', '10':'octubre',
      '11': 'noviembre', '12': 'diciembre'}
    fechas= re.findall(r'\d+\.\d+\.\d+', text) 
    for fecha in fechas: 
        fecha2 = fecha.split('.')
        if int(fecha2[1]) in range(1,13):
            dia = str(num2words(int(fecha2[0]),  to='cardinal', lang='es').upper())
            if dia == 'UNO':
                dia = 'PRIMERO'
            mes = str(meses[fecha2[1]].upper())
            año = str(num2words(int(fecha2[2]),  to='cardinal', lang='es').upper()) 
            fecha_escrita = fecha + ' ('+dia + ' DE ' + mes +' DEL ' + año +')'
            text = text.replace(fecha, fecha_escrita)
        else:
             pass
    
    text = extend_year_with_point(text)
    
    return text

def extend_year_with_point(text):
    lista = re.findall(r'(:?^|\s)([1-2][0-9][0-9][0-9])(\.)(?!\S)', text)
    años = [x for i in lista for x in i if x != '.' and x != '' and  x !=' ']
    
    for año in años:
        año_extendido =  str(num2words(int(año),  to='cardinal', lang='es').upper())
        text= text.replace(año, año+' ('+año_extendido+')')
    return text

def extended_numbers(string_, moneda_ = ''):
    #print([string_])
    moneda2 = moneda_.replace('¢','O')
    if "US$" in string_ or 'S/' in string_ or "M2" in string_: 

        if "US$" in string_:
            string_ = string_.replace('US$', 'US$ ')
            moneda2 = 'DOLARES AMERICANOS'
        elif 'S/' in string_:
            string_ = string_.replace('S/', 'S/ ')
            moneda2 = 'SOLES'
        if "M2" not in string_:
            non_percentage_substring = re.findall(r'(:?^|\s)(?=.)((?:0|(?:[0-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[0-9])?)?(\.)?(\,)?(?!\S)', string_)
            non_percentage_substring = [element[1] for element in non_percentage_substring if element[1] != '']
        else:
            non_percentage_substring = []
        percentage_substring = re.findall(r'(:?^|\s)(?=.)((?:0|(?:[0-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[0-9])?%)?(\.\,)?(\.)?(\,)?(?!\S)', string_)
        percentage_substring = [element[1] for element in percentage_substring if element[1] != '']
        area_substring = re.findall(r'(:?^|\s)(?=.)((?:0|(?:[0-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[0-9])?\s+M2)?(\.\,)?(\.)?(\,)?(?!\S)', string_)
        area_substring = [element[1] for element in area_substring if element[1] != '']
        
            
        if non_percentage_substring != []:
            start = 0
            for word in non_percentage_substring:
                if not re.search(r'{}\s+M2'.format(word), string_):
                    indice = string_.index(word, start) + len(word) 
                    string_ = string_[:indice]  + num_to_string(word, moneda = moneda2) + string_[indice:]
            start = indice 
        if percentage_substring != []:
            start = 0
            for word in percentage_substring:
                #print(string_,"----", word)
                if word[0] == '.':
                    indice = string_.index(word, start) + len(word) 
                    string_ = string_[:indice] + num_to_string('0' + word, moneda = '') + string_[indice+1:]
                else:
                    indice = string_.index(word, start) + len(word) 
                    string_ = string_[:indice] + num_to_string(word, moneda = '') + string_[indice+1:]
                start = indice 

        if area_substring != []:
            start = 0
            for word in area_substring:
                if word[0] == '.':
                    indice = string_.index(word, start) + len(word)
                    string_ = string_[:indice] + num_to_string('0' + word, moneda = '') + string_[indice+1:]
                else:
                    #print(string_,"----", word)
                    indice = string_.index(word, start) + len(word)
                    string_ = string_[:indice] + num_to_string(word, moneda = '') + string_[indice+1:]
                start = indice
    else: 
        non_percentage_substring = re.findall(r'(:?^|\s)(?=.)((?:0|(?:[0-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[0-9])?)?(?!\S)', string_)
        non_percentage_substring = [element[1] for element in non_percentage_substring if element[1] != '']
        percentage_substring = re.findall(r'(:?^|\s)(?=.)((?:0|(?:[0-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[0-9])?%)?(\.)?(\,)?(?!\S)', string_)
        percentage_substring = [element[1] for element in percentage_substring if element[1] != '']
        area_substring = re.findall(r'(:?^|\s)(?=.)((?:0|(?:[0-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[0-9])?\s+M2)?(\.\,)?(\.)?(\,)?(?!\S)', string_)
        area_substring = [element[1] for element in area_substring if element[1] != '']
        
        if non_percentage_substring != []:
            #print([string_])
            start = 0
            for word in non_percentage_substring:
                if not re.search(r'{}\s+M2'.format(word), string_):
                    if word.strip().isdigit():
                        indice = string_.index(word, start) + len(word) 
                        string_ = string_[:indice]  + num_to_string(word, moneda = '') + string_[indice:]
                    else:
                        indice = string_.index(word, start) + len(word) 
                        string_ = string_[:indice]  + num_to_string(word, moneda = moneda2) + string_[indice:]
                    start = indice 

        if percentage_substring != []:
            start = 0
            for word in percentage_substring:
                #print(string_,"----", word)
                if word[0] == '.':
                    indice = string_.index(word, start) + len(word)
                    string_ = string_[:indice] + ' (PUNTO ' + num_to_string(word[1:], moneda = '')[2:] + string_[indice:]
                else:
                    indice = string_.index(word, start) + len(word)
                    string_ = string_[:indice] + num_to_string(word, moneda = '') + string_[indice:]
                start = indice

        if area_substring != []:
            start = 0
            for word in area_substring:
                if word[0] == '.':
                    indice = string_.index(word, start) + len(word)
                    string_ = string_[:indice] + ' (PUNTO ' + num_to_string(word[1:], moneda = '')[2:] + string_[indice:]
                else:
                    indice = string_.index(word, start) + len(word)
                    string_ = string_[:indice] + num_to_string(word, moneda = '') + string_[indice:]
                start = indice

            
    
    string_ = extend_year_with_point(string_)
    string_ = date_to_string(string_)
    
    return string_
    
def remove_spaces(parrafo): 
    spaces_removed = " ".join(parrafo.split())
    spaces_removed = spaces_removed.replace(":", ": ")
    spaces_removed = spaces_removed.replace(" :", ": ")   
    spaces_removed = spaces_removed.replace("  ", " ")
    return spaces_removed

def normalize(string):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        string = string.replace(a, b).replace(a.upper(), b.upper())
    return string

def remove_special_characters(paragraph,special_characters):
    for num, esp_c in enumerate(special_characters):
        if num == 0:
            new_format = paragraph.replace(esp_c[0], esp_c[1])
        else:
            new_format = new_format.replace(esp_c[0], esp_c[1])

    return new_format

def fix_format(paragraph):
    new_format = remove_spaces(paragraph)
    new_format = remove_special_characters(new_format, [('\n', ''), ('\t', ' ')])
    new_format = normalize(new_format)

    return new_format

def removechars(cellvalue):
    text = re.sub(r"[\r\n\t\x07\x0b]", "", cellvalue)
    return text

def replace_directions(text):
    dic_abrev = {'AV.':'AVENIDA ', 'AV ': 'AVENIDA ', 'JR.': 'JIRON ', 'JR ' : 'JIRON ', 'DPTO.' :'DEPARTAMENTO ', 'DPTO': 'DEPARTAMENTO ',
     'ALT ' : 'ALTURA ', 'ALT.' : 'ALTURA ', 'CDRA.': 'CUADRA ', 'CDRA ': 'CUADRA ', 'NRO.' :	'NUMERO ', 'NRO ' : 'NUMERO ', 'Nº' : 'NUMERO', 'N°' : 'NUMERO', 
     'CAR.' : 'CARRETERA ', 'CARR.' : 'CARRETERA ', 'KM.' : 'KILOMETRO', 'CAR.CAR.': 'CARRETERA', 'URB.': 'URBANIZACION', 'CAL.': 'CALLE ', 'ET.':'ETAPA', '1RA':'PRIMERA' }
 
    for i, j in iteritems(dic_abrev):
        text = text.replace(i, j)
     

    match = re.search(r'(?i)(-)(\s)*(.+)(\s)+(-)(\s)+(.+)(\s)', text)
    if match != None:
        string = text[match.span()[0]:match.span()[1]]
        dis_dep = string.split('-')

        text = text.replace(string, 'DISTRITO DE {}, PROVINCIA Y DEPARTAMENTO DE {}'.format(dis_dep[2].strip(), dis_dep[1].strip()))

    return text

def remove_special_characters(paragraph,special_characters):
    for num, esp_c in enumerate(special_characters):
        if num == 0:
            new_format = paragraph.replace(esp_c[0], esp_c[1])
        else:
            new_format = new_format.replace(esp_c[0], esp_c[1])

    return new_format

def dni_modifications(paragraph):
    if re.search(r'(?i)(nombre)?(\s*)(\(s\))?(del)*(\s*)(\(de los\))*(\s*)(representante)(s)?(\s)*(legales)?', paragraph) and re.search(r'(?i)D\.?N\.?I', paragraph):
        result = remove_special_characters(re.sub(r'(?i)D\.?N\.?I', '.== == DNI', paragraph), [('\t', ' ')])
    elif re.search(r'(\(\d\))', paragraph ) and re.search(r'(?i)D\.?N\.?I', paragraph):
        result = remove_special_characters(re.sub(r'(?i)D\.?N\.?I', '.== == DNI', paragraph), [('\t', ' ')])
    else:
        result = paragraph

    return result

def extend_date(paragraph):
    if re.search(r'(?i)([0-3]?[0-9])(\s)+(de)(\s)+(enero|ferebro|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre)(\s)+(de|del)(\s)+([2][0-1][0-9][0-9])(\.)?', paragraph):
        result = extended_numbers(paragraph) 
    else: 
        result = paragraph
    return result






