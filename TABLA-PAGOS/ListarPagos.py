import boto3
import json
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

def lambda_handler(event, context):
    try:
        # Verificar que 'body' existe en el evento
        if 'body' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'No se encontró el cuerpo de la solicitud en el evento'
                })
            }
        
        # Cargar el cuerpo de la solicitud
        data = event['body']
        
        # Validar que 'usuario_id' está presente en el JSON de entrada
        if 'usuario_id' not in data:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Solicitud inválida',
                    'details': 'Falta el campo usuario_id en el cuerpo de la solicitud'
                })
            }
        
        usuario_id = data['usuario_id']

        # Consultar en DynamoDB para obtener los pagos del usuario
        response = pagos_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('usuario_id').eq(usuario_id)
        )

        # Convertir el resultado a un formato JSON serializable
        items = response.get('Items', [])

        # Retornar los pagos en formato JSON
        return {
            'statusCode': 200,
            'body': items
        }
    
    except Exception as e:
        # Manejo de errores con detalles específicos
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error al listar los pagos',
                'details': str(e)
            })
        }
