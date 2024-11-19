# TABLA-PAGOS

Aquí tienes los ejemplos de JSON que puedes usar en Postman para probar cada caso:

---

### 1. **POST - Crear Pago por Deuda**

Endpoint: `/pago/deuda`

#### Request JSON:
```json
{
  "usuario_id": "user123",
  "datos_pago": {
    "monto": 150,
    "titulo": "Pago de Deuda",
    "descripcion": "Pago de deuda por servicios básicos"
  }
}
```

#### Expected Response JSON:
```json
{
  "usuario_id": "user123",
  "pago_id": "generated-uuid",
  "titulo": "Pago de Deuda",
  "descripcion": "Pago de deuda por servicios básicos",
  "tipo": "deuda",
  "monto": 150,
  "estado": "pendiente",
  "fecha": "2024-11-13T12:00:00Z"
}
```

---

### 2. **POST - Crear Pago por Servicio**

Endpoint: `/pago/servicio`

#### Request JSON:
```json
{
  "usuario_id": "user123",
  "datos_servicio": {
    "monto": 200,
    "titulo": "Pago de Servicio",
    "descripcion": "Servicio de suscripción mensual"
  }
}
```

#### Expected Response JSON:
```json
{
  "usuario_id": "user123",
  "pago_id": "generated-uuid",
  "titulo": "Pago de Servicio",
  "descripcion": "Servicio de suscripción mensual",
  "tipo": "servicio",
  "monto": 200,
  "estado": "pendiente",
  "fecha": "2024-11-13T12:00:00Z"
}
```

---

### 3. **POST - Realizar Pago (Usuario)**

Endpoint: `/pago/realizar`

#### Request JSON:
```json
{
  "usuario_id": "user123",
  "cuenta_id": "account456",
  "tarjeta_id": "card789",
  "pago_id": "generated-uuid"
}
```

#### Expected Response JSON:
```json
{
  "usuario_id": "user123",
  "pago_id": "generated-uuid",
  "cuenta_id": "account456",
  "tarjeta_id": "card789",
  "descripcion": "Pago realizado por el usuario",
  "tipo": "deuda o servicio (dependiendo del pago)",
  "monto": 200,
  "estado": "pagado",
  "fecha": "2024-11-13T12:30:00Z",
  "mensaje": "El pago fue realizado el 2024-11-13T12:30:00Z por el usuario con ID user123, usando la tarjeta card789, a través de la cuenta account456, por un monto de 200. Tipo de pago: deuda o servicio."
}
```

---

### 4. **GET - Obtener Pago por ID**

Endpoint: `/pago/obtener`

#### Request JSON:
```json
{
  "usuario_id": "user123",
  "pago_id": "generated-uuid"
}
```

#### Expected Response JSON (If the payment exists):
```json
{
  "usuario_id": "user123",
  "pago_id": "generated-uuid",
  "titulo": "Pago de Servicio",
  "descripcion": "Servicio de suscripción mensual",
  "tipo": "servicio",
  "monto": 200,
  "estado": "pendiente",
  "fecha": "2024-11-13T12:00:00Z"
}
```

#### Expected Response JSON (If the payment does not exist):
```json
{
  "statusCode": 404,
  "body": "Pago no encontrado"
}
```

---

### 5. **GET - Listar Todos los Pagos (Usuario)**

Endpoint: `/pago/listar`

#### Request JSON:
```json
{
  "usuario_id": "user123"
}
```

#### Expected Response JSON:
```json
[
  {
    "usuario_id": "user123",
    "pago_id": "uuid1",
    "titulo": "Pago de Deuda",
    "descripcion": "Pago de deuda por servicios básicos",
    "tipo": "deuda",
    "monto": 150,
    "estado": "pendiente",
    "fecha": "2024-11-13T12:00:00Z"
  },
  {
    "usuario_id": "user123",
    "pago_id": "uuid2",
    "titulo": "Pago de Servicio",
    "descripcion": "Servicio de suscripción mensual",
    "tipo": "servicio",
    "monto": 200,
    "estado": "pendiente",
    "fecha": "2024-11-13T12:05:00Z"
  }
]
```

---

### 6. **PUT - Actualizar Estado de Pago (Administrador)**

Endpoint: `/pago/actualizar`

#### Request JSON:
```json
{
  "usuario_id": "user123",
  "pago_id": "generated-uuid",
  "estado": "pagado"
}
```

#### Expected Response JSON:
```json
{
  "statusCode": 200,
  "body": "Pago generated-uuid actualizado con estado pagado"
}
```

---

### 7. **DELETE - Eliminar Pago (Administrador)**

Endpoint: `/pago/eliminar`

#### Request JSON:
```json
{
  "usuario_id": "user123",
  "pago_id": "generated-uuid"
}
```

#### Expected Response JSON:
```json
{
  "statusCode": 200,
  "body": "Pago generated-uuid eliminado exitosamente"
}
```

---

These JSON examples should be suitable for each of your API endpoints in Postman. Let me know if you need further adjustments!
