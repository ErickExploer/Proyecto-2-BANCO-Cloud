import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLA-SOPORTE')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    ticket_id = data['ticket_id']
    
    response = table.get_item(Key={'usuario_id': usuario_id, 'ticket_id': ticket_id})
    
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': response['Item']
        }
    else:
        return {
            'statusCode': 404,
            'body': 'Solicitud no encontrada'
        }