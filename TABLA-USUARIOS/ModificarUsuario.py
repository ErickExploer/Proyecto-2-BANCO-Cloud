import boto3
import json
from validate_token import validate_token

def lambda_handler(event, context):
    token = event['headers'].get('Authorization')
    if not validate_token(token):
        return {'statusCode': 403, 'body': 'Acceso No Autorizado'}
    

    usuario_id = event['pathParameters']['usuario_id']
    updated_data = json.loads(event['body'])
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-USUARIOS')
    response = table.update_item(
        Key={'usuario_id': usuario_id},
        UpdateExpression="set nombre=:n, apellido=:a, email=:e, telefono=:t, dni=:d, direccion=:dir, fecha_nac=:fn",
        ExpressionAttributeValues={
            ':n': updated_data['nombre'],
            ':a': updated_data['apellido'],
            ':e': updated_data['email'],
            ':t': updated_data['telefono'],
            ':d': updated_data['dni'],
            ':dir': updated_data['direccion'],
            ':fn': updated_data['fecha_nac']
        },
        ReturnValues="UPDATED_NEW"
    )
    
    return {
        'statusCode': 200,
        'body': 'Usuario modificado exitosamente'
    }
