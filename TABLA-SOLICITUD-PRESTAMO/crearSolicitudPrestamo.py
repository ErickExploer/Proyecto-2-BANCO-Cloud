import boto3
import json
import uuid
from decimal import Decimal
from datetime import datetime

# Conexión con DynamoDB
dynamodb = boto3.resource('dynamodb')
solicitud_table = dynamodb.Table('TABLA-SOLICITUD-PRESTAMO')

# Función auxiliar para convertir Decimal a tipos serializables
def decimal_to_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 != 0 else int(obj)
    elif isinstance(obj, list):
        return [decimal_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: decimal_to_serializable(value) for key, value in obj.items()}
    return obj

def lambda_handler(event, context):
    try:
        # Validar que el cuerpo del evento exista
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud'
                }
            }

        # Parsear el cuerpo de la solicitud
        try:
            data = json.loads(event['body'])
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'El cuerpo de la solicitud no está en formato JSON válido'
                }
            }

        # Validar campos requeridos
        usuario_id = data.get('usuario_id')
        monto = data.get('monto')
        descripcion = data.get('descripcion', 'Solicitud de préstamo')

        if not usuario_id or not monto:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'Faltan campos obligatorios: usuario_id o monto'
                }
            }

        # Crear la solicitud
        solicitud_id = str(uuid.uuid4())
        fecha_creacion = datetime.utcnow().isoformat()

        # Convertir monto a Decimal
        try:
            monto = Decimal(str(monto))
        except Exception:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Monto inválido',
                    'details': 'El monto debe ser un número válido'
                }
            }

        item = {
            'usuario_id': usuario_id,
            'solicitud_id': solicitud_id,
            'monto': monto,
            'descripcion': descripcion,
            'estado': 'pendiente',
            'fecha_creacion': fecha_creacion
        }

        solicitud_table.put_item(Item=item)

        # Convertir el resultado a un formato JSON serializable
        return {
            'statusCode': 200,
            'body': decimal_to_serializable(item)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno al crear la solicitud',
                'details': str(e)
            }
        }
