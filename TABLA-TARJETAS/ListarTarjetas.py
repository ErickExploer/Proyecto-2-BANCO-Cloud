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
    
    cuenta_id = event['cuenta_id']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-TARJETAS')
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('cuenta_id').eq(cuenta_id)
    )
    items = response['Items']
    
    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
