import boto3
import json
from decimal import Decimal, getcontext, InvalidOperation

# Configurar el contexto global de Decimal
getcontext().prec = 28  # Precisión máxima
getcontext().traps[InvalidOperation] = False  # Evitar excepciones en operaciones inválidas

def decimal_to_serializable(obj):
    """
    Convierte objetos Decimal a int o float para que sean JSON serializables.
    """
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 else int(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-CUENTA')

    try:
        # Procesar el cuerpo de la solicitud
        if isinstance(event['body'], str):
            body = json.loads(event['body'])
        elif isinstance(event['body'], dict):
            body = event['body']
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Formato del cuerpo no soportado'})
            }

        usuario_id = body.get('usuario_id')
        cuenta_id = body.get('cuenta_id')
        monto = body.get('monto')

        # Validar campos obligatorios
        if not usuario_id or not cuenta_id or monto is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Solicitud inválida. Se requiere usuario_id, cuenta_id y monto.'})
            }

        # Convertir monto a Decimal con redondeo explícito
        try:
            monto = Decimal(str(monto)).quantize(Decimal('0.01'))  # Redondear a 2 decimales
        except Exception as e:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'El monto debe ser un número válido. Detalles: {str(e)}'})
            }

        # Actualizar saldo en DynamoDB
        try:
            response = table.update_item(
                Key={
                    'usuario_id': usuario_id,
                    'cuenta_id': cuenta_id
                },
                UpdateExpression="SET saldo = if_not_exists(saldo, :start) + :monto",
                ExpressionAttributeValues={
                    ':start': Decimal('0.00'),  # Valor inicial si saldo no existe
                    ':monto': monto            # Monto a sumar
                },
                ReturnValues="UPDATED_NEW"  # Devolver los valores actualizados
            )
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'Error en la actualización de DynamoDB: {str(e)}'})
            }

        # Convertir valores de respuesta a JSON serializable
        updated_attributes = json.loads(json.dumps(response['Attributes'], default=decimal_to_serializable))

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Saldo actualizado correctamente para la cuenta {cuenta_id}.',
                'updatedAttributes': updated_attributes
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error al actualizar el saldo: {str(e)}'})
        }

