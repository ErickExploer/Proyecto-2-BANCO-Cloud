import boto3
from boto3.dynamodb.conditions import Key

# Inicializar DynamoDB
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    try:
        # Convertir el cuerpo del evento a un diccionario
        data = eval(event['body']) if isinstance(event['body'], str) else event['body']
        cuenta_origen = data['cuenta_origen']
        
        # Obtener referencia a la tabla de transacciones
        transaccion_table = dynamodb.Table('TABLA-TRANSACCION')
        
        # Consultar transacciones por cuenta origen
        response = transaccion_table.query(
            KeyConditionExpression=Key('cuenta_origen').eq(cuenta_origen)
        )
        
        # Obtener los ítems de la consulta
        items = response.get('Items', [])
        
        # Respuesta exitosa
        return {
            'statusCode': 200,
            'body': {
                "message": "Transacciones listadas correctamente",
                "data": items
            }
        }
    
    except Exception as e:
        # Respuesta de error
        return {
            'statusCode': 500,
            'body': {
                "error": "Error al listar transacciones",
                "details": str(e)
            }
        }
