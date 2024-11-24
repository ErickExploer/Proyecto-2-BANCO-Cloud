import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

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
        estado = data.get('estado')

        # Validar que el estado esté presente
        if not estado or estado not in ['aceptado', 'rechazado']:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'El estado debe ser "aceptado" o "rechazado"'
                }
            }

        # Escanear solicitudes según el estado
        response = solicitud_table.scan(
            FilterExpression=Attr('estado').eq(estado)
        )

        # Convertir los resultados a tipos serializables
        solicitudes = decimal_to_serializable(response.get('Items', []))

        return {
            'statusCode': 200,
            'body': {
                'message': f'Solicitudes con estado {estado} encontradas',
                'estado': estado,
                'solicitudes': solicitudes
            }
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno al procesar la solicitud',
                'details': str(e)
            }
        }
