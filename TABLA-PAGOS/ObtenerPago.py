import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

# Función auxiliar para convertir Decimals a tipos JSON serializables
def decimal_to_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 != 0 else int(obj)
    elif isinstance(obj, list):
        return [decimal_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: decimal_to_serializable(v) for k, v in obj.items()}
    return obj

def lambda_handler(event, context):
    try:
        # Verificar si 'body' existe en el evento
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({  # Serializar a cadena JSON
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud en el evento'
                })
            }
        
        # Cargar el cuerpo de la solicitud
        data = json.loads(event['body'])
        
        # Validar que 'usuario_id' y 'pago_id' están presentes en el JSON de entrada
        if 'usuario_id' not in data or 'pago_id' not in data:
            return {
                'statusCode': 400,
                'body': json.dumps({  # Serializar a cadena JSON
                    'error': 'Solicitud inválida',
                    'details': 'Faltan campos obligatorios: usuario_id o pago_id en el cuerpo de la solicitud'
                })
            }
        
        usuario_id = data['usuario_id']
        pago_id = data['pago_id']

        # Consulta en DynamoDB para obtener el pago específico
        response = pagos_table.get_item(
            Key={'usuario_id': usuario_id, 'pago_id': pago_id}
        )

        # Verificar si el ítem fue encontrado
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({  # Serializar a cadena JSON
                    'error': 'Pago no encontrado',
                    'details': f'No se encontró el pago con ID {pago_id} para el usuario {usuario_id}'
                })
            }

        # Convertir el resultado a un formato JSON serializable
        item = decimal_to_serializable(response['Item'])

        # Retornar el pago en formato JSON
        return {
            'statusCode': 200,
            'body': item  
        }
    
    except Exception as e:
        # Manejo de errores con detalles específicos
        return {
            'statusCode': 500,
            'body': json.dumps({  # Serializar a cadena JSON
                'error': 'Error interno del servidor',
                'details': str(e)
            })
        }
