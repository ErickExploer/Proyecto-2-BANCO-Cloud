import boto3
import json

# Conexión a DynamoDB
dynamodb = boto3.resource('dynamodb')
prestamos_table = dynamodb.Table('TABLA-PRESTAMOS')

def lambda_handler(event, context):
    try:
        # Validar el cuerpo de la solicitud
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud'
                })
            }

        # Parsear el cuerpo de la solicitud
        data = json.loads(event['body'])
        usuario_id = data.get('usuario_id')
        prestamo_id = data.get('prestamo_id')

        print(f"Datos recibidos: usuario_id={usuario_id}, prestamo_id={prestamo_id}")

        # Validar los campos requeridos
        if not usuario_id or not prestamo_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'El usuario_id y el prestamo_id son obligatorios'
                })
            }

        # Validar que el préstamo exista
        response = prestamos_table.get_item(Key={'usuario_id': usuario_id, 'prestamo_id': prestamo_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Préstamo no encontrado',
                    'details': f'No se encontró el préstamo con usuario_id {usuario_id} y prestamo_id {prestamo_id}'
                })
            }

        # Eliminar el préstamo
        prestamos_table.delete_item(Key={'usuario_id': usuario_id, 'prestamo_id': prestamo_id})

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Préstamo {prestamo_id} eliminado correctamente',
                'usuario_id': usuario_id,
                'prestamo_id': prestamo_id
            })
        }

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error interno al eliminar el préstamo',
                'details': str(e)
            })
        }