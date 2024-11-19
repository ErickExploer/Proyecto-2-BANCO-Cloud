import boto3
import json
from decimal import Decimal
from datetime import datetime
import os

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')
tarjetas_table = dynamodb.Table('TABLA-TARJETAS')

def lambda_handler(event, context):
    try:
        # Validar que el cuerpo de la solicitud esté presente
        if 'body' not in event or not event['body']:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud'
                })
            }

        # Decodificar y validar el cuerpo JSON
        data = json.loads(event['body'])
        required_fields = ['usuario_id', 'cuenta_id', 'tarjeta_id', 'pago_id']
        for field in required_fields:
            if field not in data:
                return {
                    'statusCode': 400,
                    'body': json.dumps({
                        'error': 'Solicitud inválida',
                        'details': f'El campo {field} es obligatorio'
                    })
                }

        usuario_id = data['usuario_id']
        cuenta_id = data['cuenta_id']
        tarjeta_id = data['tarjeta_id']
        pago_id = data['pago_id']

        # Verificar si el pago existe
        pago_response = pagos_table.get_item(Key={'usuario_id': usuario_id, 'pago_id': pago_id})
        if 'Item' not in pago_response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Pago no encontrado',
                    'details': f'El pago con ID {pago_id} no existe para el usuario {usuario_id}'
                })
            }

        pago = pago_response['Item']
        if pago['estado'] == 'pagado':
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'El pago ya está realizado',
                    'details': f'El pago con ID {pago_id} ya tiene estado "pagado"'
                })
            }

        # Verificar si la tarjeta existe
        tarjeta_response = tarjetas_table.get_item(Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id})
        if 'Item' not in tarjeta_response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Tarjeta no encontrada',
                    'details': f'La tarjeta con ID {tarjeta_id} no existe para la cuenta {cuenta_id}'
                })
            }

        tarjeta = tarjeta_response['Item']
        saldo_anterior = tarjeta['saldo_disponible']
        monto_pagado = Decimal(pago['monto'])

        if saldo_anterior < monto_pagado:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Saldo insuficiente',
                    'details': f'El saldo disponible ({saldo_anterior}) es menor que el monto del pago ({monto_pagado})'
                })
            }

        # Actualizar saldo de la tarjeta
        nuevo_saldo = saldo_anterior - monto_pagado
        tarjetas_table.update_item(
            Key={'cuenta_id': cuenta_id, 'tarjeta_id': tarjeta_id},
            UpdateExpression='SET saldo_disponible = :nuevo_saldo',
            ExpressionAttributeValues={':nuevo_saldo': Decimal(nuevo_saldo)}
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

        # Retornar la información detallada del pago y saldo
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Pago realizado con éxito',
                'usuario_id': usuario_id,
                'pago_id': pago_id,
                'tarjeta_id': tarjeta_id,
                'estado': 'pagado',
                'monto_pagado': float(monto_pagado),
                'saldo_antes_del_pago': float(saldo_anterior),
                'saldo_actual': float(nuevo_saldo),
                'fecha': fecha_actualizacion
            })
        }

    except Exception as e:
        # Manejo de errores internos
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error interno del servidor',
                'details': str(e)
            })
        }
