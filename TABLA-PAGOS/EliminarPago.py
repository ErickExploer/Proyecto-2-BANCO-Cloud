import boto3
import json

# Conexión a DynamoDB
dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

def lambda_handler(event, context):
    print(f"Event recibido: {event}")  # Log para inspeccionar el evento recibido

    try:
        # Validar el cuerpo de la solicitud
        if 'body' not in event:
            print("Error: No se encontró el cuerpo de la solicitud.")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud'
                })
            }

        # Parsear el cuerpo de la solicitud
        data = json.loads(event['body'])
        print(f"Cuerpo parseado: {data}")  # Log del cuerpo parseado

        usuario_id = data.get('usuario_id')
        pago_id = data.get('pago_id')

        # Validar los campos requeridos
        if not usuario_id or not pago_id:
            print("Error: usuario_id o pago_id no proporcionados.")
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'El usuario_id y el pago_id son obligatorios'
                })
            }

        # Verificar si el pago existe antes de eliminarlo
        response = pagos_table.get_item(Key={'usuario_id': usuario_id, 'pago_id': pago_id})
        print(f"Respuesta de DynamoDB (get_item): {response}")  # Log de la respuesta de DynamoDB

        if 'Item' not in response:
            print(f"Pago no encontrado: usuario_id={usuario_id}, pago_id={pago_id}")
            return {
                'statusCode': 404,
                'body': {
                    'error': 'Pago no encontrado',
                    'details': f'No se encontró el pago con usuario_id {usuario_id} y pago_id {pago_id}'
                }
            }

        # Eliminar el pago
        pagos_table.delete_item(Key={'usuario_id': usuario_id, 'pago_id': pago_id})
        print(f"Pago eliminado: usuario_id={usuario_id}, pago_id={pago_id}")  # Log de la eliminación

        # Respuesta exitosa
        return {
            'statusCode': 200,
            'body': {
                'message': f'Pago {pago_id} del usuario {usuario_id} eliminado exitosamente'
            }
        }

    except Exception as e:
        # Manejo de errores inesperados
        print(f"Error inesperado: {str(e)}")  # Log del error
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno al eliminar el pago',
                'details': str(e)
            }
        }
