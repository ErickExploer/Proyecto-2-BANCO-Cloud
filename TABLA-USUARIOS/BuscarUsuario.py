import boto3
import json

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-USUARIOS')

    if 'body' in event:
        if isinstance(event['body'], str):
            try:
                body = json.loads(event['body'])
            except json.JSONDecodeError:
                return {
                    'statusCode': 400,
                    'body': 'Solicitud inválida. Formato JSON incorrecto.'
                }
        else:
            body = event['body']
    else:
        body = event

    usuario_id = body.get('usuario_id')

    if not usuario_id:
        return {
            'statusCode': 400,
            'body': 'Solicitud inválida. Falta el campo usuario_id.'
        }

    response = table.get_item(Key={'usuario_id': usuario_id})
    
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': 'Usuario no encontrado'
        }
    
    return {
        'statusCode': 200,
        'body': response['Item']
    }
