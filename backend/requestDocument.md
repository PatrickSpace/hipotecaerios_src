<h1> Interfaz gráfica de la aplicación </h1>

<h3> Carga de Documentos en el Sistema </h3>

```json
{
    "Entrada Minuta": {
        "elementType": "input-file",
        "predifined": false,
        "dataType": "document",
        "required": false,
        "format": [".docx", ".doc", ".rtf"]
    },
    "Minuta": {
        "elementType": "button",
        "predifined": true,
        "dataType": "submit",
        "required": false
    },
    "Entrada Clausula": {
        "elementType": "input-file",
        "predifined": false,
        "dataType": "list-documents",
        "required": false,
        "format": [".docx", ".doc", ".rtf"]
    },
    "Clausula": {
        "elementType": "button",
        "predifined": true,
        "dataType": "submit",
        "required": false
    },
    "Entrada Prestamo": {
        "elementType": "input-file",
        "predifined": false,
        "dataType": "document",
        "required": false,
        "format": [".docx", ".doc", ".rtf"]
    },
    "Prestamo": {
        "elementType": "button",
        "predifined": true,
        "dataType": "submit",
        "required": false
    },
    "Entrada Imagenes": {
        "elementType": "input-file",
        "predifined": false,
        "dataType": "list-images",
        "required": false,
        "format": [".jpeg", ".png"]
    },
    "Imagenes": {
        "elementType": "button",
        "predifined": true,
        "dataType": "submit",
        "required": false
        },
    "Aceptar": {
        "elementType": "button",
        "predifined": true,
        "dataType": "submit",
        "required": false
    },
    "Cancelar": {
        "elementType": "button",
        "predifined": true,
        "dataType": "submit",
        "required": false
    }
}
```

<h3> Comparecientes </h3>
Datos que se extraen de la minuta y clausulas

```json
{
    "Representantes": {
        "Nombre y Apellido": "list-string",
        "Nacionalidad": "list-string",
        "Estado Civil": "list-string",
        "Domicilio": "list-string",
        "Profesion": "list-string",
        "DNI": "list-string"
    }
}
```

```json
{
    "Banco": {
        "Nombre": "string",
        "Domicilio": "string"
    }
}
```

```json
{
    "Inmobiliaria": {
        "Nombre": "string",
        "Domicilio": "string",
        "RUC": "string"
    }
}
```

<h3> Generar Documento </h3>

```json
{
    "Generar": {
        "elementType": "button",
        "predifined": true,
        "dataType": "submit",
        "required": false
    }
}
```

<h3> ejemplo request </h3>

```json
comparecientes = [{
    "nombre": "Ricardo Enrique Swayne Kleiman",
    "nacionalidad": "peruana",
    "estadoCivil": "casado",
    "profesion": "empresario",
    "domicilio": "Lima",
    "dni": "10559097"
}, {
    "nombre": "Ruth Lina Guillermo Egoavil",
    "nacionalidad": "peruana",
    "estado civil": "soltera",
    "profesion": "contadora",
    "domicilio": "calle 45, manzana 222, distrito santa ana, provincia y departamento de Lima",
    "dni": "45328070"
}, {
    "nombre": "Abraham Noguera Pizarro",
    "nacionalidad": "peruana",
    "estado civil": "soltero",
    "profesion": "funcionario",
    "domicilio": "Lima",
    "dni": "41779438"
}, {
    "nombre": "Tomas Arturo Acevedo Cuba",
    "nacionalidad": "peruana",
    "estado civil": "soltera",
    "profesion": "funcionario",
    "domicilio": "Lima",
    "dni": "10718548"
}
]
```

```json
{
    "banco": {
        "nombre": "Banco Internacional de Peru S.A.A",
        "ruc": 20100053455,
        "domicilio": "JIRON CARLOS VILLARAN NUMERO 140, URBANIZACION SANTA CATALINA, DISTRITO DE LA VICTORIA, PROVINCIA Y DEPARTAMENTO DE LIMA"
    }
}
```

```json
{
    "inmobiliaria": {
        "nombre": "Paz Centenario S.A",
        "ruc": 20518023579,
        "domicilio": "AVENIDA CAMINO REAL NUMERO 390, TORRE CENTRAL, PISO 17, OFICINA 1701, DISTRITO DE SAN ISIDRO, PROVINCIA Y DEPARTAMENTO DE LIMA"
    }
}
```
