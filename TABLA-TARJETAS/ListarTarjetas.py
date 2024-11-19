import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

def decimal_to_serializable(obj):
    """
    Convierte objetos Decimal a tipos JSON serializables.
    """
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 else int(obj)
    elif isinstance(obj, list):
        return [decimal_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: decimal_to_serializable(value) for key, value in obj.items()}
    return obj

def lambda_handler(event, context):
    try:
        # Parsear el cuerpo de la solicitud
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

        usuario_id = body.get('usuario_id')
        cuenta_id = body.get('cuenta_id')

        if not usuario_id or not cuenta_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'El usuario_id y cuenta_id son obligatorios'
                })
            }

        # Inicializar DynamoDB
        dynamodb = boto3.resource('dynamodb')
        cuentas_table = dynamodb.Table('TABLA-CUENTA')
        tarjetas_table = dynamodb.Table('TABLA-TARJETAS')

        # Validar que la cuenta exista para el usuario
        cuenta_response = cuentas_table.get_item(Key={'usuario_id': usuario_id, 'cuenta_id': cuenta_id})
        if 'Item' not in cuenta_response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Cuenta no encontrada',
                    'details': f'No se encontró la cuenta con usuario_id {usuario_id} y cuenta_id {cuenta_id}'
                })
            }

        # Consultar tarjetas relacionadas con la cuenta y usuario
        response = tarjetas_table.query(
            KeyConditionExpression=Key('cuenta_id').eq(cuenta_id),
            FilterExpression=Attr('usuario_id').eq(usuario_id)
        )

        tarjetas = response.get('Items', [])

        # Convertir resultados a tipos JSON serializables
        tarjetas_serializables = decimal_to_serializable(tarjetas)

        return {
            'statusCode': 200,
            'body': {
                'message': 'Tarjetas encontradas',
                'usuario_id': usuario_id,
                'cuenta_id': cuenta_id,
                'tarjetas': tarjetas_serializables
            }
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Error interno del servidor', 'details': str(e)})
        }
