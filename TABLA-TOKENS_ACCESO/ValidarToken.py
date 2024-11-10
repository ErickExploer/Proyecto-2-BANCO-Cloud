import boto3
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-TOKENS_ACCESO')
    token = event['token']
    response = table.get_item(Key={'token': token})

    if 'Item' not in response:
        return {'statusCode': 403, 'body': 'Token no existe'}

    expires = response['Item']['expires']
    if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > expires:
        return {'statusCode': 403, 'body': 'Token expirado'}

    return {'statusCode': 200, 'body': 'Token válido'}
