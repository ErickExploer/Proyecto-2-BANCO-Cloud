import boto3

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    pago_id = data['pago_id']

    try:
        response = pagos_table.get_item(Key={'usuario_id': usuario_id, 'pago_id': pago_id})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': response['Item']
            }
        else:
            return {
                'statusCode': 404,
                'body': 'Pago no encontrado'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al obtener el pago: {str(e)}'
        }
