import boto3

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    pago_id = data['pago_id']
    estado = data.get('estado', 'pendiente')

    try:
        pagos_table.update_item(
            Key={'usuario_id': usuario_id, 'pago_id': pago_id},
            UpdateExpression="SET estado = :estado",
            ExpressionAttributeValues={':estado': estado}
        )
        
        return {
            'statusCode': 200,
            'body': f'Pago {pago_id} actualizado con estado {estado}'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al actualizar el pago: {str(e)}'
        }