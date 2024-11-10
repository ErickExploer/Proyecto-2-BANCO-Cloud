import boto3
from datetime import datetime
import json

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
    updated_data = json.loads(event['body'])
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-TARJETAS')
    response = table.update_item(
        Key={
            'cuenta_id': cuenta_id,
            'tarjeta_id': tarjeta_id
        },
        UpdateExpression="set limite=:l, saldo_disponible=:sd, estado=:e, fecha_emision=:fe, fecha_vencimiento=:fv, cvv=:cv",
        ExpressionAttributeValues={
            ':l': updated_data['limite'],
            ':sd': updated_data['saldo_disponible'],
            ':e': updated_data['estado'],
            ':fe': updated_data['fecha_emision'],
            ':fv': updated_data['fecha_vencimiento'],
            ':cv': updated_data['cvv']
        },
        ReturnValues="UPDATED_NEW"
    )
    
    return {
        'statusCode': 200,
        'body': 'Tarjeta modificada exitosamente'
    }
