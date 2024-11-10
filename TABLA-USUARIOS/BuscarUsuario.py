import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-USUARIOS')
    
    usuario_id = event['usuario_id']
    response = table.get_item(Key={'usuario_id': usuario_id})
    
    if 'Item' not in response:
        return {'statusCode': 404, 'body': 'Usuario no encontrado'}
    
    return {
        'statusCode': 200,
        'body': response['Item']
    }
