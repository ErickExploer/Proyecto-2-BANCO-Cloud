import boto3
import json

def lambda_handler(event, context):
    body = event.get('body')
    if isinstance(body, str):
        body = json.loads(body)

    usuario_id = body.get('usuario_id')
    cuenta_id = body.get('cuenta_id')

    if not usuario_id or not cuenta_id:
        return {
            'statusCode': 400,
            'body': 'Solicitud inválida. Faltan usuario_id o cuenta_id.'
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

    try:
        response = table.delete_item(
            Key={
                'usuario_id': usuario_id,
                'cuenta_id': cuenta_id
            }
        )
        
        return {
            'statusCode': 200,
            'body': f'Cuenta con ID {cuenta_id} eliminada exitosamente para el usuario {usuario_id}.'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error al eliminar la cuenta: {str(e)}'
        }
