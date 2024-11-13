import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    data = json.loads(event['body'])
    cuenta_origen = data['cuenta_origen']
    
    transaccion_table = dynamodb.Table('TablaTransacciones')
    
    try:
        response = transaccion_table.query(
            KeyConditionExpression=Key('cuenta_origen').eq(cuenta_origen)
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Items', []))
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al listar transacciones: {str(e)}'})
        }