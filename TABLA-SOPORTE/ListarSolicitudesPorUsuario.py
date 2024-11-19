
import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TABLA-SOPORTE')

def lambda_handler(event, context):
    try:
        # Cargar y manejar el cuerpo del evento
        data = json.loads(event['body'])
        usuario_id = data['usuario_id']
        
        # Realizar la consulta en la tabla DynamoDB
        response = table.query(
            KeyConditionExpression=Key('usuario_id').eq(usuario_id)
        )
        
        # Retornar todas las solicitudes del usuario
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])  # Convertir el resultado a JSON
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error interno del servidor: {str(e)}"})  # Convertir el error a JSON
        }
