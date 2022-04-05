<h1>Interfaz gráfica<h1>

<h3>Documentación<h3>

Ruta: http://direccion:puerto/api/bothip/documentacion
Método: POST
enviar:
```json
body = {
    "path": "C:\\Users\\Alejandro Herrera\\Documents\\Desarrollo2\\bloomcker\\20210222BotHip\\alcanfores\\alcanfores-459680\\459680-1.rtf",
}
```

Respuesta:
```json
data = {
    "comparecientes" : [{
        "nombre": "Ricardo Enrique Swayne Kleiman",
        "nacionalidad": "peruana",
        "estadoCivil": "casado",
        "profesion": "empresario",
        "domicilio": "Lima",
        "dni": "10559097",
        "representante": "comprador"
    }, {
        "nombre": "Ruth Lina Guillermo Egoavil",
        "nacionalidad": "peruana",
        "estado civil": "soltera",
        "profesion": "contadora",
        "domicilio": "calle 45, manzana 222, distrito santa ana, provincia y departamento de Lima",
        "dni": "45328070",
        "representante": "vendedor"
    }, {
        "nombre": "Abraham Noguera Pizarro",
        "nacionalidad": "peruana",
        "estado civil": "soltero",
        "profesion": "funcionario",
        "domicilio": "Lima",
        "dni": "41779438",
        "representante": "banco"
    }, {
        "nombre": "Tomas Arturo Acevedo Cuba",
        "nacionalidad": "peruana",
        "estado civil": "soltera",
        "profesion": "empresario",
        "domicilio": "Lima",
        "dni": "10718548",
        "representante": "inmobiliaria"
    }
    ],
    "banco": {
        "nombre": "Banco Internacional de Peru S.A.A",
        "ruc": 20100053455,
        "domicilio": "JIRON CARLOS VILLARAN NUMERO 140, URBANIZACION SANTA CATALINA, DISTRITO DE LA VICTORIA, PROVINCIA Y DEPARTAMENTO DE LIMA"
    },
    "inmobiliaria": {
        "nombre": "Paz Centenario S.A",
        "ruc": 20518023579,
        "domicilio": "AVENIDA CAMINO REAL NUMERO 390, TORRE CENTRAL, PISO 17, OFICINA 1701, DISTRITO DE SAN ISIDRO, PROVINCIA Y DEPARTAMENTO DE LIMA"
    }
}
```

<h3>Comparecientes<h3>

Ruta: http://direccion:puerto/api/bothip/comparecientes/<id>
Método: POST
Enviar: json
```json
data = {
    "comparecientes" : [{
        "nombre": "Ricardo Enrique Swayne Kleiman",
        "nacionalidad": "peruana",
        "estadoCivil": "casado",
        "profesion": "empresario",
        "domicilio": "Lima",
        "dni": "10559097",
        "representante": "comprador"
    }, {
        "nombre": "Ruth Lina Guillermo Egoavil",
        "nacionalidad": "peruana",
        "estado civil": "soltera",
        "profesion": "contadora",
        "domicilio": "calle 45, manzana 222, distrito santa ana, provincia y departamento de Lima",
        "dni": "45328070",
        "representante": "vendedor"
    }, {
        "nombre": "Abraham Noguera Pizarro",
        "nacionalidad": "peruana",
        "estado civil": "soltero",
        "profesion": "funcionario",
        "domicilio": "Lima",
        "dni": "41779438",
        "representante": "banco"
    }, {
        "nombre": "Tomas Arturo Acevedo Cuba",
        "nacionalidad": "peruana",
        "estado civil": "soltera",
        "profesion": "empresario",
        "domicilio": "Lima",
        "dni": "10718548",
        "representante": "inmobiliaria"
    }
    ],
    "banco": {
        "nombre": "Banco Internacional de Peru S.A.A",
        "ruc": 20100053455,
        "domicilio": "JIRON CARLOS VILLARAN NUMERO 140, URBANIZACION SANTA CATALINA, DISTRITO DE LA VICTORIA, PROVINCIA Y DEPARTAMENTO DE LIMA"
    },
    "inmobiliaria": {
        "nombre": "Paz Centenario S.A",
        "ruc": 20518023579,
        "domicilio": "AVENIDA CAMINO REAL NUMERO 390, TORRE CENTRAL, PISO 17, OFICINA 1701, DISTRITO DE SAN ISIDRO, PROVINCIA Y DEPARTAMENTO DE LIMA"
    }
}
```
Respuesta:
```json
{
    "mensaje": "Actualizado con exito"
}
```
<h3>Generar documento<h3>

Ruta: http://direccion:puerto/api/bothip/documentacion
Método: GET
Enviar:
Respuesta:
```json
mensaje = {"mensaje": "Documento procesado"}
```