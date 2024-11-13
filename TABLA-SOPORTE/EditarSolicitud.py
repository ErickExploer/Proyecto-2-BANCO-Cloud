import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLA-SOPORTE')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    ticket_id = data['ticket_id']
    titulo = data['Titulo']
    descripcion = data['descripcion']
    
    response = table.get_item(Key={'usuario_id': usuario_id, 'ticket_id': ticket_id})
    
    if response.get('Item', {}).get('estado') == 'respondido':
        return {
            'statusCode': 400,
            'body': 'La solicitud ya fue respondida y no puede ser modificada.'
        }

    table.update_item(
        Key={'usuario_id': usuario_id, 'ticket_id': ticket_id},
        UpdateExpression="SET Titulo = :titulo, descripcion = :descripcion",
        ExpressionAttributeValues={
            ':titulo': titulo,
            ':descripcion': descripcion
        }
    )
    
    return {
        'statusCode': 200,
        'body': {
            'momento': 'actual modificado',
            'usuario_id': usuario_id,
            'ticket_id': ticket_id,
            'Titulo': titulo,
            'descripcion': descripcion,
            'estado': 'pendiente'
        }
    }