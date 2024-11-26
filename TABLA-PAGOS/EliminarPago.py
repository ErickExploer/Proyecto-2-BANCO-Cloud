import boto3

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    pago_id = data['pago_id']

    try:
        pagos_table.delete_item(Key={'usuario_id': usuario_id, 'pago_id': pago_id})
        
        return {
            'statusCode': 200,
            'body': f'Pago {pago_id} eliminado exitosamente'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al eliminar el pago: {str(e)}'
        }
