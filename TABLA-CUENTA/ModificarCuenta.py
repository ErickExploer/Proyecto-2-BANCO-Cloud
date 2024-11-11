import boto3
import json
from decimal import Decimal

def decimal_to_float(item):
    for key, value in item.items():
        if isinstance(value, Decimal):
            item[key] = float(value)
    return item

def lambda_handler(event, context):
    body = event.get('body')
    if isinstance(body, str):
        body = json.loads(body)

    usuario_id = body.get('usuario_id')
    cuenta_id = body.get('cuenta_id')
    cuenta_datos = body.get('cuenta_datos', {})

    if not usuario_id or not cuenta_id or not cuenta_datos:
        return {
            'statusCode': 400,
            'body': 'Solicitud inválida. Faltan usuario_id, cuenta_id o cuenta_datos.'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-CUENTA')

    try:
        existing_account = table.get_item(
            Key={
                'usuario_id': usuario_id,
                'cuenta_id': cuenta_id
            }
        )
        if 'Item' not in existing_account:
            return {
                'statusCode': 404,
                'body': f'La cuenta con ID {cuenta_id} para el usuario {usuario_id} no existe.'
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al verificar la existencia de la cuenta: {str(e)}'
        }

    update_expression = "set "
    expression_attribute_values = {}
    for key, value in cuenta_datos.items():
        if isinstance(value, float):
            expression_attribute_values[f":{key}"] = Decimal(str(value))
        else:
            expression_attribute_values[f":{key}"] = value
        update_expression += f"{key} = :{key}, "
    update_expression = update_expression.rstrip(", ")

    try:
        response = table.update_item(
            Key={
                'usuario_id': usuario_id,
                'cuenta_id': cuenta_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )

        updated_attributes = decimal_to_float(response.get("Attributes", {}))

        return {
            'statusCode': 200,
            'body': updated_attributes
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al modificar la cuenta: {str(e)}'
        }
