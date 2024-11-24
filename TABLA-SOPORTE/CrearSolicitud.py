import boto3
import uuid
from datetime import datetime

# Obtener referencia a la tabla DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLA-SOPORTE')

def lambda_handler(event, context):
    try:
        # Cargar el cuerpo de la solicitud y convertirlo a un diccionario
        data = eval(event['body']) if isinstance(event['body'], str) else event['body']
        
        # Validar campos requeridos
        if 'usuario_id' not in data or 'Titulo' not in data or 'descripcion' not in data:
            return {
                'statusCode': 400,
                'body': {
                    "error": "Campos 'usuario_id', 'Titulo' y 'descripcion' son obligatorios"
                }
            }
        
        # Extraer datos del cuerpo
        usuario_id = data['usuario_id']
        titulo = data['Titulo']
        descripcion = data['descripcion']
        
        # Generar ticket ID y fecha
        ticket_id = str(uuid.uuid4())
        fecha = datetime.utcnow().isoformat()
        
        # Crear item para insertar en DynamoDB
        item = {
            'usuario_id': usuario_id,
            'ticket_id': ticket_id,
            'Titulo': titulo,
            'descripcion': descripcion,
            'estado': 'pendiente',
            'fecha': fecha
        }
        
        # Insertar en DynamoDB
        table.put_item(Item=item)
        
        # Respuesta de éxito
        return {
            'statusCode': 200,
            'body': {
                "message": "Solicitud de soporte creada correctamente",
                "data": {
                    "usuario_id": usuario_id,
                    "ticket_id": ticket_id,
                    "Titulo": titulo,
                    "descripcion": descripcion,
                    "estado": "pendiente",
                    "fecha": fecha
                }
            }
        }

    except Exception as e:
        # Respuesta de error
        return {
            'statusCode': 500,
            'body': {
                "error": "Error interno del servidor",
                "details": str(e)
            }
        }
