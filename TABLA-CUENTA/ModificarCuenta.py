import boto3
import json
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
    
    usuario_id = event['pathParameters']['usuario_id']
    cuenta_id = event['pathParameters']['cuenta_id']
    
    updated_data = json.loads(event['body'])
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-CUENTA')
    response = table.update_item(
        Key={
            'usuario_id': usuario_id,
            'cuenta_id': cuenta_id
        },
        UpdateExpression="set saldo=:s, nombre_cuenta=:n, interes=:i",
        ExpressionAttributeValues={
            ':s': updated_data['saldo'],
            ':n': updated_data['nombre_cuenta'],
            ':i': updated_data.get('interes', 0.0)
        },
        ReturnValues="UPDATED_NEW"
    )
    
    return {
        'statusCode': 200,
        'body': f'Cuenta {cuenta_id} modificada exitosamente'
    }
