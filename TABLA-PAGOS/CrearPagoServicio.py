import boto3
import uuid
from datetime import datetime
import json
from decimal import Decimal

# Obtener referencia a la tabla DynamoDB usando la variable de entorno
dynamodb = boto3.resource('dynamodb')
pagos_table = dynamodb.Table('TABLA-PAGOS')

def lambda_handler(event, context):
    try:
        # Cargar el cuerpo de la solicitud, conviértelo a JSON si es necesario
        data = json.loads(event['body'])
        
        # Validación de campos requeridos
        if 'usuario_id' not in data or 'datos_pago' not in data:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': "Campos 'usuario_id' y 'datos_pago' son obligatorios"
                })
            }
        
        datos_pago = data['datos_pago']
        if 'monto' not in datos_pago or 'titulo' not in datos_pago or 'descripcion' not in datos_pago:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': "Campos 'monto', 'titulo', y 'descripcion' son obligatorios en 'datos_pago'"
                })
            }
        
        # Validar que el monto sea un número positivo
        monto = datos_pago['monto']
        if not isinstance(monto, (int, float)) or monto <= 0:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': "El campo 'monto' debe ser un número positivo"
                })
            }
        
        # Convertir monto a Decimal para DynamoDB
        monto_decimal = Decimal(str(monto))
        
        # Definir datos de la transacción
        usuario_id = data['usuario_id']
        pago_id = str(uuid.uuid4())
        titulo = datos_pago['titulo']
        descripcion = datos_pago['descripcion']

        item = {
            'usuario_id': usuario_id,
            'pago_id': pago_id,
            'titulo': titulo,
            'descripcion': descripcion,
            'tipo': 'deuda',
            'monto': monto_decimal,
            'estado': 'pendiente',
            'fecha': datetime.utcnow().isoformat()
        }

        # Insertar en DynamoDB
        pagos_table.put_item(Item=item)
        
        # Respuesta de éxito
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': "Pago de deuda creado correctamente",
                'data': {
                    'usuario_id': usuario_id,
                    'pago_id': pago_id,
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'tipo': 'servicio',
                    'monto': float(monto_decimal),  # Convertir de vuelta para la respuesta
                    'estado': 'pendiente',
                    'fecha': item['fecha']
                }
            })
        }

    except Exception as e:
        print(f"Error en Lambda: {str(e)}")  # Imprimir error en los logs de CloudWatch
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': "Error interno del servidor",
                'details': str(e)
            })
        }
