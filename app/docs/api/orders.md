# Menus
Obtener Ordenes, mandar leer ordenes

### Lista de ordenes

**Request**:

`GET` `/api/v1/orders/`

Parametros:

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
200 Ok

{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "dish": {
                "name": "Sopa de Arroz, Spaguetti rojo, Milanesa con papa, platanos con crmea",
                "description": "cescripcion",
                "id": 1
            },
            "specifications": "Sin queso por favor , option 1",
            "employee": {
                "name": "antonio"
            }
        },
        {
            "dish": {
                "name": "Sopa de Arroz, Spaguetti rojo, Milanesa con papa, platanos con crmea",
                "description": "cescripcion",
                "id": 1
            },
            "specifications": "Sin queso por favor , option 1",
            "employee": {
                "name": "antonio"
            }
        },
        {
            "dish": {
                "name": "Sopa de Arroz, Spaguetti rojo, Milanesa con papa, platanos con crmea",
                "description": "cescripcion",
                "id": 1
            },
            "specifications": "Sin queso por favor , option 1",
            "employee": {
                "name": "antonio"
            }
        },
        {
            "dish": {
                "name": "Sopa de Arroz, Spaguetti rojo, Milanesa con papa, platanos con crmea",
                "description": "cescripcion",
                "id": 1
            },
            "specifications": "Sin queso por favor , option 1",
            "employee": {
                "name": "antonio"
            }
        },
        {
            "dish": {
                "name": "Sopa de Arroz, Spaguetti rojo, Milanesa con papa, platanos con crmea",
                "description": "cescripcion",
                "id": 1
            },
            "specifications": "Sin queso por favor , option 1",
            "employee": {
                "name": "antonio"
            }
        }
    ]
}
```

### Mandar leer pedidos

En caso de no ser las 11 de la mañana, esta url servira para leer los pedidos por slack

**Request**:

`GET` `/get_orders/`

*Nota:*

- Demanera algo rustica para poder seleccionar de manera satisfactoria un menu, por slack deberan escribir que opcion del menu desean como mensaje por slack
`e.g option 1` y las instrucciones consiguientes (si hubieran) con mensaje normal `(e.g no tomatoes)`
- Not Authorization Protected

**Response**:

```json
Content-Type application/json
200 Ok
```



