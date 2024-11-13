import boto3
import json
from decimal import Decimal

def lambda_handler(event, context):
    if isinstance(event['body'], str):
        body = json.loads(event['body'])
    else:
        body = event['body']

    usuario_id = body.get('usuario_id')
    cuenta_id = body.get('cuenta_id')
    tarjeta_id = body.get('tarjeta_id')
    monto = Decimal(str(body.get('monto', 0)))

    dynamodb = boto3.resource('dynamodb')
    cuentas_table = dynamodb.Table('TABLA-CUENTA')
    tarjetas_table = dynamodb.Table('TABLA-TARJETAS')

    cuenta_response = cuentas_table.get_item(Key={'usuario_id': usuario_id, 'cuenta_id': cuenta_id})
    if 'Item' not in cuenta_response:
        return {
            'statusCode': 400,
            'body': 'Error: Cuenta no encontrada para este usuario.'
        }

    cuenta_saldo = Decimal(str(cuenta_response['Item']['saldo']))
    if cuenta_saldo < monto:
        return {
            'statusCode': 400,
            'body': 'Error: Saldo insuficiente en la cuenta para realizar la recarga.'
        }

    tarjeta_response = tarjetas_table.get_item(Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id})
    if 'Item' not in tarjeta_response:
        return {
            'statusCode': 404,
            'body': 'Error: Tarjeta no encontrada.'
        }

    estado = tarjeta_response['Item'].get('estado', 'activa')
    if estado == 'bloqueada':
        return {
            'statusCode': 400,
            'body': 'Error: No se puede recargar una tarjeta que está bloqueada.'
        }

    nuevo_saldo_cuenta = cuenta_saldo - monto
    cuentas_table.update_item(
        Key={'usuario_id': usuario_id, 'cuenta_id': cuenta_id},
        UpdateExpression="SET saldo = :nuevo_saldo",
        ExpressionAttributeValues={':nuevo_saldo': nuevo_saldo_cuenta}
    )

    saldo_disponible = Decimal(str(tarjeta_response['Item']['saldo_disponible']))
    nuevo_saldo_disponible = saldo_disponible + monto
    tarjetas_table.update_item(
        Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id},
        UpdateExpression="SET saldo_disponible = :nuevo_saldo_disponible",
        ExpressionAttributeValues={':nuevo_saldo_disponible': nuevo_saldo_disponible}
    )

    return {
        'statusCode': 200,
        'body': f'Tarjeta {tarjeta_id} recargada exitosamente. Nuevo saldo disponible: {nuevo_saldo_disponible}'
    }
