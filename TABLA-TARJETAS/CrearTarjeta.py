import boto3
import uuid
from datetime import datetime

def validate_token(token):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-TOKENS_ACCESO')
    response = table.get_item(Key={'token': token})
    if 'Item' not in response:
        return False
    expires = response['Item']['expires']
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return now <= expires

def lambda_handler(event, context):
    token = event['headers'].get('Authorization')
    if not validate_token(token):
        return {'statusCode': 403, 'body': 'Acceso No Autorizado'}
    
    cuenta_id = event['cuenta_id']
    tarjeta_id = str(uuid.uuid4())
    data = event['body']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-TARJETAS')
    table.put_item(
        Item={
            'cuenta_id': cuenta_id,
            'tarjeta_id': tarjeta_id,
            'limite': data['limite'],
            'saldo_disponible': data['saldo_disponible'],
            'estado': data['estado'],
            'fecha_emision': data['fecha_emision'],
            'fecha_vencimiento': data['fecha_vencimiento'],
            'cvv': data['cvv']
        }
    )
    
    return {
        'statusCode': 200,
        'body': f'Tarjeta creada exitosamente con ID: {tarjeta_id}'
    }
