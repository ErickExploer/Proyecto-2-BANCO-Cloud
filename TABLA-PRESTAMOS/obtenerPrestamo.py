import boto3
import json
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Inicializar DynamoDB
dynamodb = boto3.resource('dynamodb')
prestamos_table = dynamodb.Table('TABLA-PRESTAMOS')

# Función auxiliar para convertir Decimal a tipos JSON serializables
def decimal_to_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 else int(obj)
    elif isinstance(obj, list):
        return [decimal_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: decimal_to_serializable(value) for key, value in obj.items()}
    return obj

def lambda_handler(event, context):
    try:
        # Validar el cuerpo de la solicitud
        data = json.loads(event['body'])
        usuario_id = data.get('usuario_id')
        prestamo_id = data.get('prestamo_id')

        if not usuario_id or not prestamo_id:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'El usuario_id y el prestamo_id son obligatorios'
                }
            }

        # Obtener el préstamo de DynamoDB
        response = prestamos_table.get_item(Key={'usuario_id': usuario_id, 'prestamo_id': prestamo_id})

        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': {'error': 'Préstamo no encontrado'}
            }

        # Convertir el préstamo a tipos serializables
        prestamo = decimal_to_serializable(response['Item'])

        return {
            'statusCode': 200,
            'body': {
                'message': 'Préstamo encontrado',
                'prestamo': prestamo
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': {'error': 'Error interno del servidor', 'details': str(e)}
        }
