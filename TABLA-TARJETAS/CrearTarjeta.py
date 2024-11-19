import boto3
import json
from datetime import datetime
from decimal import Decimal
import random

def generate_card_number():
    """Genera un número de tarjeta de 16 dígitos en formato xxxx-xxxx-xxxx-xxxx"""
    return '-'.join([''.join([str(random.randint(0, 9)) for _ in range(4)]) for _ in range(4)])

def lambda_handler(event, context):
    try:
        # Parsear el cuerpo de la solicitud
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        else:
            body = event['body']

        # Validar campos requeridos
        usuario_id = body.get('usuario_id')
        cuenta_id = body.get('cuenta_id')
        if not usuario_id or not cuenta_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'Se requieren los campos usuario_id y cuenta_id.'
                })
            }

        # Inicializar recursos de DynamoDB
        dynamodb = boto3.resource('dynamodb')
        usuarios_table = dynamodb.Table('TABLA-USUARIOS')
        cuentas_table = dynamodb.Table('TABLA-CUENTA')
        tarjetas_table = dynamodb.Table('TABLA-TARJETAS')

        # Verificar si el usuario existe
        user_response = usuarios_table.get_item(Key={'usuario_id': usuario_id})
        if 'Item' not in user_response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Usuario no encontrado',
                    'details': f'El usuario con ID {usuario_id} no existe.'
                })
            }

        # Verificar si la cuenta pertenece al usuario
        cuenta_response = cuentas_table.get_item(Key={'usuario_id': usuario_id, 'cuenta_id': cuenta_id})
        if 'Item' not in cuenta_response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Cuenta no encontrada',
                    'details': f'La cuenta con ID {cuenta_id} no pertenece al usuario {usuario_id}.'
                })
            }

        # Generar un número único de tarjeta
        tarjeta_id = generate_card_number()
        while True:
            existing_card = tarjetas_table.query(
                IndexName='tarjeta_id-index',
                KeyConditionExpression=boto3.dynamodb.conditions.Key('tarjeta_id').eq(tarjeta_id)
            )
            if existing_card['Count'] == 0:
                break
            tarjeta_id = generate_card_number()

        # Crear la nueva tarjeta
        tarjeta_item = {
            'usuario_id': usuario_id,
            'cuenta_id': cuenta_id,
            'tarjeta_id': tarjeta_id,
            'saldo_disponible': Decimal('0.00'),
            'estado': 'activa',
            'fecha_emision': datetime.now().strftime('%Y-%m-%d'),
            'fecha_vencimiento': (datetime.now().replace(year=datetime.now().year + 3)).strftime('%Y-%m-%d'),
            'cvv': str(datetime.now().microsecond % 1000).zfill(3)
        }

        tarjetas_table.put_item(Item=tarjeta_item)

        # Retornar detalles completos de la tarjeta creada
        return {
            'statusCode': 200,
            'body': {
                'mensaje': 'Tarjeta creada exitosamente',
                'usuario_id': usuario_id,
                'cuenta_id': cuenta_id,
                'tarjeta': {
                    'tarjeta_id': tarjeta_id,
                    'saldo_disponible': float(tarjeta_item['saldo_disponible']),
                    'estado': tarjeta_item['estado'],
                    'fecha_emision': tarjeta_item['fecha_emision'],
                    'fecha_vencimiento': tarjeta_item['fecha_vencimiento'],
                    'cvv': tarjeta_item['cvv']
                }
            }
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
