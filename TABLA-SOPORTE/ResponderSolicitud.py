import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLA-SOPORTE')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    ticket_id = data['ticket_id']
    response_text = data['response']

    response = table.get_item(Key={'usuario_id': usuario_id, 'ticket_id': ticket_id})
    
    if response.get('Item', {}).get('estado') == 'respondido':
        return {
            'statusCode': 400,
            'body': 'La solicitud ya fue respondida.'
        }
    
    fecha_respuesta = datetime.utcnow().isoformat()
    table.update_item(
        Key={'usuario_id': usuario_id, 'ticket_id': ticket_id},
        UpdateExpression="SET response = :response, estado = :estado, fecha_respuesta = :fecha",
        ExpressionAttributeValues={
            ':response': response_text,
            ':estado': 'respondido',
            ':fecha': fecha_respuesta
        }
    )
    
    return {
        'statusCode': 200,
        'body': {
            'usuario_id': usuario_id,
            'ticket_id': ticket_id,
            'response': response_text,
            'estado': 'respondido',
            'fecha_respuesta': fecha_respuesta
        }
    }