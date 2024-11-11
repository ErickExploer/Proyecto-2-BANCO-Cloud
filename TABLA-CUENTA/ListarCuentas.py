import boto3
import json
from decimal import Decimal

def decimal_to_float(item):
    for key, value in item.items():
        if isinstance(value, Decimal):
            item[key] = float(value)
    return item

def lambda_handler(event, context):
    body = event.get('body')
    if isinstance(body, str):
        body = json.loads(body)

    usuario_id = body.get('usuario_id')

    dynamodb = boto3.resource('dynamodb')
    usuarios_table = dynamodb.Table('TABLA-USUARIOS')
    cuentas_table = dynamodb.Table('TABLA-CUENTA')

    response = usuarios_table.get_item(Key={'usuario_id': usuario_id})
    if 'Item' not in response:
        return {
            'statusCode': 400,
            'body': 'Usuario no existe'
        }

    cuentas_response = cuentas_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('usuario_id').eq(usuario_id)
    )
    cuentas = cuentas_response.get('Items', [])

    cuentas = [decimal_to_float(cuenta) for cuenta in cuentas]

    return {
        'statusCode': 200,
        'body': cuentas
    }
