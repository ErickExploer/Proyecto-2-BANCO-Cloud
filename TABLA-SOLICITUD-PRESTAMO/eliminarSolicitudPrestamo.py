import boto3
import json

# Conexión a DynamoDB
dynamodb = boto3.resource('dynamodb')
solicitud_table = dynamodb.Table('TABLA-SOLICITUD-PRESTAMO')

def lambda_handler(event, context):
    try:
        # Validar el cuerpo de la solicitud
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud'
                }
            }

        # Parsear el cuerpo de la solicitud
        data = json.loads(event['body'])
        usuario_id = data.get('usuario_id')
        solicitud_id = data.get('solicitud_id')

        print(f"Datos recibidos: usuario_id={usuario_id}, solicitud_id={solicitud_id}")

        # Validar que los campos requeridos estén presentes
        if not usuario_id or not solicitud_id:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'El usuario_id y el solicitud_id son obligatorios'
                }
            }

        # Verificar si la solicitud existe
        response = solicitud_table.get_item(Key={'usuario_id': usuario_id, 'solicitud_id': solicitud_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': {
                    'error': 'Solicitud no encontrada',
                    'details': f'No se encontró la solicitud con usuario_id {usuario_id} y solicitud_id {solicitud_id}'
                }
            }

        # Eliminar la solicitud
        solicitud_table.delete_item(Key={'usuario_id': usuario_id, 'solicitud_id': solicitud_id})

        return {
            'statusCode': 200,
            'body': {
                'message': f'Solicitud {solicitud_id} del usuario {usuario_id} eliminada correctamente'
            }
        }

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno al eliminar la solicitud',
                'details': str(e)
            }
        }
