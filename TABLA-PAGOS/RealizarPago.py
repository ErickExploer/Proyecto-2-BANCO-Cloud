import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')
tarjetas_table = dynamodb.Table('TABLA-TARJETAS')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    cuenta_id = data['cuenta_id']
    tarjeta_id = data['tarjeta_id']
    pago_id = data['pago_id']

    pago_response = pagos_table.get_item(Key={'usuario_id': usuario_id, 'pago_id': pago_id})
    if 'Item' not in pago_response:
        return {'statusCode': 404, 'body': 'Pago no encontrado'}
    
    pago = pago_response['Item']
    if pago['estado'] == 'pagado':
        return {'statusCode': 400, 'body': 'El pago ya está realizado'}

    tarjeta_response = tarjetas_table.get_item(Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id})
    if 'Item' not in tarjeta_response:
        return {'statusCode': 404, 'body': 'Tarjeta no encontrada'}
    
    tarjeta = tarjeta_response['Item']
    if tarjeta['tarjeta_datos']['saldo'] < pago['monto']:
        return {'statusCode': 400, 'body': 'Saldo insuficiente en la tarjeta'}

    new_saldo = tarjeta['tarjeta_datos']['saldo'] - pago['monto']
    tarjetas_table.update_item(
        Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id},
        UpdateExpression='SET tarjeta_datos.saldo = :new_saldo',
        ExpressionAttributeValues={':new_saldo': new_saldo}
    )
    
    pagos_table.update_item(
        Key={'usuario_id': usuario_id, 'pago_id': pago_id},
        UpdateExpression='SET estado = :estado, fecha = :fecha',
        ExpressionAttributeValues={
            ':estado': 'pagado',
            ':fecha': datetime.utcnow().isoformat()
        }
    )
    
    return {
        'statusCode': 200,
        'body': {
            'usuario_id': usuario_id,
            'pago_id': pago_id,
            'estado': 'pagado',
            'fecha': datetime.utcnow().isoformat()
        }
    }