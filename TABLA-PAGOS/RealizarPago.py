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

    # Obtener el pago
    pago_response = pagos_table.get_item(Key={'usuario_id': usuario_id, 'pago_id': pago_id})
    if 'Item' not in pago_response:
        return {'statusCode': 404, 'body': 'Pago no encontrado'}
    
    pago = pago_response['Item']
    if pago['estado'] == 'pagado':
        return {'statusCode': 400, 'body': 'El pago ya está realizado'}

    # Obtener tarjeta y verificar saldo
    tarjeta_response = tarjetas_table.get_item(Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id})
    if 'Item' not in tarjeta_response:
        return {'statusCode': 404, 'body': 'Tarjeta no encontrada'}
    
    tarjeta = tarjeta_response['Item']
    saldo_anterior = tarjeta['tarjeta_datos']['saldo']
    monto_pagado = pago['monto']
    
    if saldo_anterior < monto_pagado:
        return {'statusCode': 400, 'body': 'Saldo insuficiente en la tarjeta'}
    
    # Realizar el pago
    nuevo_saldo = saldo_anterior - monto_pagado
    tarjetas_table.update_item(
        Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id},
        UpdateExpression='SET tarjeta_datos.saldo = :new_saldo',
        ExpressionAttributeValues={':new_saldo': nuevo_saldo}
    )
    
    # Actualizar estado del pago
    fecha_actualizacion = datetime.utcnow().isoformat()
    pagos_table.update_item(
        Key={'usuario_id': usuario_id, 'pago_id': pago_id},
        UpdateExpression='SET estado = :estado, fecha = :fecha',
        ExpressionAttributeValues={
            ':estado': 'pagado',
            ':fecha': fecha_actualizacion
        }
    )
    
    # Respuesta con los detalles del pago
    return {
        'statusCode': 200,
        'body': {
            'mensaje': 'Pago realizado con éxito',
            'usuario_id': usuario_id,
            'pago_id': pago_id,
            'tarjeta_id': tarjeta_id,
            'estado': 'pagado',
            'monto_pagado': float(monto_pagado),
            'saldo_antes_del_pago': float(saldo_anterior),
            'saldo_actual': float(nuevo_saldo),
            'fecha': fecha_actualizacion
        }
    }
