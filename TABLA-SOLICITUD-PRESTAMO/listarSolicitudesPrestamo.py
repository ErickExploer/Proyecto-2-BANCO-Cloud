import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

# Conexión con DynamoDB
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
        # Asegurarnos de que el cuerpo está presente y no vacío
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud'
                }
            }

        # Parseo manual del cuerpo sin usar json.loads
        body = event['body']
        if isinstance(body, str):
            try:
                data = eval(body) if body.startswith("{") else None
            except Exception:
                return {
                    'statusCode': 400,
                    'body': {
                        'error': 'Solicitud inválida',
                        'details': 'El cuerpo de la solicitud no es válido'
                    }
                }
        elif isinstance(body, dict):
            data = body
        else:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'Formato del cuerpo no reconocido'
                }
            }

        # Validar el usuario_id
        usuario_id = data.get('usuario_id')
        if not usuario_id:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'El campo usuario_id es obligatorio'
                }
            }

        # Consultar DynamoDB para obtener las solicitudes
        response = solicitud_table.query(
            KeyConditionExpression=Key('usuario_id').eq(usuario_id)
        )

        items = response.get('Items', [])

        # Si no hay resultados
        if not items:
            return {
                'statusCode': 404,
                'body': {
                    'error': 'No se encontraron solicitudes',
                    'details': f'No hay solicitudes registradas para el usuario_id: {usuario_id}'
                }
            }

        # Convertir el resultado en un formato serializable
        solicitudes = decimal_to_serializable(items)

        return {
            'statusCode': 200,
            'body': {
                'message': 'Solicitudes obtenidas exitosamente',
                'data': solicitudes
            }
        }
    except Exception as e:
        # Manejo de errores internos
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno al listar las solicitudes',
                'details': str(e)
            }
        }
