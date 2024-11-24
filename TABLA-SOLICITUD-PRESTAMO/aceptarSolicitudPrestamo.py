import boto3
import json
from decimal import Decimal

# Conexión a DynamoDB
dynamodb = boto3.resource('dynamodb')
solicitud_table = dynamodb.Table('TABLA-SOLICITUD-PRESTAMO')

# Función auxiliar para convertir tipos Decimal a JSON serializables
def decimal_to_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 != 0 else int(obj)
    elif isinstance(obj, list):
        return [decimal_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: decimal_to_serializable(value) for key, value in obj.items()}
    return obj

# Función Lambda
def lambda_handler(event, context):
    try:
        # Validar el cuerpo de la solicitud
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud'
                }
            }

        # Parsear el cuerpo de la solicitud
        data = json.loads(event['body'])
        
        usuario_id = data.get('usuario_id')
        solicitud_id = data.get('solicitud_id')

        # Validar que usuario_id y solicitud_id estén presentes
        if not usuario_id or not solicitud_id:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'Los campos usuario_id y solicitud_id son obligatorios'
                }
            }

        # Obtener la solicitud desde DynamoDB
        response = solicitud_table.get_item(Key={'usuario_id': usuario_id, 'solicitud_id': solicitud_id})
        solicitud = response.get('Item')

        # Validar si la solicitud existe
        if not solicitud:
            return {
                'statusCode': 404,
                'body': {'error': 'Solicitud no encontrada'}
            }

        # Manejar estados de la solicitud
        estado_actual = solicitud.get('estado')
        if estado_actual == 'rechazado':
            return {
                'statusCode': 400,
                'body': {
                    'message': 'La solicitud ya fue rechazada',
                    'estado_actual': estado_actual
                }
            }
        elif estado_actual == 'aceptado':
            return {
                'statusCode': 400,
                'body': {
                    'message': 'La solicitud ya fue aceptada previamente',
                    'estado_actual': estado_actual
                }
            }
        elif estado_actual == 'pendiente':
            # Actualizar el estado de la solicitud a 'aceptado'
            solicitud_table.update_item(
                Key={'usuario_id': usuario_id, 'solicitud_id': solicitud_id},
                UpdateExpression='SET estado = :estado',
                ExpressionAttributeValues={':estado': 'aceptado'}
            )

            return {
                'statusCode': 200,
                'body': {
                    'message': 'Solicitud aceptada exitosamente',
                    'usuario_id': usuario_id,
                    'solicitud_id': solicitud_id,
                    'nuevo_estado': 'aceptado'
                }
            }

        # Manejo de estados desconocidos (si ocurre)
        return {
            'statusCode': 400,
            'body': {
                'error': 'Estado desconocido',
                'estado_actual': estado_actual
            }
        }

    except Exception as e:
        # Manejo de errores generales
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno al procesar la solicitud',
                'details': str(e)
            }
        }
