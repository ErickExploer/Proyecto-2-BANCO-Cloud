import boto3
import hashlib
import uuid
from datetime import datetime, timedelta

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    # Obtener usuario y contraseña de la entrada
    usuario_id = event['usuario_id']
    password = event['password']
    hashed_password = hash_password(password)
    
    # Conexión a DynamoDB
    dynamodb = boto3.resource('dynamodb')
    usuarios_table = dynamodb.Table('usuarios')
    
    # Validar usuario
    response = usuarios_table.get_item(Key={'usuario_id': usuario_id})
    if 'Item' not in response:
        return {'statusCode': 403, 'body': 'Usuario no existe'}
    
    # Validar contraseña
    if hashed_password != response['Item']['password']:
        return {'statusCode': 403, 'body': 'Contraseña incorrecta'}
    
    # Generar token
    token = str(uuid.uuid4())
    expires = (datetime.now() + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')
    
    # Guardar token en la tabla de TOKENS_ACCESO
    tokens_table = dynamodb.Table('tokens_acceso')
    tokens_table.put_item(
        Item={
            'token': token,
            'expires': expires
        }
    )
    
    return {
        'statusCode': 200,
        'token': token,
        'expires': expires
    }
