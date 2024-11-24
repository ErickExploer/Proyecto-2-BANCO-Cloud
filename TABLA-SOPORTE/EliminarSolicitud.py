import boto3
import json

# Conexión a DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLA-SOPORTE')

def lambda_handler(event, context):
    try:
        # Parsear el cuerpo de la solicitud
        if isinstance(event['body'], str):
            data = json.loads(event['body'])
        else:
            data = event['body']

        # Validar los campos obligatorios
        usuario_id = data.get('usuario_id')
        ticket_id = data.get('ticket_id')

        if not usuario_id or not ticket_id:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'usuario_id y ticket_id son obligatorios'
                }
            }

        # Verificar si la solicitud existe
        response = table.get_item(Key={'usuario_id': usuario_id, 'ticket_id': ticket_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': {
                    'error': 'Solicitud no encontrada',
                    'details': f'No se encontró una solicitud con usuario_id {usuario_id} y ticket_id {ticket_id}'
                }
            }

        # Eliminar la solicitud
        table.delete_item(Key={'usuario_id': usuario_id, 'ticket_id': ticket_id})

        # Responder con éxito
        return {
            'statusCode': 200,
            'body': {
                'message': f'Solicitud {ticket_id} del usuario {usuario_id} se eliminó correctamente'
            }
        }

    except Exception as e:
        # Manejo de errores
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno del servidor',
                'details': str(e)
            }
        }
