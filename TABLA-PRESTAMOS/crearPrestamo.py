import boto3
import json
from datetime import datetime
from decimal import Decimal, getcontext
import uuid

# Configurar contexto para Decimal
getcontext().prec = 28  # Configurar precisión global

# Conexión a DynamoDB
dynamodb = boto3.resource('dynamodb')
prestamos_table = dynamodb.Table('TABLA-PRESTAMOS')

# Función auxiliar para convertir Decimal a tipos JSON serializables
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
        # Obtener datos de la solicitud
        data = event['body']
        print(f"Datos recibidos: {data}")
        
        usuario_id = data['usuario_id']
        cuenta_id = data['cuenta_id']
        monto = Decimal(str(data['monto']))  # Asegurar que monto sea string antes de convertir
        plazo = int(data['plazo'])
        tasa_interes = Decimal(str(data['tasa_interes']))  # Asegurar que tasa_interes sea string
        descripcion = data.get('descripcion', 'Préstamo solicitado')

        # Generar un ID único para el préstamo
        prestamo_id = str(uuid.uuid4())

        # Cálculo del monto total con intereses
        monto_total = monto + (monto * tasa_interes / Decimal('100'))
        monto_total = monto_total.quantize(Decimal('0.01'))  # Redondear a 2 decimales

        # Crear el préstamo
        fecha_creacion = datetime.utcnow().isoformat()
        prestamo_item = {
            'usuario_id': usuario_id,
            'prestamo_id': prestamo_id,
            'cuenta_id': cuenta_id,
            'monto': monto_total,
            'descripcion': descripcion,
            'estado': 'activo',
            'plazo': plazo,
            'tasa_interes': tasa_interes,
            'fecha_creacion': fecha_creacion,
            'fecha_vencimiento': (datetime.utcnow().replace(year=datetime.utcnow().year + plazo // 12)).isoformat()
        }
        print(f"Préstamo a registrar: {prestamo_item}")

        prestamos_table.put_item(Item=prestamo_item)



        # Responder con los datos
        return {
            'statusCode': 200,
            'body': {
                'message': 'Préstamo creado exitosamente',
                'prestamo': decimal_to_serializable(prestamo_item)
            }
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': 'Error interno al crear el préstamo',
                'details': str(e)
            }
        }
