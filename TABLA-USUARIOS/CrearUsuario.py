import boto3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-USUARIOS')
    
    usuario_id = event['usuario_id']
    password = event['password']
    hashed_password = hash_password(password)
    
    response = table.put_item(
        Item={
            'usuario_id': usuario_id,
            'nombre': event['nombre'],
            'apellido': event['apellido'],
            'email': event['email'],
            'telefono': event['telefono'],
            'dni': event['dni'],
            'direccion': event['direccion'],
            'fecha_nac': event['fecha_nac'],
            'password': hashed_password
        }
    )
    
    return {
        'statusCode': 200,
        'body': 'Usuario creado exitosamente'
    }
