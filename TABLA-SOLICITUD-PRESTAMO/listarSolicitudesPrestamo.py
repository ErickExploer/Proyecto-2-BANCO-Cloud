import boto3
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key  # Asegúrate de importar Key

# Conexión con DynamoDB
dynamodb = boto3.resource('dynamodb')
solicitud_table = dynamodb.Table('TABLA-SOLICITUD-PRESTAMO')

# Función auxiliar para convertir Decimal a tipos JSON serializables
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
        # Parsear el cuerpo de la solicitud
        data = json.loads(event['body'])
        usuario_id = data.get('usuario_id')

        if not usuario_id:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'El campo usuario_id es obligatorio'
                }
            }

        # Consulta a DynamoDB para obtener solicitudes por usuario_id
        response = solicitud_table.query(
            KeyConditionExpression=Key('usuario_id').eq(usuario_id)
        )

        # Convertir el resultado a un formato JSON serializable
        items = decimal_to_serializable(response.get('Items', []))

        return {
            'statusCode': 200,
            'body': items  # Serializar los resultados a JSON
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error al listar las solicitudes de préstamo',
                'details': str(e)
            }
        }
