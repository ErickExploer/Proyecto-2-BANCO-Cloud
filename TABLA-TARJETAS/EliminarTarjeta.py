import boto3
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
    
    cuenta_id = event['pathParameters']['cuenta_id']
    tarjeta_id = event['pathParameters']['tarjeta_id']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-TARJETAS')
    table.delete_item(
        Key={
            'cuenta_id': cuenta_id,
            'tarjeta_id': tarjeta_id
        }
    )
    
    return {
        'statusCode': 200,
        'body': 'Tarjeta eliminada exitosamente'
    }
