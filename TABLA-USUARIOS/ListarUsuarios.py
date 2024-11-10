import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-USUARIOS')
    
    usuario_id = event.get('usuario_id')
    
    if usuario_id:
        response = table.query(
            KeyConditionExpression=Key('usuario_id').eq(usuario_id)
        )
    else:
        response = table.scan()
    
    return {
        'statusCode': 200,
        'body': response['Items']
    }
