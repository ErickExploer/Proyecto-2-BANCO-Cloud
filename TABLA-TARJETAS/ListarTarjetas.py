import boto3
import json

def lambda_handler(event, context):
    if isinstance(event['body'], str):
        body = json.loads(event['body'])
    else:
        body = event['body']

    usuario_id = body.get('usuario_id')
    cuenta_id = body.get('cuenta_id')

    dynamodb = boto3.resource('dynamodb')
    cuentas_table = dynamodb.Table('TABLA-CUENTA')
    tarjetas_table = dynamodb.Table('TABLA-TARJETAS')

    cuenta_response = cuentas_table.get_item(Key={'usuario_id': usuario_id, 'cuenta_id': cuenta_id})
    if 'Item' not in cuenta_response:
        return {
            'statusCode': 400,
            'body': 'Error: Cuenta no encontrada para este usuario.'
        }

    response = tarjetas_table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('cuenta_id').eq(cuenta_id)
    )

    return {
        'statusCode': 200,
        'body': response['Items']
    }
