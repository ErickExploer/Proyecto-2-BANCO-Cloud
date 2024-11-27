import boto3
import json
from datetime import datetime
from decimal import Decimal

# Conexión a DynamoDB
dynamodb = boto3.resource('dynamodb')
prestamos_table = dynamodb.Table('TABLA-PRESTAMOS')

# Función auxiliar para convertir tipos numéricos a Decimal
def convertir_a_decimal(data):
    if isinstance(data, float):
        return Decimal(str(data))  # Convertir float a Decimal
    elif isinstance(data, dict):
        return {k: convertir_a_decimal(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convertir_a_decimal(i) for i in data]
    return data

# Función auxiliar para convertir Decimal a JSON serializable
def decimal_to_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 != 0 else int(obj)
    elif isinstance(obj, list):
        return [decimal_to_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: decimal_to_serializable(value) for key, value in obj.items()}
    return obj

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
        data = event['body']
        usuario_id = data['usuario_id']
        prestamo_id = data['prestamo_id']
        datos_a_actualizar = data.get('datos', {})

        print(f"Datos recibidos: usuario_id={usuario_id}, prestamo_id={prestamo_id}, datos_a_actualizar={datos_a_actualizar}")

        # Validar los campos requeridos
        if not usuario_id or not prestamo_id or not datos_a_actualizar:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'Solicitud inválida',
                    'details': 'El usuario_id, prestamo_id y datos a actualizar son obligatorios'
                }
            }

        # Validar que el préstamo exista
        response = prestamos_table.get_item(Key={'usuario_id': usuario_id, 'prestamo_id': prestamo_id})
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': {
                    'error': 'Préstamo no encontrado',
                    'details': f'No se encontró el préstamo con usuario_id {usuario_id} y prestamo_id {prestamo_id}'
                }
            }

        # Campos permitidos para la actualización
        campos_permitidos = {
            'cuenta_id', 'monto', 'descripcion', 'estado', 'plazo',
            'tasa_interes', 'fecha_creacion', 'fecha_vencimiento'
        }

        # Filtrar y convertir los campos permitidos a Decimal si es necesario
        datos_filtrados = {
            key: convertir_a_decimal(value) for key, value in datos_a_actualizar.items() if key in campos_permitidos
        }

        # Validar que haya al menos un campo permitido para actualizar
        if not datos_filtrados:
            return {
                'statusCode': 400,
                'body': {
                    'error': 'No hay campos válidos para actualizar',
                    'details': f'Campos permitidos: {list(campos_permitidos)}'
                }
            }

        # Construir la expresión de actualización dinámicamente
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}

        for key, value in datos_filtrados.items():
            attribute_name = f"#{key}"
            attribute_value = f":{key}"
            update_expression += f"{attribute_name} = {attribute_value}, "
            expression_attribute_names[attribute_name] = key
            expression_attribute_values[attribute_value] = value

        # Remover la última coma y espacio
        update_expression = update_expression.rstrip(", ")

        # Actualizar los datos en DynamoDB
        prestamos_table.update_item(
            Key={'usuario_id': usuario_id, 'prestamo_id': prestamo_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )

        return {
            'statusCode': 200,
            'body': {
                'message': f'Préstamo {prestamo_id} actualizado correctamente',
                'datos_actualizados': decimal_to_serializable(datos_filtrados)
            }
        }

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno al actualizar el préstamo',
                'details': str(e)
            }
        }
