import boto3
from validate_token import validate_token

def lambda_handler(event, context):

    token = event['headers'].get('Authorization')
    if not validate_token(token):
        return {'statusCode': 403, 'body': 'Acceso No Autorizado'}
    
    usuario_id = event['pathParameters']['usuario_id']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-USUARIOS')
    response = table.delete_item(
        Key={
            'usuario_id': usuario_id
        }
    )
    
    return {
        'statusCode': 200,
        'body': f'Usuario {usuario_id} eliminado exitosamente'
    }
