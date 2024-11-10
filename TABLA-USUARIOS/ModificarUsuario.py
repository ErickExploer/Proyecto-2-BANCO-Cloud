import boto3
import json
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    body = event.get('body')
    if body is None:
        body = event
    elif isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': 'Solicitud inválida. El formato del JSON es incorrecto.'
            }

    usuario_id = body.get('usuario_id')
    updated_data = body
    if not usuario_id or not updated_data:
        return {
            'statusCode': 400,
            'body': 'Solicitud inválida. Faltan usuario_id o datos de actualización.'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-USUARIOS')
    
    update_expression = "set "
    expression_attribute_values = {}
    for key, value in updated_data.items():
        if key != 'usuario_id':
            if key == "password":
                hashed_password = hash_password(value)
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = hashed_password
            else:
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
    update_expression = update_expression.rstrip(", ")

    try:
        response = table.update_item(
            Key={'usuario_id': usuario_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )

        return {
            'statusCode': 200,
            'body': f'Usuario {usuario_id} modificado exitosamente'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al modificar el usuario: {str(e)}'
        }
import boto3
import json
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    body = event.get('body')
    if body is None:
        body = event
    elif isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': 'Solicitud inválida. El formato del JSON es incorrecto.'
            }

    usuario_id = body.get('usuario_id')
    updated_data = body
    if not usuario_id or not updated_data:
        return {
            'statusCode': 400,
            'body': 'Solicitud inválida. Faltan usuario_id o datos de actualización.'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TABLA-USUARIOS')
    
    update_expression = "set "
    expression_attribute_values = {}
    for key, value in updated_data.items():
        if key != 'usuario_id':
            if key == "password":
                hashed_password = hash_password(value)
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = hashed_password
            else:
                update_expression += f"{key} = :{key}, "
                expression_attribute_values[f":{key}"] = value
    update_expression = update_expression.rstrip(", ")

    try:
        response = table.update_item(
            Key={'usuario_id': usuario_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )

        return {
            'statusCode': 200,
            'body': f'Usuario {usuario_id} modificado exitosamente'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al modificar el usuario: {str(e)}'
        }
