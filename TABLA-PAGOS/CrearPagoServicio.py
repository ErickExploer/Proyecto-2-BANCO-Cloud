import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

def lambda_handler(event, context):
    data = event['body']
    usuario_id = data['usuario_id']
    pago_id = str(uuid.uuid4())
    monto = data['datos_pago']['monto']
    titulo = data['datos_pago']['titulo']
    descripcion = data['datos_pago']['descripcion']

    item = {
        'usuario_id': usuario_id,
        'pago_id': pago_id,
        'titulo': titulo,
        'descripcion': descripcion,
        'tipo': 'servicio',
        'monto': monto,
        'estado': 'pendiente',
        'fecha': datetime.utcnow().isoformat()
    }

    pagos_table.put_item(Item=item)
    
    return {
        'statusCode': 200,
        'body': item
    }