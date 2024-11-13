import boto3

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']

    try:
        response = pagos_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('usuario_id').eq(usuario_id)
        )
        return {
            'statusCode': 200,
            'body': response.get('Items', [])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al listar los pagos: {str(e)}'
        }