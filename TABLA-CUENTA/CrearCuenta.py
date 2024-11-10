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
    
    usuario_id = event['usuario_id']
    cuenta_id = str(uuid.uuid4())
    saldo = event['saldo']
    nombre_cuenta = event['nombre_cuenta']
    interes = event.get('interes', 0.0)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-CUENTA')
    table.put_item(
        Item={
            'usuario_id': usuario_id,
            'cuenta_id': cuenta_id,
            'saldo': saldo,
            'nombre_cuenta': nombre_cuenta,
            'interes': interes
        }
    )
    
    return {
        'statusCode': 200,
        'body': f'Cuenta creada exitosamente con ID: {cuenta_id}'
    }
