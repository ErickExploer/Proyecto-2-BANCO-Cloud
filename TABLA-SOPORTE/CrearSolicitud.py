import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLA-SOPORTE')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    titulo = data['Titulo']
    descripcion = data['descripcion']
    
    ticket_id = str(uuid.uuid4())
    fecha = datetime.utcnow().isoformat()
    
    item = {
        'usuario_id': usuario_id,
        'ticket_id': ticket_id,
        'Titulo': titulo,
        'descripcion': descripcion,
        'estado': 'pendiente',
        'fecha': fecha
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': item
    }