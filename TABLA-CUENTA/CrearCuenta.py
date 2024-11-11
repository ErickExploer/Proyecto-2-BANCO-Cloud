import boto3
import json
from decimal import Decimal

def lambda_handler(event, context):
    body = event.get('body')
    if isinstance(body, str):
        body = json.loads(body)

    usuario_id = body['usuario_id']
    cuenta_datos = body['cuenta_datos']

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
    cuenta_numero = cuentas_response['Count'] + 1
    cuenta_id = f"CUENTA-{cuenta_numero}"

    cuentas_table.put_item(
        Item={
            'usuario_id': usuario_id,
            'cuenta_id': cuenta_id,
            'saldo': Decimal(str(cuenta_datos['saldo'])),
            'nombre_cuenta': cuenta_datos['nombre_cuenta'],
            'interes': Decimal(str(cuenta_datos['interes']))
        }
    )

    return {
        'statusCode': 200,
        'body': f'Cuenta creada exitosamente con ID: {cuenta_id}'
    }
