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
    
    body = json.loads(event['body'])
    usuario_id = body.get('usuario_id')
    cuenta_id = body.get('cuenta_id')
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-CUENTA')
    response = table.get_item(
        Key={
            'usuario_id': usuario_id,
            'cuenta_id': cuenta_id
        }
    )
    
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': 'Cuenta no encontrada'
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response['Item'])
    }
